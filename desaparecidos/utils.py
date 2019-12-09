def paginate(data, page, page_size):
    return {k: v[:page_size] for k, v in data.items()}
