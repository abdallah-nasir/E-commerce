from django.forms.widgets import CheckboxSelectMultiple
import django_filters
from .models import *

from django import forms

class ColorFilter(django_filters.FilterSet):
    color__name = django_filters.ModelMultipleChoiceFilter(widget=CheckboxSelectMultiple,queryset=Colors.objects.all())
    brand = django_filters.ModelMultipleChoiceFilter(widget=CheckboxSelectMultiple,queryset=Brands.objects.all())
    class Meta:     
        model=Product
        fields=["color","brand"]   
         