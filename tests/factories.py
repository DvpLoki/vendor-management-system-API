import factory
from django.contrib.auth.models import User
from orders.models import Order
from vendor.models import Vendor, HistoricalPerformance


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.sequence(lambda n: "loki%s" % n)
    password = "password"


class VendorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vendor

    name = factory.sequence(lambda n: "loki%s" % n)
    contact_details = factory.sequence(lambda n: "98765432%s" % n)
    address = "andhra pradesh , india"
    user = factory.SubFactory(UserFactory)


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    vendor = factory.SubFactory(VendorFactory)
    items = [{"pid": 9877, "price": 977}]
    quantity = 3
