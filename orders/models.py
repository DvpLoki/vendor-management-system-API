from operator import truediv
from django.db import models
from vendor.models import Vendor
import uuid


class Order(models.Model):

    class status_enum(models.TextChoices):
        CANCELED = "canceled"
        PENDING = "pending"
        COMPLETED = "completed"

    po_number = models.CharField(
        max_length=10, unique=True, primary_key=True, default=uuid.uuid4, editable=False
    )
    vendor = models.ForeignKey(Vendor, related_name="orders", on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    expected_delivery_date = models.DateTimeField(null=True)
    delivery_date = models.DateTimeField(null=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(
        choices=status_enum.choices, default=status_enum.PENDING, max_length=10
    )
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField(null=True)
    acknowledgement_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.po_number
