from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from datetime import datetime
import pytz


# Purchase Order API Endpoint Class Based View
class Purchase(APIView):
    # creating a new Purchase Order
    def post(self, request):
        serializer = PurchaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # getting all Purchase Orders
    def get(self, request):
        orders = PurchaseOrderModel.objects.all()
        serializer = PurchaseSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # getting a single Purchase Order using the Purchase Order id
    def get(self, request, id):
        order = PurchaseOrderModel.objects.get(id)
        serializer = PurchaseSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # updating a single Purchase Order data using the Purchase Order id
    def put(self, request, id):
        order = PurchaseOrderModel.objects.get(id)
        serializer = PurchaseSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # deleting a single Purchase Order using the Purchase Order id
    def delete(self, request, id):
        order = PurchaseOrderModel.objects.get(id)
        order.delete()
        return Response(status=status.HTTP_200_OK)


# Purchase Order with Filter API Endpoint Class Based View
class Purchase_filter(APIView):
    # getting all Purchase Orders associated with a vendor id
    def get(self, request, v_id):
        orders = PurchaseOrderModel.objects.filter(vendor=v_id)
        serializer = PurchaseSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Purchase Order Acknowledgement API Endpoint Class Based View
class Purchase_Acknowledgement(APIView):
    def post(self, request, id):
        order = PurchaseOrderModel.objects.get(id)
        order.acknowledgement_date = datetime.now(tz=pytz.utc)
        order.save()
