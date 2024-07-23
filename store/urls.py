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
    path('about/', views.about, name="about"),
    
    
    #update item
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    
    #login form      
    path('register/' ,views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout_view'),
    #path('account/', views.account, name='account'),
]