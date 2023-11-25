from django.db import models


# Create your models here.
class VendorModel(models.Model):
    name = models.CharField(max_length=30)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=5, primary_key=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)
    num_orders = models.IntegerField(default=0)
    num_fulfilled_orders = models.IntegerField(default=0)
    # num_on_time_orders = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.vendor_code


class PerformanceModel(models.Model):
    vendor = models.ForeignKey(VendorModel, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()
