from decimal import Decimal

PRODUCT_VARIANTS_PRICES_ARGNAMES = [
    'expected_min_price',
    'expected_first_price',
    'expected_second_price',
]
PRODUCT_VARIANTS_PRICES_ARGVALUES = [
    (Decimal('13'), Decimal('15'), Decimal('48')),
    (Decimal('4'), Decimal('150'), Decimal('3256')),
    (Decimal('7'), Decimal('216'), Decimal('8')),
    (Decimal('19'), Decimal('29'), Decimal('48')),
    (Decimal('125'), Decimal('361'), Decimal('994')),
    (Decimal('255'), Decimal('301'), Decimal('5882')),
    (Decimal('1255'), Decimal('6891'), Decimal('8300')),
    (Decimal('3952'), Decimal('3999'), Decimal('4941')),
]
