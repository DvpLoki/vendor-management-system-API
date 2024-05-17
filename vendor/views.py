from rest_framework import permissions, views, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


from orders import serializers
from vendor.models import Vendor, HistoricalPerformance
from vendor.serializers import (
    HistoricalPerformanceSerializer,
    VendorPerformanceSerializer,
    VendorSerializer,
    VendorUpdateSerializer,
)


class VendorListCreate(views.APIView):
    serializer_class = VendorSerializer

    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = self.serializer_class(vendors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorGetPutDelete(views.APIView):
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, id):
        obj = get_object_or_404(Vendor, vendor_code=id)
        return obj

    def get(self, request, vendor_id, format=None):
        if vendor_id == "null" or vendor_id == "":
            return Response(
                {"detail": "invalid vendor id "}, status=status.HTTP_400_BAD_REQUEST
            )
        vendor = self.get_object(vendor_id)
        serializer = self.serializer_class(vendor)
        return Response(serializer.data)

    def put(self, request, vendor_id, format=None):
        if vendor_id == "null" or vendor_id == "":
            return Response(
                {"detail": "invalid vendor id "}, status=status.HTTP_400_BAD_REQUEST
            )
        vendor = self.get_object(vendor_id)
        ## do authentication if user = vendor model
        serializer = VendorUpdateSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, vendor_id, format=None):
        if vendor_id == "null" or vendor_id == "":
            return Response(
                {"detail": "invalid vendor id "}, status=status.HTTP_400_BAD_REQUEST
            )
        vendor = self.get_object(vendor_id)
        # do authentication for if user ==vendor
        user = User.objects.get(vendor=vendor)
        user.delete()
        return Response(
            data={"msg": "deleted successfully"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
def Performance(request, vendor_id):
    if vendor_id == "null" or vendor_id == "":
        return Response(
            {"detail": "invalid vendor id "}, status=status.HTTP_400_BAD_REQUEST
        )
    vendor = get_object_or_404(Vendor, vendor_code=vendor_id)
    serializer = VendorPerformanceSerializer(vendor)
    return Response(serializer.data)


@api_view(["GET"])
def PerformanceHistory(request, vendor_id):
    if vendor_id == "null" or vendor_id == "":
        return Response(
            {"detail": "invalid vendor id "}, status=status.HTTP_400_BAD_REQUEST
        )
    vendor = get_object_or_404(Vendor, vendor_code=vendor_id)
    history = HistoricalPerformance.objects.filter(vendor=vendor.vendor_code).order_by(
        "-date"
    )
    if not history:
        return Response(
            {"detail": "no history recorded"}, status=status.HTTP_204_NO_CONTENT
        )
    serializer = HistoricalPerformanceSerializer(history, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
