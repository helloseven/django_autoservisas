from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Car, Order

class OrderCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        self.fields['car'].queryset = Car.objects.filter(client=self.request.user)

    class Meta:
        model = Order
        fields = ['car']

