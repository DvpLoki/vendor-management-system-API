from django.db import models
from django.contrib.auth.models import User
import uuid


class Vendor(models.Model):
    name = models.CharField(null=False, unique=False, max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="vendor")
    contact_details = models.TextField(unique=True, max_length=12, null=False)
    address = models.TextField(null=False)
    vendor_code = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self) -> str:
        return self.name


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(
        Vendor, related_name="historical_performance", on_delete=models.CASCADE
    )
    date = models.DateTimeField(auto_now_add=True, editable=False)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self) -> str:
        return f"{self.vendor.name}-{self.date}"
