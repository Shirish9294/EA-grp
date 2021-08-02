from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, User
from cart.forms import CartAddProductForm
from .forms import *
import requests
import json


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()

    # pull IP to see local currency
    response = requests.get(
        'https://api.getgeoapi.com/v2/ip/check?api_key=6e1e62d64cbc5f6cec2a8cae8dbd34cd38953e6a&format=json')
    geodata = response.json()
    currency = geodata['currency']
    currencycode = currency['code']
    # pass local currency to currency API
    r1string = 'https://api.getgeoapi.com/v2/currency/convert?api_key=6e1e62d64cbc5f6cec2a8cae8dbd34cd38953e6a&from=USD&to='
    r2string = currencycode
    r3string = '&format=json'
    apistring = r1string + r2string + r3string
    response = requests.get(apistring)
    exchangerate = response.json()
    extrate = exchangerate['rates']
    exttrate = extrate[currencycode]
    exrate = exttrate['rate']

    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   'exrate': exrate,
                   'currencycode': currencycode})


# -----------------------------------------------------
def CustomerSignUpView(request):
    model = User
    form_class = CustomerSignUpForm
    form = CustomerSignUpForm
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            is_customer = True
            form.save()
            return redirect('shop:signup_successful')
        else:
            context = {'form': form}
            return render(request, 'registration/signup.html', context)
    else:
        context = {'form': form}
        return render(request, 'registration/signup.html', context)


def signup_successful(request):
    return render(request, 'registration/signup_successful.html', {'shop': signup_successful})


# def login(request):
#     return render(request, 'registration/login.html', {'shop': login})