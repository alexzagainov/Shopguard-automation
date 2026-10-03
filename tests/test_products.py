import pytest

from tests.base_test import BaseTest


class TestProducts(BaseTest):
    def test_product_details(self):
        self.header.products()
        self.products_page.view_product(0)
        assert self.product_details_page.is_details_visible()

    @pytest.mark.parametrize("search_key,should_find",[
        pytest.param("winter", True, id="winter"),
        pytest.param("top", True, id="top"),
        pytest.param("", True, id="empty - shows all products"),
        pytest.param("to@p", False, id="wrong search"),
    ])
    def test_search(self,search_key,should_find):
        self.header.products()
        self.products_page.search(search_key)
        results = self.products_page.get_products_names()
        if should_find:
            assert len(results) > 0, f"no results for '{search_key}'"
        else:
            assert results == [], f"expected no results for '{search_key}', got {results}"




