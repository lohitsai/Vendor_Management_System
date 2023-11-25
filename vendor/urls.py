from django.urls import path, include
from .views import *

urlpatterns = [
    path("api/vendors/", Vendors.as_view()),
    path("api/vendors/<str:id>/", Vendor.as_view()),
    path("api/vendors/<str:id/performance/", Performance.as_view()),
]
