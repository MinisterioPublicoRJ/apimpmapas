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
    cache_timeout = settings.CACHE_TIMEOUT

    def __getattr__(self, key):
        if key != "cache_key":
            raise AttributeError

        class_name = self.__class__.__name__
        return '{}_key'.format(
            ''.join(
                [f'_{l.lower()}' if l.isupper() and i else l.lower()
                 for i, l in enumerate(class_name)]
            )
        )
