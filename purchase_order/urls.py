from django.urls import path, include
from .views import *

urlpatterns = [
    path("api/purchase_orders/", Purchases.as_view()),
    path("api/purchase_orders/<str:id>/", Purchase.as_view()),
    path("api/purchase_orders/vendor/<str:v_id>/", Purchase_filter.as_view()),
    path(
        "api/purchase_orders/<str:id>/acknowledge/", Purchase_Acknowledgement.as_view()
    ),
]
