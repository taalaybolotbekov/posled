from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
import telebot
from .forms import CartAddProductForm , OrderSendForm
from django.views import View



@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm( initial={'quantity': item['quantity'],
                            'update': True})
    return render(request, 'cart/cart.html', {'cart': cart})

def order(request):
    return render(request, 'cart/checkout.html')

def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

bot = telebot.TeleBot('919453059:AAENKg-9F-wLrH6aa0--6xjfggcfYaShCfw')

class OrderSendView(View):
    def post(self, request):
        if request.method == 'POST':
            form = OrderSendForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                phone = form.cleaned_data['phone']
                if form.cleaned_data['mail'] == '':
                    mail = 'Не указана'
                else:
                    mail = form.cleaned_data['mail']
                cart = Cart(request)
                message = 'Поступил новый заказ!\r\n\r\nИмя: ' + name + '\r\nТелефон: ' + phone + '\r\nПочта: ' \
                          + mail + '\r\n\r\nПродукты\r\n\r\n'

                for c in cart:
                    message += 'Название: ' + str(c['product']) + '\r\n'
                    message += 'Цена: ' + str(c['price']) + '\r\n\r\n'
                    message += 'Количество:  ' + str(c['quantity']) + '\r\n\r\n'

                message += 'Общая стоимость: ' + str(cart.get_total_price())

                bot.send_message(449062776, message)
                Cart.clear(cart)
                return redirect('cart:cart_detail')
            return redirect('index')