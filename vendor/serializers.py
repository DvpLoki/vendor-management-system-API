from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Vendor, HistoricalPerformance


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {"password": {"write_only": True}}


class VendorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Vendor
        fields = ["vendor_code", "name", "contact_details", "address", "user"]

    def create(self, validated_data):
        userdata = validated_data.pop("user")
        user = User(**userdata)
        user.set_password(userdata["password"])
        user.save()
        vendor = Vendor(**validated_data)
        vendor.user = user
        vendor.save()
        return vendor


class VendorUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        fields = ["name", "address"]


class VendorPerformanceSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Vendor
        fields = "__all__"


class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = "__all__"
