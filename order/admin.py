from django.contrib import admin

from . import models

admin.site.register(models.PaidOrder)
admin.site.register(models.DeviceToken)
admin.site.register(models.ManualPermission)
admin.site.register(models.Product)