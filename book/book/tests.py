import json
from datetime import datetime
from webbrowser import get
from django.urls import reverse
from django.test import TestCase
from requests import delete
from rest_framework import status
from rest_framework.test import APIClient

from book.models import Book, Category, Company
from book.serializers import BookSerializer, CategorySerializer, CompanySerializer
from django.contrib.auth.models import User


class CategoryTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='super', password='super', email='abc@xyz.com')
        self.client = APIClient()
        self.client.force_authenticate(user=user)

        self.anonymous_client = APIClient()

        self.category = Category.objects.create(category='food')
        self.category_payload = {
            'category': 'exceries',
        }
        self.update_category_payload = {
            'category': 'python'
        }

    def get_categories(self, client):
        response = client.get(reverse('category-list'))

        return response

    def get_categories_serializer(self):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)

        return serializer

    def test_user_can_get_all_category(self):
        response = self.get_categories(self.client)
        serializer = self.get_categories_serializer()

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_can_get_all_category(self):
        response = self.get_categories(self.anonymous_client)
        serializer = self.get_categories_serializer()

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def create_category(self, client):
        response = client.post(reverse('category-list'), data=json.dumps(self.category_payload), content_type='application/json')
        
        return response

    def test_user_can_create_category(self):
        response = self.create_category(self.client)

        self.assertTrue(Category.objects.get(category=self.category_payload['category']))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_anonymous_cannot_create_category(self):
        response = self.create_category(self.anonymous_client)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def get_category(self, client):
        response = client.get(reverse('category-detail', kwargs={'pk': self.category.pk}))

        return response

    def get_category_serializer(self):
        category = Category.objects.get(pk=self.category.pk)
        serializer = CategorySerializer(category)

        return serializer

    def test_user_can_get_category(self):
        response = self.get_category(self.client)
        serializer = self.get_category_serializer()

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_can_get_category(self):
        response = self.get_category(self.anonymous_client)
        serializer = self.get_category_serializer()

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def update_category(self, client):
        response = client.put(reverse('category-detail', kwargs={'pk': self.category.pk}), data=json.dumps(self.update_category_payload), content_type='application/json')

        return response

    def test_user_can_update_category(self):
        response = self.update_category(self.client)
        serializer = self.get_category_serializer()

        self.assertEqual(response.data['category'], serializer.data['category'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_update_category(self):
        response = self.update_category(self.anonymous_client)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def delete_category(self, client):
        response = client.delete(reverse('category-detail', kwargs={'pk': self.category.pk}))

        return response

    def test_user_can_delete_category(self):
        response = self.delete_category(self.client)

        self.assertEqual(Category.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_anonymout_cannot_delete_category(self):
        response = self.delete_category(self.anonymous_client)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CompanyTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='super', password='super', email='abc@xyz.com')
        self.client = APIClient()
        self.client.force_authenticate(user=user)

        self.anonmous_client = APIClient()

        self.company = Company.objects.create(company='test', address='test', phone='1234567890')

        self.company_payload = {
            'company': 'a',
            'address': 'abc',
            'phone': '09876543121',
        }
        self.update_company_payload = {
            'company': 'b',
            'address': 'def',
            'phone': '09876543121',
        }

    def get_companies(self, client):
        response = client.get(reverse('company-list'))

        return response

    def get_companies_serializer(self):
        company = Company.objects.all()
        serializer = CompanySerializer(company, many=True)

        return serializer

    def test_user_can_get_all_company(self):
        response = self.get_companies(self.client)
        serializer = self.get_companies_serializer()

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_can_get_all_company(self):
        response = self.get_companies(self.anonmous_client)
        serializer = self.get_companies_serializer()

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def create_company(self, client):
        response = client.post(reverse('company-list'), data=json.dumps(self.company_payload), content_type='application/json')

        return response

    def test_user_can_create_company(self):
        response = self.create_company(self.client)

        self.assertTrue(Company.objects.get(company=self.company_payload['company']))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_anonymous_cannot_create_company(self):
        response = self.create_company(self.anonmous_client)

        self.assertFalse(Company.objects.filter(company=self.company_payload['company']))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def get_company(self, client):
        response = client.get(reverse('company-detail', kwargs={'pk': self.company.pk}))

        return response

    def test_user_can_get_company(self):
        response = self.get_company(self.client)

        self.assertEqual(response.data['company'], self.company.company)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_can_get_company(self):
        response = self.get_company(self.anonmous_client)

        self.assertEqual(response.data['company'], self.company.company)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def update_company(self, client):
        response = client.put(reverse('company-detail', kwargs={'pk': self.company.pk}), data=json.dumps(self.update_company_payload), content_type='application/json')

        return response

    def get_company_serializer(self):
        company = Company.objects.get(pk=self.company.pk)
        serializer = CompanySerializer(company)

        return serializer

    def test_client_can_update_company(self):
        response = self.update_company(self.client)
        serializer = self.get_company_serializer()

        self.assertEqual(response.data['company'], serializer.data['company'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_connot_update_company(self):
        response = self.update_company(self.anonmous_client)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def delete_company(self, client):
        response = client.delete(reverse('company-detail', kwargs={'pk': self.company.pk}))

        return response

    def test_client_can_delete_company(self):
        response = self.delete_company(self.client)

        self.assertFalse(Company.objects.filter(pk=self.company.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_anonymous_cannot_delete_company(self):
        response = self.delete_company(self.anonmous_client)

        self.assertTrue(Company.objects.get(pk=self.company.pk))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BookTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='super', password='super', email='abc@xyz.com')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.anonymous_client = APIClient()

        self.company = Company.objects.create(company='test', address='test', phone='1234567890')
        self.category = Category.objects.create(category='food')
        self.book = Book.objects.create(title='test', category=self.category, company=self.company, publish_date=datetime.now(), user=self.user)

        self.book_payload = {
            'title': 'test-1',
            'category': self.category.pk,
            'company': self.company.pk,
            'publish_date': datetime.now().isoformat(),
            'user': self.user.pk,
        }

        self.update_book_payload = {
            'title': 'test-change',
            'category': self.category.pk,
            'company': self.company.pk,
            'publish_date': datetime.now().isoformat(),
            'user': self.user.pk,
        }

    def get_books(self, client):
        response = client.get(reverse('book-list'))

        return response

    def get_books_serializer(self):
        book = Book.objects.all()
        serializer = BookSerializer(book, many=True)

        return serializer

    def test_user_can_get_all_book(self):
        response = self.get_books(self.client)
        serializer = self.get_books_serializer()
        
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_can_get_all_book(self):
        response = self.get_books(self.anonymous_client)
        serializer = self.get_books_serializer()

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def create_book(self, client):
        response = client.post(reverse('book-list'), data=json.dumps(self.book_payload), content_type='application/json')

        return response

    def test_user_can_create_book(self):
        response = self.create_book(self.client)

        self.assertTrue(Book.objects.get(title=self.book_payload['title']))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_anonymous_cannot_create_book(self):
        response = self.create_book(self.anonymous_client)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def get_book(self, client):
        response = client.get(reverse('book-detail', kwargs={'pk': self.book.pk}))

        return response

    def get_book_serializer(self):
        book = Book.objects.get(title=self.book.title)
        serializer = BookSerializer(book)

        return serializer

    def test_user_can_get_book(self):
        response = self.get_book(self.client)
        serializer = self.get_book_serializer()
        
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_can_get_book(self):
        response = self.get_book(self.anonymous_client)
        serializer = self.get_book_serializer()

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def update_book(self, client):
        response = client.put(reverse('book-detail', kwargs={'pk': self.book.pk}), data=json.dumps(self.update_book_payload), content_type='application/json')

        return response

    def test_user_can_update_book(self):
        response = self.update_book(self.client)

        self.assertEqual(response.data['title'], 'test-change')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_update_book(self):
        response = self.update_book(self.anonymous_client)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def delete_book(self, client):
        response = client.delete(reverse('book-detail', kwargs={'pk': self.book.pk}))

        return response

    def test_client_can_delete_book(self):
        response = self.delete_book(self.client)

        self.assertFalse(Book.objects.filter(pk=self.book.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_anonymous_cannot_delete_book(self):
        response = self.delete_book(self.anonymous_client)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)