from rest_framework import permissions

from proxies.login.serializers import SCAPermissionSerializer


class SCARolePermission(permissions.BasePermission):
    message = "Usuário não possui ROLE necessária no SCA"

    def has_permission(self, request, view):
        ser = SCAPermissionSerializer(data=request.GET)
        ser.is_valid(raise_exception=True)

        payload = ser.validated_data["payload"]
        payload_roles = payload.get("roles")
        if not payload_roles:
            return False

        return len(set(payload_roles) & set(view.permission_roles)) > 0
