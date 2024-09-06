from django.test import TestCase
from .models import Book
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

class BookAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.book = Book.objects.create(
            title="Another Book",
            author="Another Author",
            description="Another Description",
            published_date="2023-01-01",
            price=50.50
        )
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

    def test_get_books(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, 200)

    def test_create_book(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'description': 'New Description',
            'published_date': '2023-02-01',
            'price': 30.00
        }
        response = self.client.post('/api/books/', data)
        self.assertEqual(response.status_code, 201)
