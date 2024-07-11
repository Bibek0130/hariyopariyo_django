import json
from .models import *
from .views import *

# def cookieCart(request):
#     try:
#         cart = json.loads(request.COOKIES['cart'])
#     except:
#         cart = {}
#         print('Cart: ',cart)
        
#         items = [] #to break loop
#         order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
#         cartItems = order['get_cart_items']
        
#         for i in cart:
#             #we use try block to prevent items in cart that may have been removed from causing 
#             try:
#                 cartItems += cart[i]['quantity']
                
#                 product = Product.objects.get(id=i)
#                 total = (product.price) * cart[i]['quantity']
                
#                 order['get_cart_total'] += total
#                 order['get_cart_items'] += cart[i]['quantity']
                
#                 item = {
#                     'product' : {
#                         'id':product.id,
#                         'name':product.name,
#                         'price':product.price,
#                         'imageURL':product.imageURL
#                     },
#                     'quantity':cart[i]['quantity'],
#                     'get_total':total,
#                 }
#                 items.append(item)
                
#                 if product.digital == 'False':
#                     order['shipping'] = True
#             except:
#                 pass
#         return {'CartItems':cartItems, 'order':order, 'items':items}

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES.get('cart', '{}'))
    except json.JSONDecodeError:
        cart = {}
        print('Cart: ', cart)
    
    items = []  # To break loop
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']
    
    for i in cart:
        try:
            cartItems += cart[i]['quantity']
            
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
            
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']
            
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }
            items.append(item)
            
            if product.digital == False:
                order['shipping'] = True
        except Product.DoesNotExist:
            pass
    
    return {'cartItems': cartItems, 'order': order, 'items': items}

def cartData(request):
    if  request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData.get('cartItems', 0)
        order = cookieData.get('order', {})
        items = cookieData.get('items',[])
    return{'items':items, 'order':order, 'cartItems':cartItems}
 
def guestOrder(request, data):
    print('User is not logged in')
        
    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
    
    cookieData = cookieCart(request)
    items = cookieData['items']
    
    customer, created = Customer.objects.get_or_create(
        email = email,  
    )
    customer.name = name
    customer.save()
    
    order = Order.objects.create(
        customer =customer, 
        complete = False,   
    )
    
    for item in items:
        product = Product.objects.get(id = item['product']['id'])
        
        orderItem = OrderItem.objects.create(
            product = product,
            order = order,
            quantity =item['quantity'],
        )
    return customer, order