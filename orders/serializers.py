from rest_framework import serializers
from django.shortcuts import get_object_or_404

from datetime import datetime, timedelta
from vendor.models import Vendor
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    vendor_id = serializers.CharField(write_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = [
            "po_number",
            "vendor",
            "order_date",
            "delivery_date",
            "expected_delivery_date",
            "status",
            "issue_date",
            "quality_rating",
            "acknowledgement_date",
        ]

    def validate_vendor_id(self, value):
        if value is None or value == "null":
            raise serializers.ValidationError("vendor_id required")
        if isinstance(value, str):
            return value
        raise serializers.ValidationError("vendor_id not a string")

    def create(self, validated_data):
        vendor_id = validated_data.get("vendor_id")
        vendor = get_object_or_404(Vendor, vendor_code=vendor_id)
        validated_data["vendor"] = vendor
        validated_data["expected_delivery_date"] = datetime.now() + timedelta(days=5)
        validated_data["issue_date"] = datetime.now()
        return super().create(validated_data)


class OrderAcknowledgeSerializer(serializers.Serializer):
    acknowledgement_date = serializers.DateTimeField()

    def update(self, instance, validated_data):
        instance.acknowledgement_date = validated_data.get(
            "acknowledgement_date", datetime.now()
        )
        instance.save()
        return instance


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status", "delivery_date"]


class OrderRatingSerializer(serializers.ModelSerializer):
    quality_rating = serializers.FloatField()

    class Meta:
        model = Order
        fields = ["quality_rating"]
