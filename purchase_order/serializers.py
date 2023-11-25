from .models import PurchaseOrderModel
from rest_framework import serializers


class PurchaseSerializer(serializers.ModelSerializer):
    quality_rating = serializers.IntegerField(allow_null=True, default=None)
    issue_date = serializers.DateTimeField(read_only=True)
    acknowledgement_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = PurchaseOrderModel
        fields = [
            "po_number",
            "vendor",
            "order_date",
            "delivery_date",
            "items",
            "quantity",
            "status",
            "quality_rating",
            "issue_date",
            "acknowledgement_date",
        ]
