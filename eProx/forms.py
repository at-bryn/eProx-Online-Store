from django.forms import ModelForm
from .models import *
from order.models import *
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



#This is python form that is to register new users in the database.
class SignUpForm(UserCreationForm):
	
	class Meta:
		model = User
		fields = ('username', 'password1', 'password2') 	# username is the username of the new user.
            												#password1 is the first password the user enters.
															# password2 is the confirmation of the first password entered by the user

		        
class BssRegForm(UserCreationForm):
	
	class Meta:
		model = User
		fields = ('username', 'password1', 'password2')    

#The product form is for registering  new products onto the website.
class Productform(ModelForm):
    class Meta:
        model=Product
        fields="__all__"# This extracts all the fields of the product model.
        excludes = 'business'
        

#The business form is for registering  new businesses onto the website.
class Businessform(ModelForm):
    class Meta:
        model = Business
        fields="__all__" # This extracts all the fields of the Buiness model.

class Customerform(ModelForm):
    class Meta:
        model = Customer
        fields="__all__" #         

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        			
                    
class ProfileUserForm(forms.ModelForm):
    class Meta:
            model = Profile
            fields = ['name','Company','bio','birthday','country','phone','email','website']


class BusinessEditForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = "__all__"     
          

        
