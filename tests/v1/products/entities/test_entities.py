import pytest
from slugify import slugify

from src.apps.products.entities.products import ProductEntity


@pytest.mark.parametrize(
    argnames='expected_product_title',
    argvalues=[
        'New IPhone 17 Pro Max, 256GB',
        '8 Silver plates for cooking',
        'Test PrOductName',
        'Hello(1*&(*!@$&)*!&@#+!@#+!_@%)!@%**!&# 94712946^!@%&^  WOrLD!',
        '1927 1239 15826, }{{:":L":>?<~~``',
        '你好世界',
        'こんにちは世界',
        'Selam Dünya',
        'مرحبا بالعالم',
        'Привет, мир',
        'привіт, світ',
        'բարև աշխարհ',
        'გამარჯობა მსოფლიო',
    ],
)
def test_build_entity_slug(expected_product_title: str):
    entity = ProductEntity(seller_id=0, title=expected_product_title)
    expected_slug = f'{slugify(text=entity.title)}-{entity.id[-8:]}'

    entity.build_slug()
    assert expected_slug == entity.slug
