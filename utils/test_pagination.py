from unittest import TestCase

from utils.test_func_pagination import make_pagination_range


class PaginationTest(TestCase):
    def test_pagination_range_return_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1
        )
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):  # noqa: E501
        # current_page = 1 - qty_page = 2 - middle_page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1
        )
        self.assertEqual([1, 2, 3, 4], pagination)
        # current_page = 2 - qty_page = 2 - middle_page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2
        )
        ...
        self.assertEqual([1, 2, 3, 4], pagination)
        # current_page = 3 - qty_page = 2 - middle_page = 2
        # here the range has to change
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3
        )
        self.assertEqual([2, 3, 4, 5], pagination)
