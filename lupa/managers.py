from decouple import config
from django.db import models
from django.db.models import Q
from ordered_model.models import OrderedModelManager


def _get_authorized_roles(permissions):
    from .models import Grupo

    if permissions:
        return Grupo.objects.filter(role__in=permissions)

    return Grupo.objects.filter(role=config('GUEST_ROLE'))


class RoleManager(OrderedModelManager):
    def get_authorized(self, permissions):
        roles = _get_authorized_roles(permissions)

        return self.get_queryset().filter(
            Q(roles_allowed__in=[r.id for r in roles]) |
            Q(roles_allowed=None)
        )


class DadoDetalheManager(OrderedModelManager):
    def get_authorized(self, permissions):
        roles = _get_authorized_roles(permissions)

        return self.get_queryset().filter(
            Q(dado_main__roles_allowed__in=[r.id for r in roles]) |
            Q(dado_main__roles_allowed=None)
        )
