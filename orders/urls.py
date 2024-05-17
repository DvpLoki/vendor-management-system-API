from django.urls import path


from orders.views import (
    OrderGetPutDelete,
    OrderListCreate,
    OrderAcknowledgement,
    OrderRating,
)

urls = [
    path("purchase_orders/", OrderListCreate.as_view()),
    path("purchase_orders/<str:po_id>/", OrderGetPutDelete.as_view()),
    path("purchase_orders/<str:po_id>/acknowledge", OrderAcknowledgement),
    path("purchase_orders/<str:po_id>/rating", OrderRating),
]
