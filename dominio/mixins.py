from decouple import config
from django.conf import settings
from django.core.paginator import EmptyPage, Paginator
from django.views.decorators.cache import cache_page


class PaginatorMixin:

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
