import django_filters

from src.apps.products.models.products import Product


class GlobalProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Minimum price')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Maximum price')
    price_range = django_filters.RangeFilter(field_name='price', label='Price range')

    class Meta:
        model = Product
        fields = ['min_price', 'max_price', 'price_range']


class PersonalProductFilter(GlobalProductFilter):
    is_visible = django_filters.BooleanFilter(label='Is visible')

    class Meta:
        model = Product
        fields = GlobalProductFilter.Meta.fields + ['is_visible']
