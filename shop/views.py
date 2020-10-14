from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.core.mail import send_mail
from django.views import View
from .forms import ApplicationsForm
import telebot
from django.views.generic import ListView
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

bot = telebot.TeleBot('1116291257:AAFuY9YASfUnBJ6nwwLyvwJiLJykcepzgLI')

def index(request):
    form = ApplicationsForm()
    product = Product.objects.all()
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/index.html',{'product':product,'cart_product_form': cart_product_form })



def shop(request):
    product = Product.objects.all()
    product_list = Product.objects.all()
    cart_product_form = CartAddProductForm()
    page = request.GET.get('page', 1)

    paginator = Paginator(product_list, 6)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {'cart_product_form': cart_product_form, 
                'producent': product,
                'products': products,   
    }
    return render(request, 'shop/shop.html', context)

def contact(request):
    return render(request, 'shop/contact-us.html')

def product_details(request):
    return render(request, 'shop/product-details.html')

def product_affiliate(request):
    return render(request, 'shop/product-details-affiliate.html')

def product_group(request):
    return render(request, 'shop/product-details-group.html')

def product_variable(request):
    return render(request, 'shop/product-details-variable.html')

def cart(request):
    return render(request, 'cart/cart.html')


class ApplicationsView(View):
    def post(self, request):
        if request.method == 'POST':
            form = ApplicationsForm(request.POST)
            # print(request.POST)
        if form.is_valid():
            form.save()
            mail = form.cleaned_data['mail']
            name = form.cleaned_data['name']
            comment = form.cleaned_data['comment']
            subject = 'Новая заявка на подписку!'
            from_email = 'bolotbekovtaalay@gmail.com'
            to_email = ['bolotbekovtaalay@gmail.com']
            message = 'Новая заявка!' + '\r\n' + '\r\n' + 'Почта: ' + mail + '\r\n' + '\r\n' + 'Имя: ' + name + '\r\n' + 'Коммент: ' + comment
            send_mail(subject, message, from_email, to_email, fail_silently=False)
            bot.send_message(449062776, message)
        return redirect('shop:contact')

class SearchResultsView(ListView):
    model = Product
    template_name = 'shop/search_results.html'
    
    def get_queryset(self): # новый
        query = self.request.GET.get('q')
        object_list = Product.objects.filter(Q(name__icontains=query) | Q(category__icontains=query))
        return object_list

