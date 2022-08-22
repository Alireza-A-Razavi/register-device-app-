from rest_framework.permissions import BasePermission

from order.models import DeviceToken

class UserAgentPermission(BasePermission):

    allowed_agents = "PostmanRuntime",

    def has_permission(self, request, view):
        try:
            print(request.META["HTTP_USER_AGENT"])
            if request.META["HTTP_USER_AGENT"]:
                for agent in self.allowed_agents:
                    if agent in request.META["HTTP_USER_AGENT"]:
                        return True
                return False
        except KeyError:
            return False
        # return super().has_permission(request, view)

class DevicePermission(BasePermission):

    def has_permission(self, request, view):
        try:
            if request.data.get("token") and request.data.get("uuid"):
                token = request.data.get("token")
                try:
                    device_token = DeviceToken.objects.get(token=token)
                    if device_token.device_uuid == request.data.get('uuid'):
                        return True
                    else:
                        return False
                except DeviceToken.DoesNotExist:
                    return False
        except KeyError:
            return False