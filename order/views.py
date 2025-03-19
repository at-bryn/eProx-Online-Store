from django.shortcuts import render, redirect
# from django.contrib.auth import login as auth_login
from cart.cart import Cart
from .models import *
from .forms import *
from eProx.models import Business, Customer

def create_order(request):
    return render(request, 'order/create.html')
    

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():

            #creating a new user alongside the order
            user = User.objects.create_user(
                email = form.cleaned_data.get('email'),
                name = form.cleaned_data.get('first_name'),
                last_name = form.cleaned_data.get('last_name'),
                password = form.cleaned_data.get('password')
            )
            user.save()
            #update user fields to be used for the next order
            # user.address = form.cleaned_data.get('address')
            # user.postal_code = form.cleaned_data.get('postal_code')
            # user.city = form.cleaned_data.get('city')
            # auth_login(request, user)
            order = form.save()
            
            for item in cart:
                OrderedProducts.objects.create(order=order, product=item['product'],
                                         price=item['price'], quantity=item['quantity'])
            # clear the cart
            cart.clear()
            return render(request, 'order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'order/create.html', {'cart': cart, 'form': form})

def make_order(request):
    #used to create orders for when a user is logged in
    form = CheckoutForm()
    cart = Cart(request)
    customer = request.user.customer
    
    owner = request.user
    checkout = Checkout.objects.create(
            user = owner,
            first_name = request.user.first_name,
            last_name = request.user.last_name,
            email = request.user.email,
            # postal_code = owner.postal_code,
            # city = owner.city
    )
    order = Order.objects.create(customer=customer, checkout=checkout)
    for item in cart:
        OrderedProducts.objects.create(order=order.checkout, product=item['product'],
                                    price=item['price'], quantity=item['quantity'])
    # clear the cart
    cart.clear()
    return render(request, 'order/created.html', {'order': order,'form':form,})

def checkoutDetails(request):
    user = request.user
    if request.method =="POST":
        form= CheckoutForm(request.POST,request.FILES)
        if form.is_valid(): #The business information must be valid for it to be saved in the database
            form.instance.user = user
            form.save()
            return redirect('home')
        else:
            return render(request,'eProx/homepage.html',{'form':form})
    else:           
        return render(request,'order/created.html',{'form':form}) 
    
def checkout_view(request):
    user = request.user
    business = Business.objects.get(user=user)
    orders_with_checkout = Order.objects.filter(checkout__business=business)

    return render(request, 'order/template', {
        'orders_with_checkout': orders_with_checkout,
    })