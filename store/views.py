from django.shortcuts import render

# Create your views here.
def store(request):
    context = {}
    return render(request, 'store/store.html',context)

def cart(request):
    context = {}
    return render(request, 'store/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)

def main(request):
    context= {}
    return render(request, 'store/main.html',context)

def features(request):
    context = {}
    return render(request, 'store/features.html', context)

# def products(request):
#     context = {}
#     return render(request, 'store/products.html', context)

def categories(request):
    context = {}
    return render(request, 'store/categories.html', context)
    
