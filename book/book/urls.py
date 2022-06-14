from django.urls import path, include
from rest_framework.routers import DefaultRouter
from book.views import BookViewSet, CategoryViewSet, CompanyViewSet


router = DefaultRouter()
router.register(r'book', BookViewSet, basename='book')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'company', CompanyViewSet, basename='company')


urlpatterns = [
    path('', include(router.urls))
]