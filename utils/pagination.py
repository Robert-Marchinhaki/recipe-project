import math

from django.core.paginator import Paginator


def make_pagination_range(page_range, qty_pages, current_page):
    middle_page = math.ceil(qty_pages / 2)
    start_range = current_page - middle_page
    start_range_offset = abs(start_range) if start_range < 0 else 0
    stop_range = current_page + middle_page
    final_page = len(page_range)
    small_range = final_page > 4
    if final_page < qty_pages:
        start_range = 0
    else:
        if start_range < 0:
            start_range = 0
            stop_range += start_range_offset
        if stop_range >= final_page:
            start_range = abs(abs(start_range) - abs(final_page - stop_range))

    pagination = page_range[start_range:stop_range] if small_range else page_range
    return {
        'pagination': pagination,
        'page_range': page_range,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'total_pages': final_page,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': current_page >= (qty_pages) and small_range,  # noqa: E501
        'first_page_active_span': current_page >= (qty_pages + 1) and small_range,  # noqa: E501
        'last_page_out_of_range': stop_range < final_page and small_range,
        'last_page_active_span': stop_range < final_page - 1 and small_range,
    }


def make_pagination(request, queryset, per_page, qty_page=3):
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


if __name__ == '__main__':
    print('Code here')
    pagination = make_pagination_range(
        page_range=list(range(1, 4)),
        qty_pages=3,
        current_page=0
    )
    pass
