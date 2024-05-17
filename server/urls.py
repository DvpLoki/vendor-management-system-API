from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from vendor.urls import urls as vendor_urls
from orders.urls import urls as order_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(vendor_urls)),
    path("api/", include(order_urls)),
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/docs/", SpectacularSwaggerView.as_view()),
    path("api/schema/redocs/", SpectacularRedocView.as_view()),
]
