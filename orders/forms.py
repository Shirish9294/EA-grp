from django import forms
from django.db import transaction
from shop.models import *

from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        # Order.Customer = Customer.objects.get(user=request.user)
        fields = ['first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city']

    # @transaction.atomic
    # def save(self):
    #
    #     Order.save()
