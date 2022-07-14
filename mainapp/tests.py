from django.test import TestCase
from django.test.client import Client, RequestFactory    
from mainapp.models import Product, ProductCategory
from django.core.management import call_command

class TestMainappSmoke(TestCase):
    
    def setUp(self):
        call_command('flush', '--noinput')
        category = ProductCategory(name='testtest')
        category.save()
        product = Product(category=category, name='test')
        product.save()

    def test_main_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
    
    def test_contacts_page(self):
        response = self.client.get("/contacts/")
        self.assertEqual(response.status_code, 200)
   
    def test_products_page(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        
    def test_category_page(self):
        response = self.client.get("/products/1")
        self.assertEqual(response.status_code, 200)
  
    def test_product_page(self):
        response = self.client.get("/product/1")
        self.assertEqual(response.status_code, 200)
        

class ProductsTestCase(TestCase):
    def setUp(self):
        category = ProductCategory.objects.create(name="стулья")
        self.product_1 = Product.objects.create(
                name="стул 1",
                category=category,
                price = 168.5,
                quantity=15)
        
        self.product_2 = Product.objects.create(name="стул 2",
                    category=category,
                    price=758.45,
                    quantity=45,
                    is_active=False)
        
    def test_product_get(self):
        product_1 = Product.objects.get(name="стул 1")
        product_2 = Product.objects.get(name="стул 2")
        self.assertEqual(product_1, self.product_1)
        self.assertEqual(product_2, self.product_2)
    
    def test_product_print(self):
        product_1 = Product.objects.get(name="стул 1")
        product_2 = Product.objects.get(name="стул 2")
        self.assertEqual(str(product_1), 'стул 1 (стулья)')
        self.assertEqual(str(product_2), 'стул 2 (стулья)')
    

