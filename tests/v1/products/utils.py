from tests.v1.products.factories import ProductModelFactory, ProductVariantModelFactory


def create_test_products_with_variant(products_params: dict, variant_params: dict | None = None) -> None:
    products = ProductModelFactory.create_batch(**products_params)
    for product in products:
        if variant_params:
            ProductVariantModelFactory.create(product=product, **variant_params)
        else:
            ProductVariantModelFactory.create(product=product)
