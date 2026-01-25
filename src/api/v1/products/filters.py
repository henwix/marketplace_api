import django_filters

from src.apps.products.models.products import Product


class PersonalProductFilter(django_filters.FilterSet):
    is_visible = django_filters.BooleanFilter(label='Is visible')

    class Meta:
        model = Product
        fields = ['is_visible']
