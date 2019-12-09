def paginate(data, page, page_size=10):
    new_dict = dict()
    for k, v in data.items():
        slice_ = range(page_size*(page-1), page_size*page)
        new_dict[k] = {new_idx: v[val] for new_idx, val in enumerate(slice_)}

    return new_dict
