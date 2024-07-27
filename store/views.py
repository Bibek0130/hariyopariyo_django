from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
import json 
from datetime import datetime
from django.contrib.auth import login, authenticate, logout
from .forms import  CustomAuthenticationForm, CustomUserCreationForm

#llogin and signup
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            print(user)
            user.save()
            #login(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                #login(request, user)
                return redirect('products')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def logout(request):
    logout(request)
    return redirect('products')


from .utils import cookieCart, cartData, guestOrder
# Create your views here.
def store(request):
    context={}
    return render(request, 'store/store.html',context)

def cart(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

#to  fix csrf 403 error while usingg incognito mode or when a user loggs in for the first time.
#here, we import csrf_exempt 
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def checkout(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def main(request):
    context= {}
    return render(request, 'store/main.html',context)

def features(request):
    context = {}
    return render(request, 'store/features.html', context)

def products(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems,'items':items, 'order':order} 
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
   
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    product = Product.objects.get(id=productId)
    # reason we are using get_or_create beacuse we want to add to it and modify it.
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    
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
        
        
    else:
        customer, order  = guestOrder(request, data)
    
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    
    
    #conformation to see if the data has been manipulated from frontend or not
    if total == float(order.get_cart_total):
        order.complete = True
    order.save()  
    
    if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
            )
    
    return JsonResponse('Payment Submitted...', safe=False )


#account
def account(request):
    
    login(request)
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                #login(request, user)
                return redirect('home')
    else:
        form = CustomAuthenticationForm()
    logout(request)
    return render(request, 'store/account.html', {'form': form})
  