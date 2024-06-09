from django.urls import path
from . import views

urlpatterns = [
    #leave as empty string for base url
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('main/', views.main, name="main"),
    path('features/', views.features, name="features" ),
    path('products/', views.products, name="products"),
    path('categories/', views.categories, name="categories"),
    path('about/', views.about, name="about"),
    
    #update item
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
]