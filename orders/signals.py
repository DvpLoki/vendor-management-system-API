from datetime import datetime
from django.db.models import F, Count, Case, When, FloatField, Value, Q, Avg
from django.dispatch import Signal, receiver
from orders.models import Order
from vendor.models import Vendor, HistoricalPerformance


order_completed = Signal(["order"])
quality_rated = Signal(["order"])
acknowledged = Signal(["order"])


@receiver(order_completed)
def delivery_and_fulfillment_rate(sender, order, **kwargs):
    if order.status != "pending":
        vendor = Vendor.objects.get(vendor_code=order.vendor.vendor_code)
        orders = Order.objects.filter(vendor=vendor.vendor_code)
        total_orders_issued = orders.count()
        orders_completed = (
            orders.filter(status="completed")
            .annotate(
                on_time=Case(
                    When(delivery_date__lte=F("expected_delivery_date"), then=Value(1)),
                    default=Value(0),
                    output_field=FloatField(),
                )
            )
            .aggregate(
                total_completed=Count("po_number"),
                total_on_time_completed=Count("on_time", filter=Q(on_time=1)),
            )
        )

        if orders_completed["total_completed"] > 0:
            on_time_delivery_rate = (
                orders_completed["total_on_time_completed"]
                / orders_completed["total_completed"]
            ) * 100
            fulfillment_rate = (
                orders_completed["total_completed"] / total_orders_issued
            ) * 100

        else:
            on_time_delevery_rate = 0
            fulfillment_rate = 0
        vendor.on_time_delivery_rate = on_time_delivery_rate
        vendor.fulfillment_rate = fulfillment_rate
        vendor.save()
        history = HistoricalPerformance(
            vendor=vendor,
            on_time_delivery_rate=vendor.on_time_delivery_rate,
            fulfillment_rate=vendor.fulfillment_rate,
            quality_rating_avg=vendor.quality_rating_avg,
            average_response_time=vendor.average_response_time,
        )
        history.save()


@receiver(quality_rated)
def quality_rating_avg(sender, order, **kwargs):
    vendor = Vendor.objects.get(vendor_code=order.vendor.vendor_code)
    orders = Order.objects.filter(
        vendor=vendor.vendor_code, quality_rating__isnull=False, status="completed"
    ).aggregate(avg_rating=Avg("quality_rating"))
    vendor.quality_rating_avg = orders["avg_rating"]
    vendor.save()
    history = HistoricalPerformance(
        vendor=vendor,
        on_time_delivery_rate=vendor.on_time_delivery_rate,
        fulfillment_rate=vendor.fulfillment_rate,
        quality_rating_avg=vendor.quality_rating_avg,
        average_response_time=vendor.average_response_time,
    )
    history.save()


@receiver(acknowledged)
def avg_response_time(sender, order, **kwargs):
    vendor = Vendor.objects.get(vendor_code=order.vendor.vendor_code)
    orders = (
        Order.objects.filter(vendor=vendor.vendor_code)
        .annotate(time_diff=F("acknowledgement_date") - F("issue_date"))
        .aggregate(avg_res=Avg("time_diff"))
    )
    vendor.average_response_time = orders["avg_res"].total_seconds() / 60
    vendor.save()
    history = HistoricalPerformance(
        vendor=vendor,
        on_time_delivery_rate=vendor.on_time_delivery_rate,
        fulfillment_rate=vendor.fulfillment_rate,
        quality_rating_avg=vendor.quality_rating_avg,
        average_response_time=vendor.average_response_time,
    )
    history.save()
