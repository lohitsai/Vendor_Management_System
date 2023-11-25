from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *


class Vendors(APIView):
    # creating a new vendor
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # getting all vendors
    def get(self, request):
        vendors = VendorModel.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Specific Vendor API Endpoint Class Based View
class Vendor(APIView):
    # getting a single vendor using the vendor id
    def get(self, request, id):
        vendor = VendorModel.objects.get(pk=id)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # updating a single vendor data using the vendor id
    def put(self, request, id):
        vendor = VendorModel.objects.get(pk=id)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # deleting a single vendor using the vendor it
    def delete(self, request, id):
        vendor = VendorModel.objects.get(pk=id)
        vendor.delete()
        return Response(status=status.HTTP_200_OK)


# Historical Performance API Endpoint Class Based View
class Performance(APIView):
    # getting the Historical Performance of a vendor using the vendor id
    # And ordering them Chronologically
    def get(self, request, id):
        vendor_perf = PerformanceModel.objects.filter(vendor=id).order_by("-date")
        serializer = PerformanceSerializer(vendor_perf, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
