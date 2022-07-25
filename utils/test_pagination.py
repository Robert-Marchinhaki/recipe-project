from unittest import TestCase
from utils.func_pagination import make_pagination_range


class PaginationTest(TestCase):
    def test_pagination_range_return_a_pagination_range(self):
        pagination = make_pagination_range(
            pagination_list=list(range(1, 21)),
            qty_pages=4,
            current_page=1
        )
        self.assertEqual([1, 2, 3, 4], pagination)
