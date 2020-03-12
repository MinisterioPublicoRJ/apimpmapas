from django.core.paginator import EmptyPage, Paginator


class PaginatorMixin:

    def paginate(self, model_response, page, page_size):
        paginator = Paginator(model_response, page_size)
        try:
            page_data = paginator.page(page).object_list
        except EmptyPage:
            page_data = []

        return page_data
