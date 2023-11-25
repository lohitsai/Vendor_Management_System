from django.db import models
from vendor.models import VendorModel, PerformanceModel
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
import pytz


# Creating the Purchase Order Model
class PurchaseOrderModel(models.Model):
    po_number = models.CharField(max_length=30, primary_key=True)
    vendor = models.ForeignKey(
        VendorModel, on_delete=models.SET_NULL, null=True, blank=False
    )
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField(default=dict)
    quantity = models.IntegerField(default=0)
    status = models.CharField(max_length=10)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgement_date = models.DateTimeField(null=True, blank=True)
    Completed = models.BooleanField(default=False, auto_created=True)
