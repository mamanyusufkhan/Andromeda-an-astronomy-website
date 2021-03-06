import json
from django.shortcuts import render
from .models import *
from .utils import cookieCart, cartData
from django.http import JsonResponse
import datetime

# Create your views here.
def store(request):
    data = cartData(request)       
    items = data['items']

    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store\store.html', context)

def cart(request):

    data = cartData(request)       
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)       
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else: 
        print("User not logged in")
        name = data['form']['name']
        email = data['form']['email']

        cookieData = cookieCart(request)
        items = cookieData['items']

        customer, created = Customer.objects.get_or_create(
            email=email,

        )

        customer.name = name
        customer.save()

        order = Order.objects.create(
            customer=customer,
            complete=False,
        )

        for item in items:
            product = Product.objects.get(id=item['product']['id'])
            orderItem = OrderItem.objects.create(
                product=product,
                order=order,
                quantity=item['quantity']
    
            )
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            zipcode = data['shipping']['zipcode']
        )


    return JsonResponse('Payment complete!', safe=False)