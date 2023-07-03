from django import forms
from django.db.models import Q
import django_filters
from crispy_forms.helper import FormHelper

from .models import Document


class DocumentFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        label='',
        lookup_expr='icontains',
        method='custom_filter',
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )

    date_added = django_filters.DateTimeFilter(
        field_name='date_added',
        label='',
        lookup_expr='lte',
        widget=forms.DateTimeInput(
            attrs={'type': 'date', 'class': 'form-control'}
            )
        )
    
    is_secret = django_filters.BooleanFilter(
        label='',
        widget=forms.CheckboxInput()
        )
    
    def custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(lead__email__icontains=value) | 
            Q(lead__last_name__icontains=value) | 
            Q(lead__first_name__icontains=value)
        )
    
    class Meta:
        model = Document
        fields = ['title', 'is_secret']

    