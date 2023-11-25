from .models import VendorModel, PerformanceModel
from rest_framework import serializers


class VendorSerializer(serializers.ModelSerializer):
    on_time_delivery_rate = serializers.FloatField(read_only=True)
    quality_rating_avg = serializers.FloatField(read_only=True)
    average_response_time = serializers.FloatField(read_only=True)
    fulfillment_rate = serializers.FloatField(read_only=True)

    class Meta:
        model = VendorModel
        fields = [
            "name",
            "contact_details",
            "address",
            "vendor_code",
            "on_time_delivery_rate",
            "quality_rating_avg",
            "average_response_time",
            "fulfillment_rate",
        ]


class PerformanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PerformanceModel
        fields = [
            "vendor",
            "date",
            "on_time_delivery_rate",
            "quality_rating_avg",
            "average_response_time",
            "fulfillment_rate",
        ]
