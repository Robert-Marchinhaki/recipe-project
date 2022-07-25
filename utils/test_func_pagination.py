import math


def make_pagination_range(page_range, qty_pages, current_page):
    middle_page = math.ceil(qty_pages / 2)
    start_range = current_page - middle_page
    start_range_offset = abs(start_range) if start_range < 0 else 0
    stop_range = current_page + middle_page + start_range_offset
    final_page = len(page_range)
    if start_range < 0:
        start_range = 0
    if (start_range + (middle_page+1)) >= final_page:
        start_range = final_page - qty_pages
    pagination = page_range[start_range:stop_range]
    return {
        'pagination': pagination,
        'page_range': page_range,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'total_pages': final_page,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': current_page > middle_page,
        'last_page_out_of_range': stop_range < final_page,
    }
