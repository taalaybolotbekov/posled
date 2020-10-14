from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 100)]



class CartAddProductForm(forms.Form):
  quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label=('Количество'))
  update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class OrderSendForm(forms.Form):
    name = forms.CharField()
    phone = forms.CharField()
    mail = forms.CharField(required=False)