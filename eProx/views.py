from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect
from .models import *
from order.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User,Group
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse
from.forms import *
from django.http import JsonResponse
import json
from .decorators import allowed_users
from django.http import HttpResponse,HttpResponseNotAllowed,HttpResponseNotFound
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from cart.forms import *
from order.views import  make_order


#This is the view for the home page.
def home(request):
    products = Product.objects.all()#This is a query expression in  that retrieves all the objects from the Product table in the database.
    context ={'products':products,}
    return render(request, 'eProx/homepage.html',context)


#This is a view for the product page which shows all products available in the database.
#@allowed_users(allowed_roles=['Customer','Admin'])
def product(request):
    cart_product_form = CartAddProductForm()
    products = Product.objects.all()  #This is a query expression in  that retrieves all the objects from the Product table in the database.
    context ={'products':products,'order':order,'cart_product_form':cart_product_form}
    return render(request,'eProx/product.html',context)



#Each product is assigned a product card for organisation and easy viewing .
def productcard(request,pk):
    cart_product_form = CartAddProductForm()
    product= Product.objects.get(id=pk) 
    context = {'cart_product_form':cart_product_form,'product':product, }
    #This retrieves a specific instance of the Product model from the database based on its primary key used as a product id.
    return render(request,'eProx/productcard.html',context)

    


#@allowed_users(allowed_roles=['Customer','Admin'])
def category(request,foo):
    #just replacing hyphens with spaces...nothing much
    foo = foo.replace('-',' ')
    try:
        category=Category.objects.get(name=foo)
        products= Product.objects.filter(category=category)
        return render(request,'eProx/category.html',{'products':products, 'category':category})
    except:
        return redirect('home')


# This is for product registration.
@login_required(login_url= "login")
@allowed_users(allowed_roles=['Business','Admin'])
def regproduct(request):
    form = Productform()
    current_user=request.user
    user_business=Business.objects.get(user=current_user)

    if request.method == "POST":
        form= Productform(request.POST,request.FILES)
        if form.is_valid():#the product information is only saved in the database if it is valid as per the product model.
            form.instance.business=user_business
            form.save()
            return redirect ('manage')# once the product information is valid and saved in the database,the user is re-directed 
          
        else:
            return render(request,'eProx/productreg.html',{'form':form})
    else:           
        return render(request,'eProx/productreg.html',{'form':form})
    
# The regbusiness view is for registering new businesses.
#@allowed_users(allowed_roles=['Business','Admin'])
def regbusiness(request):
    form = Businessform()
    user = request.user
    if request.method =="POST":
        form= Businessform(request.POST,request.FILES)
        if form.is_valid(): #The business information must be valid for it to be saved in the database
            form.instance.user = user
            form.save()
            return redirect ('business')
        else:
            return render(request,'eProx/regbusiness.html',{'form':form})
    else:           
        return render(request,'eProx/regbusiness.html',{'form':form}) 



