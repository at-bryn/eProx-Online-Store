from django.contrib.auth.models import User
from django.db import models



# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, null = True, blank = True)
    name = models.CharField(max_length= 200, null = True)
    phone = models.CharField(max_length= 200, null = True)
    email = models.CharField(max_length= 200, null = True)
    date_created = models.DateTimeField(auto_now_add = True, null = True)
    business = models.ForeignKey('Business', on_delete=models.CASCADE, null= True)
    def __str__(self):
        return self.name
    
# Each product must belong to a category and the category table of the database only takes the category name.
class Category(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
         return self.name


# This is a database table that stores business details when the business is being registered.
    #Each business must provide the details listed below.
class Business(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, null = True, blank = True)
    name= models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    email = models.EmailField()
    contacts=models.CharField(max_length=20)

    description=models.TextField(max_length =500)
    logo = models.ImageField(upload_to='business_logos/', blank=True, null=True)#Only the logo is optional.


#This is what shows in the database. The name and the location.
    def __str__(self):
        return self.name + "-- " + self.location


# This a database table  called Product that stores product details as listed below.
#     A product must have all the details below and not miss out any. 
    
class Product(models.Model):
    name= models.CharField(max_length=100)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null = True, blank = True)
    price= models.FloatField(null = True)
    category= models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    digital = models.BooleanField(default = False, null = True, blank= False)
    picture= models.ImageField(upload_to='uploads/product/',default=1)
    description= models.TextField(max_length =500)
    upload_date = models.DateField(auto_now_add=True) 

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.picture.url
        except:
            url = ''
        return url

    

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, null= True, on_delete = models.SET_NULL, blank = True)
    # order = models.ForeignKey(Order, null= True, on_delete = models.SET_NULL)
    address = models.CharField(max_length = 100 ,null = True)
    city = models.CharField(max_length = 100 ,null = True)
    state = models.CharField(max_length = 100 ,null = True)
    zipcode = models.CharField(max_length = 100 ,null = True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(null=True, max_length=50)
    email = models.CharField(null=True, max_length=50)
    Company = models.CharField(null=True, max_length=50)
    bio = models.TextField(User, null=True, max_length=50)
    birthday = models.CharField(null= True, max_length=50)
    country = models.CharField(null = True, max_length=50)
    phone = models.CharField(null= True, max_length=50)
    images = models.ImageField(default='default.jpg', upload_to='profile_pics/',null= True)
    website = models.CharField(max_length=50,null=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    # def save(self):
    #     super().save()
    #     img = Image.open(self.images.path)

    #     if img.height >300 or img.width > 300:
    #         output_size = (300,300)
    #         img.thumbnail(output_size)
    #         img.thumbnail(self.images.path)s





    



