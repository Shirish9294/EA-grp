from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
import json
import requests

@login_required
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


@login_required
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


@login_required
def cart_detail(request):


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


    cart = Cart(request)
    for item in cart:
            item['update_quantity_form'] = CartAddProductForm(
                              initial={'quantity': item['quantity'],
                              'update': True})
    return render(request, 'cart/detail.html', {'cart': cart,
                                                'exrate': exrate,
                                                'currencycode': currencycode})