# This is the search view
#@allowed_users(allowed_roles=['Customer','Admin'])
def search(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        searched_products = Product.objects.filter(name__icontains=searched)

        if not searched_products:
            messages.info(request, "The product does not exist.")   
            referring_url = request.META.get('HTTP_REFERER')
            if referring_url:
                return HttpResponseRedirect(referring_url)
            else:
                return HttpResponseRedirect(reverse('product'))
        else:
            return render(request, 'eProx/search.html', {'searched': searched_products})
    else:
        return render(request, 'eProx/search.html', {})
      

    
#This logs the current user.
@login_required
def place_order(request):
    return make_order(request)  
    
# this adds items to the cart
# @allowed_users(allowed_roles=['Customer','Admin'])
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    context = {'product': product, 'cart_product_form': cart_product_form}
    return render(request, 'eProx/product.html', context)

# The register view is for signing up new users.
def register(request): 
    form = SignUpForm()
    if request.method =="POST":
        form= SignUpForm(request.POST)
        if form.is_valid(): #The user information must be valid for it to be saved in the database
            new_user=form.save()
            # user = form.instance.user
            Customer.objects.create(
                user=new_user,
                name = new_user.username,
                email = new_user.email,
            )
    
            group = Group.objects.get(name='Customer')
            new_user.groups.add(group) 
     
            username= form.cleaned_data.get('username')   #This extracts the cleaned and validated value of the 'username' field from the form
            password= form.cleaned_data.get('password1')  #This extracts the cleaned and validated value of the 'password1' field from the form
            user = authenticate(request,username=username,password=password)
            if user is not None: #once the user is fully registered and saved in the database, they are now authenticated and logged in
                login(request,user)
                return redirect ('home')
        else: 
            return redirect ('home')
    else:           
        return render(request,'eProx/signup.html',{'form':form})
    


def register_bss(request):
    form = BssRegForm()
    if request.method =="POST":
        form= SignUpForm(request.POST)
        if form.is_valid(): #The business information must be valid for it to be saved in the database
            new_business=form.save()

            group = Group.objects.get(name='Business')
            new_business.groups.add(group)
     
            username= form.cleaned_data.get('username')   #This extracts the cleaned and validated value of the 'username' field from the form
            password= form.cleaned_data.get('password1')  #This extracts the cleaned and validated value of the 'password1' field from the form
            user = authenticate(request,username=username,password=password)
            if user is not None: #once the user is fully registered and saved in the database, they are now authenticated and logged in
                login(request,user)
                return redirect ('regbusiness')
        else: 
            return redirect ('regbusiness')
    else:           
        return render(request,'eProx/bssreg.html',{'form':form})    
        




def order(request, status=None):
    if request.user.is_authenticated:
        customer = request.user.customer
        if status:
            orders = Order.objects.filter(customer=customer, status = status)
        else:
            orders = Order.objects.filter(customer = customer)





# @allowed_users(allowed_roles=['Customer','Admin'])
# def customer_info(request):
#     if request.user.is_authenticated:
#         user = request.user
#         customer = Customer.objects.get(user=user)
#         orders = Checkout.objects.filter(user=user)
#         return render(request, 'eProx/userprofile.html', {'customer': customer, 'orders': orders})
#     else:
#         return render(request, 'eProx/homepage.html')



def mark_delivered(request, order_id):
    if request.method == 'POST':
        order = Order.objects.get(id=order_id)
        order.status = 'Delivered'
        order.save()
    return redirect('userinfo')


# @allowed_users(allowed_roles=['Business', 'Admin'])
# def manage(request):
#     try:
#         business = get_object_or_404(Business, user=request.user)
#         products = Product.objects.filter(business=business)
#         # orders = Order.objects.filter(customer__business__user=request.user)
#         orders = Order.objects.filter(product__in=products).distinct()
#         items= OrderedProducts.objects.all()

#         checkout_info = []
#         for user in orders:
#             checkout_info = Checkout.objects.filter(user=user).first()
#             if checkout_info:
#                 checkout_info.append(checkout_info)




#         return render(request, 'eProx/manage.html', {
#             'products': products,
#             'orders': orders,
#             'items':items
#         })
#     except Business.DoesNotExist:
#         return HttpResponse("Business not found.")
#     except Order.DoesNotExist:
#         return HttpResponse("No orders found.")
#     except Exception as e:
#         return HttpResponse(f"An error occurred: {e}")


@login_required
@allowed_users(allowed_roles=['Business','Admin'])
def edit_business(request):
    business = request.user.business
    if request.method == 'POST':
        form = BusinessEditForm(request.POST, instance=business)
        if form.is_valid():
            # Assign the current user to the user field
            business.user = request.user
            form.save()
            return redirect('business')
    else:
        form = BusinessEditForm(instance=business)
    return render(request, 'eProx/edit_business.html', {'form': form})


# @require_POST
# def update_order_status(request, order_id):
#     order = get_object_or_404(Checkout, id=order_id)
#     order.status = 'Delivered'  # Update the status
#     order.save()
#     return redirect('manage')  # Redirect to the order list page


@allowed_users(allowed_roles=['Business','Admin'])
def delete_product(request, product_id):
    if request.method == 'POST':
        try:
            product = Product.objects.get(pk=product_id)
            product.delete()
            return redirect('manage')  # Redirect to a view that displays the list of products
        except Product.DoesNotExist:
            return HttpResponseNotFound('Product not found')
    else:
        return HttpResponseNotAllowed(['POST'])  # Allow only POST requests
    

@allowed_users(allowed_roles=['Business','Admin'])
def delete_order(request, order_id):
    if request.method == 'POST':
        order = Checkout.objects.filter(id=order_id).first()
        if order:
            order.delete()
            messages.success(request, 'Order deleted successfully.')
        else:
            messages.error(request, 'Order does not exist.')
    else:
        messages.error(request, 'Invalid request method.')

    return redirect('manage')  


def orderstatus(request):
    if request.user.is_authenticated:
        # Get orders for the logged-in user
        orders = Checkout.objects.filter(customer__user=request.user)

        context = {'orders': orders, 'user': request.user}
        return render(request, 'eProx/orderstatus.html', context)
    else:
        # Redirect to the login page or display an error message
        return redirect(request, 'eProx/login.html')

# class CustomLoginView(LoginView):
#     def get_success_url(self):
#         user = self.request.user
#         if user.groups.filter(name='Customer').exists():
#             return reverse_lazy('home')
#         elif user.groups.filter(name='Business').exists():
#             return reverse_lazy('business')
#         else:
#             return reverse_lazy('home')  

class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name='Customer').exists():
            return reverse_lazy('home')
        elif user.groups.filter(name='Business').exists():
            return reverse_lazy('business')
        else:
            return reverse_lazy('home')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')

@allowed_users(allowed_roles=['Business','Admin'])
def business(request):
    user = request.user
    
    # Retrieve the business object related to the current user
    business = Business.objects.get(user=user)
    return render(request, 'eProx/business1.html', {'business_profile': business})


from django.shortcuts import render, get_object_or_404

@allowed_users(allowed_roles=['Business','Admin'])
def manage(request):
    business = get_object_or_404(Business, user=request.user)
    products = Product.objects.filter(business=business)
    # orders = Order.objects.filter(product__in=products)
    # Filter ordered items related to the user's business
    items = OrderedProducts.objects.filter(product__in=products)
    # Filter the checkout information based on the products owned by the business
    checkout_info = Checkout.objects.filter(product__in=products).distinct()
    # checkout_info = []
    # for order in orders:
    #     checkout = Checkout.objects.filter(order=order).first()
    #     if checkout:
    #         checkout_info.append(checkout)

    # Initialize an empty list to store orders
    orders = []

        # Loop through each checkout to retrieve associated orders
    for checkout in checkout_info:
        checkout_orders = Order.objects.filter(checkout=checkout)
        orders.extend(checkout_orders)

    return render(request, 'eProx/manage.html', {
        'products': products,
        'orders': orders,
        'checkout_info': checkout_info,
        'ordered_items': items
    })

@allowed_users(allowed_roles=['Customer','Admin'])
def customer_info(request):
    if request.user.is_authenticated:
        user = request.user
        customer = Customer.objects.get(user=user)
        orders = Order.objects.filter(customer__user=user)
        return render(request, 'eProx/userprofile.html', {'customer': customer, 'orders': orders})
    else:
        return render(request, 'eProx/homepage.html')
    

@require_POST
def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        if new_status == 'Delivered':  # Check if the new status is "Delivered"
            order.status = new_status
            order.save()
    return redirect('manage')