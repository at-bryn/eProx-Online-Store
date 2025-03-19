from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('create_order',views.create_order,name = 'create'),
    path('create/', views.order_create, name='order_create'),
    path('checkout/',views.checkoutDetails, name= 'checkout'),
    path('checkouted/', views.checkout_view,name='checkouted')
]