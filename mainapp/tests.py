from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post
from .models import Blog

class BlogCreationViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_blog_creation_view_with_valid_data(self):
        response = self.client.post(reverse('utworz_blog'), data={'title': 'Testowy tytuł', 'content': 'Testowa treść'})
        self.assertEqual(response.status_code, 200)  # Oczekiwany kod statusu przekierowania

    def test_example(self):
        self.assertTrue(True)  # Przykładowy test, który zawsze przechodzi

    def test_user(self):
        self.assertEqual(self.user.username, 'testuser')
    def test_szyfrowanie_hasla(self):
        self.assertNotEquals(self.user.password, 'testpassword')
