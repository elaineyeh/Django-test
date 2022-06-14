from rest_framework import permissions, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from django.contrib.auth.models import User

from book.models import Book, Category, Company
from book.serializers import BookSerializer, CategorySerializer, CompanySerializer, UserSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes_by_action = {
        'create': [AllowAny],
        'list': [IsAdminUser]
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_cation]
        except KeyError:
            return [permission() for permission in self.permission_classes]