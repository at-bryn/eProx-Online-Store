from django.urls import path
from .import views
from .views import CustomLoginView, CustomLogoutView
#the urls of the app
urlpatterns = [
    path('', views.home, name = "home"),
    path('product/',views.product, name = "product"),
    path('business1/',views.business, name = "business1"),
    path('signup/',views.register, name = "signup"), 
    path('bessreg/',views.register_bss, name = "bssreg"), 
    # path('checkout/',views.checkout, name ="checkout"),
    path('product',views.product, name ="product"),
    
    path('regproduct',views.regproduct, name='regproduct'),
    path('regbusiness',views.regbusiness, name='regbusiness'),
    
    path('search',views.search, name='search'),
    path('category/<str:foo>',views.category, name='category'),
    path('product/<int:pk>',views.productcard, name='productcard'),
    # path('profile_general/',views.profile_general, name='profile_general'),
    # path('profile_recieve/<int:id>',views.profile_receive, name='profile_recieve'),
    
    path('orderstatus/', views.orderstatus, name='orderstatus'),
    path('manage',views.manage, name='manage'),
    path('business',views.business, name='business'),
    path('userinfo',views.customer_info, name='userinfo'),
    path('delete-product/<int:product_id>/',views.delete_product, name='delete_product'),
    path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('edit/', views.edit_business, name='edit_business'),
    
    path('mark_delivered/<int:order_id>/', views.mark_delivered, name='mark_delivered'), 
    path('place/', views.place_order, name='place'),
]
