import pytest

from tests.base_test import BaseTest


class TestProducts(BaseTest):
    def test_product_details(self):
        self.header.products()
        self.products_list.view_product(0)
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
        results = self.products_list.get_products_names()
        if should_find:
            assert len(results) > 0, f"no results for '{search_key}'"
        else:
            assert results == [], f"expected no results for '{search_key}', got {results}"

    # Test Case 18
    def test_view_category_products(self):
        assert self.sidebar.is_categories_visible(), "categories are not visible"
        self.sidebar.open_category("Women", "Tops")
        assert self.products_list.get_title() == "Women - Tops Products"
        assert len(self.products_list.get_products_names()) > 0, "no products in category"

        self.sidebar.open_category("Men", "Jeans")
        assert self.products_list.get_title() == "Men - Jeans Products"
        assert len(self.products_list.get_products_names()) > 0, "no products in category"

    # Test Case 19
    def test_view_brand_products(self):
        self.header.products()
        assert self.sidebar.is_brands_visible(), "brands are not visible"
        # the side bar shows how many products each brand has, e.g. "(6) Polo"
        brands = self.sidebar.get_brands()

        for brand in ["Polo", "Madame"]:
            self.sidebar.open_brand(brand)
            assert self.products_list.get_title() == f"Brand - {brand} Products"
            count = len(self.products_list.get_products_names())
            assert count == brands[brand], f"'{brand}' shows {count} products, the side bar says {brands[brand]}"

    # Test Case 21
    def test_add_review_on_product(self):
        self.header.products()
        assert self.products_list.get_title() == "All Products"
        self.products_list.view_product(0)
        assert self.product_details_page.is_write_review_visible(), "'Write Your Review' is not visible"

        self.product_details_page.write_review("Alex", "alex2@gmail.com", "Good quality, fits well")
        assert self.product_details_page.get_review_success_message() == "Thank you for your review."

