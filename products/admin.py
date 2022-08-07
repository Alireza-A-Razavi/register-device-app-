from django.contrib import admin

from .models import (
    Product, 
    PieceOfCode,
    ProductFile,
    ProductPermission,
)

admin.site.register(ProductFile)
admin.site.register(ProductPermission)
admin.site.register(PieceOfCode)


class PieceOfCodeTabularInline(admin.TabularInline):
    model = Product.codes.through

class ProductFileTabularInline(admin.TabularInline):
    model = Product.files.through

class ProductPermissionTabularInline(admin.TabularInline):
    model = Product.permissions.through

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ("name", "wp_product_id",)
    inlines = [
        PieceOfCodeTabularInline,
        ProductFileTabularInline,
        ProductPermissionTabularInline,
    ]
    search_fields = ("wp_product_id", "name",)