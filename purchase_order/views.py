from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from vendor.models import *
from datetime import datetime
import pytz


# Purchase Orders API Endpoint Class Based View
class Purchases(APIView):
    # creating a new Purchase Order
    def post(self, request):
        serializer = PurchaseSerializer(data=request.data, context={"request": request})
        vendor = VendorModel.objects.get(vendor_code=serializer.data["vendor"])
        vendor.num_orders += 1
        vendor.save()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # getting all Purchase Orders
    def get(self, request):
        orders = PurchaseOrderModel.objects.all()
        serializer = PurchaseSerializer(orders, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


# Purchase Order API Endpoint Class Based View
class Purchase(APIView):
    # getting a single Purchase Order Instance using the Purchase Order id
    def get(self, request, id):
        order = PurchaseOrderModel.objects.get(pk=id)
        serializer = PurchaseSerializer(order, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # updating a single Purchase Order data using the Purchase Order id
    def put(self, request, id):
        # getting the Purchase Order Instance using the Purchase order id
        order = PurchaseOrderModel.objects.get(pk=id)
        serializer = PurchaseSerializer(
            order, data=request.data, context={"request": request}
        )

        # getting the Associated Vendor Instance to update it metrics
        vendor = VendorModel.objects.get(vendor_code=serializer.data["vendor"])

        # checking if the purchase order is completed
        if (
            serializer.data["status"] == "completed"
            and not serializer.data["Completed"]
        ):
            vendor.num_fulfilled_orders += 1
            # checking if the purchase order was delivered on time and updating the on_time_delivery_rate accordingly on the vendor instance
            if serializer.data["delivery_date"] < datetime.now(tz=pytz.utc):
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
                + serializer.data["quality_rating"]
            ) / vendor.num_fulfilled_orders

            # Updating the fullfillment rate
            vendor.fulfillment_rate = vendor.num_fulfilled_orders / vendor.num_orders
            serializer.data["Completed"] = True
        # updating the historical record of the vendor and saving it
        PerformanceModel(
            vendor=vendor,
            date=datetime.now(tz=pytz.utc),
            on_time_delivery_rate=vendor.on_time_delivery_rate,
            quality_rating_avg=vendor.quality_rating_avg,
            average_response_time=vendor.average_response_time,
            fulfillment_rate=vendor.fulfillment_rate,
        ).save()

        # saving the vendor Instance
        vendor.save()

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # deleting a single Purchase Order using the Purchase Order id
    def delete(self, request, id):
        order = PurchaseOrderModel.objects.get(pk=id)
        order.delete()
        return Response(status=status.HTTP_200_OK)


# Purchase Order with Filter API Endpoint Class Based View
class Purchase_filter(APIView):
    # getting all Purchase Orders associated with a vendor id
    def get(self, request, v_id):
        orders = PurchaseOrderModel.objects.filter(vendor=v_id)
        serializer = PurchaseSerializer(orders, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


# Purchase Order Acknowledgement API Endpoint Class Based View
class Purchase_Acknowledgement(APIView):
    def post(self, request, id, format="JSON"):
        order = PurchaseOrderModel.objects.get(pk=id)

        # setting the time the purchase order was acknowledged
        order.acknowledgement_date = datetime.now(tz=pytz.utc)
        serializer = PurchaseSerializer(order)

        # getting the Associated Vendor Instance to update it metrics
        vendor = VendorModel.objects.get(vendor_code=serializer.data["vendor"])

        # checking if the purchase order has been acknowleded before
        # and updating the average_response_time on the vendor instance
        if (
            serializer.data["acknowledgement_date"] != ""
            and serializer.data["acknowledgement_date"] is not None
        ):
            vendor.average_response_time = (
                # convering time difference into hours
                vendor.average_response_time * (vendor.num_orders - 1)
                + (
                    serializer.data["acknowledgement_date"]
                    - serializer.data["issue_date"]
                ).seconds
                / 3600
            ) / vendor.num_orders

            # updating the historical record of the vendor
            PerformanceModel(
                vendor=vendor,
                date=datetime.now(tz=pytz.utc),
                on_time_delivery_rate=vendor.on_time_delivery_rate,
                quality_rating_avg=vendor.quality_rating_avg,
                average_response_time=vendor.average_response_time,
                fulfillment_rate=vendor.fulfillment_rate,
            ).save()
            # saving the vendor Instance
            vendor.save()
            # saving the Purchase Order Instance
            order.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(
                {"Error": "Already Acknowledged"}, status=status.HTTP_400_BAD_REQUEST
            )
