from rest_framework.test import APIClient
import pytest
from pytest_factoryboy import register
from .factories import OrderFactory, VendorFactory, UserFactory

register(UserFactory)
register(VendorFactory)
register(OrderFactory)


@pytest.fixture
def api_client():
    return APIClient
