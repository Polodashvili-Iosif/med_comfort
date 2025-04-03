import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
@pytest.mark.parametrize("url,template", [
    ("/non-existent-url/", '404.html'),
    (
        reverse(
            'services:category_detail',
            kwargs={'slug': 'non-existent-category'}
        ),
        'services/404_category.html'),
    (
        reverse(
            'services:service_detail',
            kwargs={'slug': 'non-existent-service'}
        ),
        'services/404_services.html'),
])
def test_404_error_templates(client, url, template):
    response = client.get(url)
    assert response.status_code == 404
    assertTemplateUsed(response, template)
