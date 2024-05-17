import pytest
from datetime import datetime

pytestmark = pytest.mark.django_db


class TestOrderListCreate:
    endpoint = "/api/purchase_orders/"

    def test_get_orders(self, order_factory, api_client):
        order_factory.create_batch(5)
        res = api_client().get(self.endpoint)
        assert res.status_code == 200
        assert len(res.data) == 5

    def test_create_order(self, api_client, vendor_factory):
        vendor = vendor_factory()
        vendor_code = vendor.vendor_code
        res = api_client().post(
            self.endpoint,
            {
                "vendor_id": vendor_code,
                "items": [{"pid": "979373", "price": "65666"}],
                "quantity": 3,
            },
            format="json",
        )
        assert res.status_code == 201
        assert res.data["vendor"] == f"{vendor_code}"


class TestOrderGetPutDelete:
    endpoint = "/api/purchase_orders"

    def test_get_order_by_id(self, order_factory, api_client):
        order = order_factory()
        po_id = order.po_number
        res = api_client().get(f"{self.endpoint}/{po_id}/")
        assert res.data["po_number"] == f"{po_id}"
        assert res.status_code == 200

    def test_update_order(self, api_client, order_factory):
        order = order_factory(acknowledgement_date=datetime.now())
        po_id = order.po_number
        res = api_client().put(
            f"{self.endpoint}/{po_id}/",
            {"delivery_date": "2024-05-12T10:50", "status": "completed"},
            format="json",
        )
        assert res.data["status"] == "completed"
        assert res.status_code == 200

    def test_delete_order(self, api_client, order_factory):
        order = order_factory()
        po_id = order.po_number
        res = api_client().delete(
            f"{self.endpoint}/{po_id}/",
        )
        assert res.status_code == 404


class TestOrderAcknowledgementAndRating:
    endpoint = "/api/purchase_orders"

    def test_order_acknowlegement(self, api_client, order_factory):
        order = order_factory(issue_date=datetime.now())
        po_id = order.po_number
        res = api_client().post(
            f"{self.endpoint}/{po_id}/acknowledge",
            {"acknowledgement_date": "2024-05-12T10:50"},
            format="json",
        )
        assert res.status_code == 200

    def test_order_rating(self, api_client, order_factory):
        order = order_factory(acknowledgement_date=datetime.now(), status="completed")
        po_id = order.po_number
        res = api_client().post(
            f"{self.endpoint}/{po_id}/rating",
            {"quality_rating": 4},
            format="json",
        )
        assert res.data["quality_rating"] == 4
        assert res.status_code == 200
