from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from vendor.views import (
    Performance,
    VendorGetPutDelete,
    VendorListCreate,
    PerformanceHistory,
)

urls = [
    path("vendors/login", TokenObtainPairView.as_view()),
    path("vendors/login/refresh", TokenRefreshView.as_view()),
    path("vendors/", VendorListCreate.as_view()),
    path("vendors/<str:vendor_id>/", VendorGetPutDelete.as_view()),
    path("vendors/<str:vendor_id>/performance", Performance),
    path("vendors/<str:vendor_id>/performance-history", PerformanceHistory),
]
