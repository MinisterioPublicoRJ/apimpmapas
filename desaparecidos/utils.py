def paginate(data, page, page_size):
    return {k: v[page_size*(page-1):page_size*page] for k, v in data.items()}
