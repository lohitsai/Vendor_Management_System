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
    acknowledged = models.BooleanField(default=False, auto_created=True)
    Completed = models.BooleanField(default=False, auto_created=True)
    created = models.BooleanField(default=False, auto_created=True)

    # overridding save method to write custom logic to update the associated vendor model metrics
    def save(self, *args, **kwargs):
        # getting assoicated vendor instance
        vendor = VendorModel.objects.get(vendor_code=self.vendor)
        if not self.created:
            vendor.num_orders += 1
            self.created = True

        # checking if the request is a new purchase order or updating an existing purchase order
        if self.status == "completed" and not self.Completed:
            vendor.num_fulfilled_orders += 1
            # checking if the purchase order was delivered on time and updating the on_time_delivery_rate accordingly on the vendor instance
            if self.delivery_date < datetime.now(tz=pytz.utc):
                vendor.on_time_delivery_rate = (
                    vendor.on_time_delivery_rate * (vendor.num_fulfilled_orders - 1)
                ) / vendor.num_fulfilled_orders
            else:
                vendor.on_time_delivery_rate = (
                    (vendor.on_time_delivery_rate * (vendor.num_fulfilled_orders - 1))
                    + 1
                ) / vendor.num_fulfilled_orders

            # Updating the avg quality rating on the associated vendor instance
            vendor.quality_rating_avg = (
                vendor.quality_rating_avg * (vendor.num_fulfilled_orders - 1)
                + self.quality_rating
            ) / vendor.num_fulfilled_orders

            self.Completed = True

        # checking if the purchase order has been acknowleded or not
        # and updating the average_response_time on the vendor instace
        if (
            self.acknowledgement_date != None
            and self.acknowledgement_date != ""
            and not self.acknowledged
        ):
            vendor.average_response_time = (
                # convering time difference into hours
                vendor.average_response_time * (vendor.num_orders - 1)
                + (self.acknowledgement_date - self.issue_date).seconds / 3600
            ) / (vendor.num_orders)
            self.acknowledged = True

        # Updating the fullfillment rate
        vendor.fulfillment_rate = vendor.num_fulfilled_orders / vendor.num_orders

        # updating the historical record of the vendor
        PerformanceModel(
            vendor=vendor,
            date=datetime.now(tz=pytz.utc),
            on_time_delivery_rate=vendor.on_time_delivery_rate,
            quality_rating_avg=vendor.quality_rating_avg,
            average_response_time=vendor.average_response_time,
            fulfillment_rate=vendor.fulfillment_rate,
        ).save()
        # saving the vendor instance to the database
        vendor.save()
        super().save(*args, **kwargs)
