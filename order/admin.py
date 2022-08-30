from django.contrib import admin

from . import models

@admin.register(models.DeviceToken)
class DeviceTokenModelAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at",)

admin.site.register(models.PaidOrder)
admin.site.register(models.ProductLine)

