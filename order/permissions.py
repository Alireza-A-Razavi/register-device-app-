from rest_framework.permissions import BasePermission

from .models import PaidOrder

class DevicePermission(BasePermission):

    def has_permission(self, request, view):
        order = PaidOrder.objects.get(user=request.user, wp_order_id=id)
        try:
            if request.META["Device-UUID"] == order.device_token.token:
                return True
            else:
                return False
        except KeyError:
            return False