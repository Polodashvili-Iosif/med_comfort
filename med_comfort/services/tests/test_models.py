import pytest


@pytest.mark.django_db
class TestServiceCategoryModel:
    def test_service_category_str(self, load_service_data, first_category):
        assert str(first_category) == first_category.name


@pytest.mark.django_db
class TestServiceModel:
    def test_service_str(self, load_service_data, first_service):
        assert str(first_service) == first_service.name
