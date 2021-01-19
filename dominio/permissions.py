from django.conf import settings
from rest_framework.permissions import BasePermission


class PromotorOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        return view.token_payload.get(
            "cargo",
            settings.FUNCIONARIO_CARGO_SIGLA
        ) == settings.PROMOTOR_CARGO_SIGLA
