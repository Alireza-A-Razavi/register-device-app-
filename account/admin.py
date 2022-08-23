from statistics import mode
from django.contrib import admin
from . import models

class UserProductPermissionsTabularInLine(admin.TabularInline):
    model = models.UserProductPermission


class UserModelAdmin(admin.ModelAdmin):
    model = models.User
    inlines = [
        UserProductPermissionsTabularInLine,
    ]

admin.site.register(models.User, UserModelAdmin)