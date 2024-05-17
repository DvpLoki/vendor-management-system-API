from rest_framework import generics, views, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from orders.signals import order_completed, quality_rated, acknowledged
from orders.models import Order
from orders.serializers import (
    OrderSerializer,
    OrderAcknowledgeSerializer,
    OrderStatusSerializer,
    OrderRatingSerializer,
)


class OrderListCreate(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderGetPutDelete(views.APIView):
    serializer_class = OrderSerializer

    def get_object(self, po_id):
        obj = get_object_or_404(Order, po_number=po_id)
        return obj

    def get(self, request, po_id, format=None):
        if po_id == "null" or po_id == "":
            return Response(
                {"detail": "invalid po_id"}, status=status.HTTP_400_BAD_REQUEST
            )
        order = self.get_object(po_id)
        serializer = self.serializer_class(order)
        return Response(serializer.data)

    def put(self, request, po_id, format=None):
        if po_id == "null" or po_id == "":
            return Response(
                {"detail": "invalid po_id"}, status=status.HTTP_400_BAD_REQUEST
            )
        order = self.get_object(po_id)
        ## do authentication if user = order model
        if order.acknowledgement_date:
            serializer = OrderStatusSerializer(order, data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                if serializer.validated_data["status"] != "pending":
                    order_completed.send(sender=self.__class__, order=order)
                return Response(serializer.data)
        return Response(
            {"detail": "order not Acknowledged "}, status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, po_id, format=None):
        if po_id == "null" or po_id == "":
            return Response(
                {"detail": "invalid po_id"}, status=status.HTTP_400_BAD_REQUEST
            )
        order = self.get_object(po_id)
        # do authentication for if user ==vendor

        order.delete()
        return Response(
            data={"msg": "deleted successfully"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["POST"])
def OrderAcknowledgement(request, po_id):
    if po_id == "null" or po_id == "":
        return Response({"detail": "invalid po_id"}, status=status.HTTP_400_BAD_REQUEST)
    order = get_object_or_404(Order, po_number=po_id)
    # authenticate if user = vendor of order model
    if order.acknowledgement_date:
        return Response(
            {"detail": "already acknowledged"}, status.HTTP_208_ALREADY_REPORTED
        )
    serializer = OrderAcknowledgeSerializer(order, request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        acknowledged.send(sender=OrderAcknowledgement, order=order)
        return Response(serializer.data)


@api_view(["POST"])
def OrderRating(request, po_id):
    if po_id == "null" or po_id == "":
        return Response({"detail": "invalid po_id"}, status=status.HTTP_400_BAD_REQUEST)
    order = get_object_or_404(Order, po_number=po_id)
    # authenticate if user for rating
    if order.status == "pending":
        return Response({"detail": "Order not completed"}, status.HTTP_400_BAD_REQUEST)
    if order.quality_rating:
        return Response({"detail": "already rated"}, status.HTTP_208_ALREADY_REPORTED)
    serializer = OrderRatingSerializer(order, request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        quality_rated.send(sender=OrderRating, order=order)
        return Response(serializer.data)
