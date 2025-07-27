import django_filters
from .models import Message
from django.contrib.auth import get_user_model

class MessageFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="timestamp", lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name="timestamp", lookup_expr='lte')
    sender = django_filters.ModelChoiceFilter(queryset=get_user_model().objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'start_date', 'end_date']
