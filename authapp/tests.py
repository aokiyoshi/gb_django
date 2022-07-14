from django.test import TestCase
from django.test.client import Client
from authapp.models import ShopUser
from django.core.management import call_command


# Create your tests here.
class TestUserManagement(TestCase):
    def setUp(self):
        self.client = Client()
        call_command('flush', '--noinput')

        self.superuser = ShopUser.objects.create_superuser(
                'django_2',
                'django2@geekshop.local', 
                'geekbrains')

        self.user = ShopUser.objects.create_user(
                'tarantino',
                'tarantino@geekshop.local', 
                'geekbrains')

    def test_super_user_login(self):
        self.client.login(username='django_2', password='geekbrains')
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.superuser)
    
    def test_user_login(self):
        self.client.login(username='tarantino', password='geekbrains') 
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.user)

    
    def test_user_logout(self):
        response = self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, 302)
        # главная после выхода
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

    def test_basket_login_redirect(self):
        response = self.client.get('/basket/')
        print(f'{response.url=}')
        self.assertEqual(response.url, '/auth/login/?next=/basket/')
        self.assertEqual(response.status_code, 302)
