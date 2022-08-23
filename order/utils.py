from django.contrib.auth import get_user_model


from .models import DeviceToken, PaidOrder

from account.models import  UserProductPermission
from products import ProductType

User = get_user_model()

# def plugin_is_valid(request):
#     device_token = request.META.get("DEVICE-TOKEN")
#     device = DeviceToken.objects.get(token=device_token)
#     for plugin in device.linked_plugins.all():
#         if plugin

def perform_raise_permission(order: PaidOrder, user):
    if order.rose_permission:
        return order, False

    else:
        lines = order.line_items.all()
        for line in lines:
            product = line.item
            permission, created = UserProductPermission.objects.get_or_create(
                user=user,
                product=product,
            )
            permission.allowed_device_count += product.device_count_limit
            permission.save()
        order.rose_permission = True
        order.save()
        return order, True