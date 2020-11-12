import math

from decouple import config
from django.conf import settings
from django.core.paginator import EmptyPage, Paginator
from django.http import HttpResponseForbidden
from django.views.decorators.cache import cache_page
from jwt import InvalidSignatureError, DecodeError
from login.jwtlogin import unpack_jwt


class PaginatorMixin:
    PAGE_SIZE = None

    def get_n_pages(self, data):
        return math.ceil(len(data)/self.PAGE_SIZE)

    def paginate(self, model_response, page, page_size):
        paginator = Paginator(model_response, page_size)
        try:
            page_data = paginator.page(page).object_list
        except EmptyPage:
            page_data = []

        return page_data


class CacheMixin:
    cache_timeout = None
    cache_config = None

    def __getattr__(self, key):
        if key != "cache_key":
            raise AttributeError

        class_name = self.__class__.__name__
        return ''.join(
            [f'_{l.lower()}' if l.isupper() and i else l.lower()
             for i, l in enumerate(class_name)]
        )

    def get_timeout(self):
        timeout = settings.CACHE_TIMEOUT
        if self.cache_timeout is not None:
            return self.cache_timeout

        if self.cache_config is not None:
            timeout = config(
                self.cache_config,
                cast=int,
                default=settings.CACHE_TIMEOUT
            )

        return timeout

    def dispatch(self, request, *args, **kwargs):
        return cache_page(
            self.get_timeout(),
            key_prefix=self.cache_key
        )(super().dispatch)(request, *args, **kwargs)


class JWTAuthMixin:
    orgao_url_kwarg = "orgao_id"

    def authorize_user_in_orgao(self, token_payload, *args, **kwargs):
        # TODO: nos deveríamos aceitar POST de um admin para qualquer órgão?
        is_admin = token_payload.get("tipo_permissao", "regular") == "admin"
        orgaos_validos = token_payload.get("ids_orgaos_lotados_validos", [])
        orgao_payload = token_payload.get("orgao")
        orgao_payload = int(orgao_payload) if orgao_payload else None
        orgaos = (
            [int(o) for o in orgaos_validos]
            + [orgao_payload]
        )
        orgao_url = kwargs.get(self.orgao_url_kwarg)
        orgao_url = int(orgao_url) if orgao_url else orgao_url
        return (
            is_admin
            or orgao_url in orgaos
            or not orgao_url
        )

    def dispatch(self, request, *args, **kwargs):
        try:
            self.token_payload = unpack_jwt(request)
            if self.authorize_user_in_orgao(
                self.token_payload,
                *args,
                **kwargs
            ):
                return super().dispatch(request, *args, **kwargs)
            else:
                return HttpResponseForbidden()

        except (InvalidSignatureError, DecodeError):
            return HttpResponseForbidden()
