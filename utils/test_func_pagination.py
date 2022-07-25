import math


def make_pagination_range(page_range, qty_pages, current_page):
    middle_page = math.ceil(qty_pages / 2)
    start_range = current_page - middle_page
    start_range_offset = abs(start_range) if start_range < 0 else 0
    stop_range = current_page + middle_page + start_range_offset

    if start_range < 0:
        start_range = 0

    return page_range[start_range:stop_range]
