from tokenize import endpats
import pytest

import vendor

pytestmark = pytest.mark.django_db


class TestVendorListCreate:
    endpoint = "/api/vendors/"

    def test_get_all_vendors(self, api_client, vendor_factory):
        vendor_factory.create_batch(5)
        res = api_client().get(self.endpoint)
        assert res.status_code == 200
        assert len(res.data) == 5

    def test_create_vendor(self, api_client):
        res = api_client().post(
            self.endpoint,
            {
                "user": {"username": "loki1234", "password": "password"},
                "name": "loki",
                "contact_details": "28438195003",
                "address": "gunture ",
            },
            format="json",
        )
        assert res.status_code == 201
        assert res.data["user"]["username"] == "loki1234"


class TestVendorGetPutDelete:
    endpoint = "/api/vendors"

    def test_get_vendor_by_id(self, vendor_factory, api_client):
        vendor = vendor_factory()
        vendor_id = vendor.vendor_code
        res = api_client().get(f"{self.endpoint}/{vendor_id}/")
        assert res.data["vendor_code"] == f"{vendor_id}"
        assert res.status_code == 200

    def test_update_vendor(self, api_client):
        # creating vendor
        vendor = api_client().post(
            f"{self.endpoint}/",
            {
                "user": {"username": "loki1234", "password": "password"},
                "name": "loki",
                "contact_details": "28438195003",
                "address": "gunture ",
            },
            format="json",
        )
        assert vendor.data["name"] == "loki"
        assert vendor.data["user"]["username"] == "loki1234"
        vendor_id = vendor.data["vendor_code"]

        # login required for token
        token = api_client().post(
            f"{self.endpoint}/login",
            {"username": "loki1234", "password": "password"},
        )
        assert token.status_code == 200
        # updating a vendor
        res = api_client().put(
            f"{self.endpoint}/{vendor_id}/",
            {"name": "devarapu ", "address": "vizag,indore"},
            headers={
                "Authorization": f'Bearer {token.data["access"]}',
            },
            format="json",
        )
        assert res.status_code == 200
        assert res.data["name"] == "devarapu"

    def delete_vendor(self, api_client):
        # creating vendor
        vendor = api_client().post(
            f"{self.endpoint}/",
            {
                "user": {"username": "loki007", "password": "password"},
                "name": "loki",
                "contact_details": "28438195003",
                "address": "gunture ",
            },
            format="json",
        )

        assert vendor.data["user"]["username"] == "loki007"
        vendor_id = vendor.data["vendor_code"]

        # login required for token
        token = api_client().post(
            f"{self.endpoint}/login",
            {"username": "loki007", "password": "password"},
        )
        assert token.status_code == 200
        # deleting a vendor
        res = api_client().delete(
            f"{self.endpoint}/{vendor_id}/",
            headers={
                "Authorization": f'Bearer {token.data["access"]}',
            },
            format="json",
        )
        assert res.status_code == 404


class TestVendorPerformance:
    endpoint = "/api/vendors"

    def test_vendor_performance(self, api_client, vendor_factory):
        vendor = vendor_factory()
        vendor_id = vendor.vendor_code
        res = api_client().get(f"{self.endpoint}/{vendor_id}/performance")
        assert res.status_code == 200

    def test_vendor_performance_history(self, api_client, order_factory):
        order = order_factory(
            issue_date="2024-05-11T10:50", expected_delivery_date="2024-05-13T10:20"
        )
        po_id = order.po_number
        vendor_id = order.vendor.vendor_code
        order_acknowledge = api_client().post(
            f"/api/purchase_orders/{po_id}/acknowledge",
            {"acknowledgement_date": "2024-05-11T10:55"},
            format="json",
        )
        order_update = api_client().put(
            f"/api/purchase_orders/{po_id}/",
            {"delivery_date": "2024-05-13T10:10", "status": "completed"},
            format="json",
        )
        order_rating = api_client().post(
            f"/api/purchase_orders/{po_id}/rating",
            {"quality_rating": 4},
            format="json",
        )
        res = api_client().get(f"{self.endpoint}/{vendor_id}/performance")
        assert res.data["on_time_delivery_rate"] == 100.0
        assert res.data["quality_rating_avg"] == 4.0
        assert res.data["average_response_time"] == 5.0
        assert res.status_code == 200

        vendor_history = api_client().get(
            f"{self.endpoint}/{vendor_id}/performance-history"
        )
        assert len(vendor_history.data) == 3


class TestLoginRefresh:
    endpoint = "/api/vendors"

    def test_login(self, api_client):
        # creating vendor
        vendor = api_client().post(
            f"{self.endpoint}/",
            {
                "user": {"username": "loki007", "password": "password"},
                "name": "loki",
                "contact_details": "28438195003",
                "address": "gunture ",
            },
            format="json",
        )

        assert vendor.data["user"]["username"] == "loki007"
        vendor_id = vendor.data["vendor_code"]

        res = api_client().post(
            f"{self.endpoint}/login",
            {"username": "loki007", "password": "password"},
        )
        assert res.status_code == 200

    def test_refresh_token(self, api_client):
        # creating vendor
        vendor = api_client().post(
            f"{self.endpoint}/",
            {
                "user": {"username": "loki007", "password": "password"},
                "name": "loki",
                "contact_details": "28438195003",
                "address": "gunture ",
            },
            format="json",
        )

        assert vendor.data["user"]["username"] == "loki007"
        vendor_id = vendor.data["vendor_code"]

        token = api_client().post(
            f"{self.endpoint}/login",
            {"username": "loki007", "password": "password"},
            format="json",
        )
        assert token.status_code == 200
        res = api_client().post(
            f"{self.endpoint}/login/refresh",
            {"refresh": token.data["refresh"]},
            format="json",
        )
        assert res.status_code == 200
