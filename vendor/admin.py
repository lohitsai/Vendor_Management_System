from django.contrib import admin
from .models import PerformanceModel, VendorModel

# Register your models here.
admin.site.register(PerformanceModel)
admin.site.register(VendorModel)
