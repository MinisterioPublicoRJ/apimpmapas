from math import ceil


def paginate(data, page, page_size=10):
    return data[page_size * (page-1):page_size*page]


def previous_next_page(base_url, page, data_len, page_size):
    last_page = ceil(data_len / page_size)
    first_page = 1
    next_page = page + 1 if (page + 1) * page_size <= data_len else None
    prev_page = page - 1 if (page - 1) > 0 else None

    qs = base_url + '?page=%s'

    links = {
        'self': qs % page,
        'first': qs % first_page,
        'prev': qs % prev_page if prev_page is not None else prev_page,
        'next': qs % next_page if next_page is not None else next_page,
        'last': qs % last_page
    }

    return links
