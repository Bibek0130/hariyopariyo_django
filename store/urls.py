from django.urls import path
from . import views

urlpatterns = [
    #leave as empty string for base url
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('main/', views.main, name="main"),
    path('features/', views.features, name="features" )
]