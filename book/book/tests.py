import json
from datetime import datetime
from webbrowser import get
from django.urls import reverse
from django.test import TestCase
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

    def test_user_can_get_all_category(self):
        response = self.client.get(reverse('category-list'))

        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_can_get_all_category(self):
        response = self.anonymous_client.get(reverse('category-list'))

        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_create_category(self):
        response = self.client.post(reverse('category-list'), data=json.dumps(self.category_payload), content_type='application/json')
        
        self.assertTrue(Category.objects.get(category=self.category_payload['category']))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_anonymous_cannot_create_category(self):
        response = self.anonymous_client.post(reverse('category-list'), data=json.dumps(self.category_payload), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_get_category(self):
        response = self.client.get(reverse('category-detail', kwargs={'pk': self.category.pk}))

        category = Category.objects.get(pk=self.category.pk)
        serializer = CategorySerializer(category)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_can_get_category(self):
        response = self.anonymous_client.get(reverse('category-detail', kwargs={'pk': self.category.pk}))

        category = Category.objects.get(pk=self.category.pk)
        serializer = CategorySerializer(category)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_update_category(self):
        response = self.client.put(reverse('category-detail', kwargs={'pk': self.category.pk}), data=json.dumps(self.update_category_payload), content_type='application/json')

        category = Category.objects.get(pk=self.category.pk)
        serializer = CategorySerializer(category)

        self.assertEqual(response.data['category'], serializer.data['category'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_update_category(self):
        response = self.anonymous_client.put(reverse('category-detail', kwargs={'pk': self.category.pk}), data=json.dumps(self.update_category_payload), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_delete_category(self):
        response = self.client.delete(reverse('category-detail', kwargs={'pk': self.category.pk}))

        self.assertEqual(Category.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_anonymout_cannot_delete_category(self):
        response = self.anonymous_client.delete(reverse('category-detail', kwargs={'pk': self.category.pk}))

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

    def test_user_can_get_all_company(self):
        response = self.client.get(reverse('company-list'))

        company = Company.objects.all()
        serializer = CompanySerializer(company, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_can_get_all_company(self):
        response = self.anonmous_client.get(reverse('company-list'))

        company = Company.objects.all()
        serializer = CompanySerializer(company, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_create_company(self):
        response = self.client.post(reverse('company-list'), data=json.dumps(self.company_payload), content_type='application/json')

        self.assertTrue(Company.objects.get(company=self.company_payload['company']))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_anonymous_cannot_create_company(self):
        response = self.anonmous_client.post(reverse('company-list'), data=json.dumps(self.company_payload), content_type='application/json')

        self.assertFalse(Company.objects.filter(company=self.company_payload['company']))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_get_company(self):
        response = self.client.get(reverse('company-detail', kwargs={'pk': self.company.pk}))

        self.assertEqual(response.data['company'], self.company.company)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_can_get_company(self):
        response = self.anonmous_client.get(reverse('company-detail', kwargs={'pk': self.company.pk}))

        self.assertEqual(response.data['company'], self.company.company)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_can_update_company(self):
        response = self.client.put(reverse('company-detail', kwargs={'pk': self.company.pk}), data=json.dumps(self.update_company_payload), content_type='application/json')

        company = Company.objects.get(pk=self.company.pk)
        serializer = CompanySerializer(company)

        self.assertEqual(response.data['company'], serializer.data['company'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_connot_update_company(self):
        response = self.anonmous_client.put(reverse('company-detail', kwargs={'pk': self.company.pk}), data=json.dumps(self.company.pk), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_client_can_delete_company(self):
        response = self.client.delete(reverse('company-detail', kwargs={'pk': self.company.pk}))

        self.assertFalse(Company.objects.filter(pk=self.company.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_anonymous_cannot_delete_company(self):
        response = self.anonmous_client.delete(reverse('company-detail', kwargs={'pk': self.company.pk}))

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

    def test_user_can_get_all_book(self):
        response = self.client.get(reverse('book-list'))

        book = Book.objects.all()
        serializer = BookSerializer(book, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_can_get_all_book(self):
        response = self.anonymous_client.get(reverse('book-list'))

        book = Book.objects.all()
        serializer = BookSerializer(book, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_create_book(self):
        response = self.client.post(reverse('book-list'), data=json.dumps(self.book_payload), content_type='application/json')

        self.assertTrue(Book.objects.get(title=self.book_payload['title']))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_anonymous_cannot_create_book(self):
        response = self.anonymous_client.post(reverse('book-list'), data=json.dumps(self.book_payload), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_get_book(self):
        response = self.client.get(reverse('book-detail', kwargs={'pk': self.book.pk}))

        book = Book.objects.get(title=self.book.title)
        serializer = BookSerializer(book)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_can_get_book(self):
        response = self.anonymous_client.get(reverse('book-detail', kwargs={'pk': self.book.pk}))

        book = Book.objects.get(title=self.book.title)
        serializer = BookSerializer(book)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_update_book(self):
        response = self.client.put(reverse('book-detail', kwargs={'pk': self.book.pk}), data=json.dumps(self.update_book_payload), content_type='application/json')

        self.assertEqual(response.data['title'], 'test-change')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_update_book(self):
        response = self.anonymous_client.put(reverse('book-detail', kwargs={'pk': self.book.pk}), data=json.dumps(self.update_book_payload), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_client_can_delete_book(self):
        response = self.client.delete(reverse('book-detail', kwargs={'pk': self.book.pk}))


        self.assertFalse(Book.objects.filter(pk=self.book.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_anonymous_cannot_delete_book(self):
        response = self.anonymous_client.delete(reverse('book-detail', kwargs={'pk': self.book.pk}))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)