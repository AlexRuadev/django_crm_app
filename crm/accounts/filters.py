import django_filters
from django_filters import DateFilter

from .models import *


class OrderFilter(django_filters.FilterSet):
    # custom attributes
    start_date = DateFilter(field_name='date_created', lookup_expr='gte')
    end_date = DateFilter(field_name='date_created', lookup_expr='lte')

    class Meta:
        # Minimum of 2 attributes
        model = Order
        fields = '__all__'
        # excluding some attributes
        exclude = ['customer', 'date_created']
