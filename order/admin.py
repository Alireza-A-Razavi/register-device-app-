from django.contrib import admin

from . import models

admin.site.register(models.PaidOrder)
admin.site.register(models.ProductLine)
admin.site.register(models.DeviceToken)