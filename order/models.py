from django.db import models
from eProx.models import *

class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='checkouts')
    first_name = models.CharField(max_length=50, null= True)
    last_name = models.CharField(max_length=50, null= True)
    email = models.EmailField(null= True)
    address = models.CharField(max_length=250,null= True)
    created = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, null= True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        total_cost = 0
        for item in self.items.all():
            total_cost += item.product.price * item.quantity
        return total_cost

class Order(models.Model):
    status_choices = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Delivered', 'Delivered'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True, null=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    status = models.CharField(max_length=20, choices=status_choices, default='Pending')
    checkout = models.ForeignKey(Checkout, related_name='orders', on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through='OrderedProducts')

    class Meta:
        ordering = ['-date_ordered']
    # def __str__(self):
    #     return f"Order {self.id} by {self.customer}"
    def save(self, *args, **kwargs):
        if not self.checkout:
            self.checkout = Checkout.objects.create()
        super().save(*args, **kwargs)

    def get_ordered_products(self):
        return self.orderedproducts_set.all()

    def get_cart_items_count(self):
        return sum(item.quantity for item in self.get_ordered_products())

    def get_cart_total(self):
        return sum(item.get_total() for item in self.get_ordered_products())

    def __str__(self):
        return f'{self.customer.name} - Order No. {self.id}'

    @property
    def get_ordered_products(self):
        return self.checkout.items.all()

        
    @property
    def get_cart_total(self):
       orderitems = self.orderitem_set.all()
       total = sum([item.get_total for item in orderitems])
       return total

    @property
    def get_cart_items(self):
       orderitems = self.orderitem_set.all()
       total_items = sum(item.get_quantity for item in orderitems)
       return total_items

class OrderedProducts(models.Model):
    orders = models.ForeignKey(Order, on_delete=models.CASCADE, null = True)
    order = models.ForeignKey(Checkout, related_name='items', on_delete=models.CASCADE, null= True)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, null = True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = (('order', 'product'),)

    def __str__(self):
        return  str(self.product) +  str(' order No. ')+ str(self.id) 
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    @property
    def get_quantity(self):
        total_quantity = self.quantity
        return total_quantity
    
    def get_cost(self):
        return self.price * self.quantity