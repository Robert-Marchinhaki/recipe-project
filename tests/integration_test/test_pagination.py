from unittest import TestCase
import pytest
from utils.test_func_pagination import make_pagination_range


@pytest.mark.fast
class PaginationTest(TestCase):
    def test_pagination_range_return_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):  # noqa: E501
        # current_page = 1 - qty_page = 2 - middle_page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)
        # current_page = 2 - qty_page = 2 - middle_page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)
        # current_page = 3 - qty_page = 2 - middle_page = 2
        # here the range has to change
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3
        )['pagination']
        self.assertEqual([2, 3, 4, 5], pagination)

    def test_make_sure_middle_range_are_correct(self):
        # current_page = 10 - qty_page = 2 - middle_page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=10
        )['pagination']
        self.assertEqual([9, 10, 11, 12], pagination)

        # current_page = 15 - qty_page = 2 - middle_page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=15
        )['pagination']
        self.assertEqual([14, 15, 16, 17], pagination)

        # current_page = 20 - qty_page = 2 - middle_page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=18
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

    def test_make_pagination_is_static_when_last_page_is_next(self):

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=19
        )['pagination']
        self.assertEqual(
            [17, 18, 19, 20],
            pagination,
            msg='current_page = 19 - qty_page = 4 - middle_page = 2')

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=20
        )['pagination']
        self.assertEqual(
            [17, 18, 19, 20],
            pagination,
            msg='current_page = 20 - qty_page = 4 - middle_page = 2')

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=21
        )['pagination']
        self.assertEqual(
            [17, 18, 19, 20],
            pagination,
            msg='current_page = 21 - qty_page = 4 - middle_page = 2')
