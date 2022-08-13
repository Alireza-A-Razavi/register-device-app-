from statistics import mode
from django.contrib import admin
from . import models

class UserAppPermissionsTabularInline(admin.TabularInline):
    model = models.UserAppPermission

class UserProductPermissionsTabularInLine(admin.TabularInline):
    model = models.UserProductPermission


class UserModelAdmin(admin.ModelAdmin):
    model = models.User
    inlines = [
        UserAppPermissionsTabularInline,
        UserProductPermissionsTabularInLine,
    ]

admin.site.register(models.User, UserModelAdmin)