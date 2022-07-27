import math

from django.core.paginator import Paginator


def make_pagination_range(page_range, qty_pages, current_page):
    middle_page = math.ceil(qty_pages / 2)
    start_range = current_page - middle_page
    start_range_offset = abs(start_range) if start_range < 0 else 0
    stop_range = current_page + middle_page
    final_page = len(page_range)
    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset
    if final_page < stop_range:
        pass  # noqa: E501 this is equal to use start_range = 0, using this to prevent bugs
    elif stop_range >= final_page:
        start_range = start_range - abs(final_page - stop_range)
    pagination = page_range[start_range:stop_range]
    return {
        'pagination': pagination,
        'page_range': page_range,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'total_pages': final_page,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': current_page >= (qty_pages - 1),  # noqa: E501
        'first_page_active_span': current_page >= (qty_pages),  # noqa: E501
        'last_page_out_of_range': stop_range < final_page,
    }


# make_pagination_range(
#     page_range=list(range(1, 4)),
#     qty_pages=4,
#     current_page=1
# )['pagination']


def make_pagination(request, queryset, per_page, qty_page=4):
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1
    pagination = Paginator(queryset, per_page)
    pag_get_page = pagination.get_page(current_page)

    pagination_range = make_pagination_range(
        pagination.page_range,
        qty_page,
        current_page,
    )
    return pag_get_page, pagination_range
