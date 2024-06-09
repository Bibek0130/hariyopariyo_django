from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json 
from datetime import datetime

from .models import *
from .utils import cookieCart
# Create your views here.
def store(request):
    context={}
    return render(request, 'store/store.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
        
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

#to  fix csrf 403 error while usingg incognito mode or when a user loggs in for the first time.
#here, we import csrf_exempt 
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def checkout(request):
    if  request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def main(request):
    context= {}
    return render(request, 'store/main.html',context)

def features(request):
    context = {}
    return render(request, 'store/features.html', context)

def products(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        # order = cookieData['order']
        # items = cookieData['items']
    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems,'items':items}
    return render(request, 'store/products.html', context)

def categories(request):
    context = {}
    return render(request, 'store/categories.html', context)

def about(request):
    context = {}
    return render(request, 'store/About.html', context) 

#merging duplicates and removing extras
def merge_duplicates():
    from store.models import OrderItem

    duplicates = OrderItem.objects.values('order', 'product').annotate(count=models.Count('id')).filter(count__gt=1)

    for duplicate in duplicates:
        items = OrderItem.objects.filter(order=duplicate['order'], product=duplicate['product'])
        main_item = items.first()
        extra_items = items[1:]

        for item in extra_items:
            main_item.quantity += item.quantity
            item.delete()

        main_item.save()

merge_duplicates()
  

#update item view
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    print('Action:', action)
    print('ProductId:', productId)
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    # reason we are using get_or_crate beacuse we want to add to it and modify it.
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)

#creating processorder function
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.load(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        
        #conformation to see if the data has been manipulated from frontend or not
        if total == order.get_cart_total:
            order.complete = True
        order.save()
        
        #adding shipping logic
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
            )
        
    else:
        print('User is not logged in')
    return JsonResponse('Payment Submitted...', safe=False)
    