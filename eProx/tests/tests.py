from django.test import TestCase, SimpleTestCase
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
class HomePageTests(SimpleTestCase):

    def test_home_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

class CartCheckoutLoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_cart_page_access(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart.html')
        self.assertContains(response, 'Your shopping cart')

    def test_empty_cart_checkout(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your cart is empty.')
        self.assertNotContains(response, 'Proceed to checkout')

    def test_add_to_cart(self):
        self.client.login(username='testuser', password='testpassword')
        product_id = 1  # Replace with actual product ID or use fixtures to create test data
        response = self.client.post(reverse('add_to_cart', args=[product_id]))
        self.assertRedirects(response, reverse('cart'))
        # Check if the added product is in the cart
        cart_response = self.client.get(reverse('cart'))
        self.assertContains(cart_response, 'Added Product Name')
    
    def test_login(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertRedirects(response, reverse('home'))  # Assuming 'home' is the name of your home page URL
        self.assertTrue(self.client.session['_auth_user_id'])  # Check if user is logged in
    
    def test_logout(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'))  # Assuming 'home' is the name of your home page URL
        self.assertFalse(self.client.session.get('_auth_user_id'))  # Check if user is logged out
