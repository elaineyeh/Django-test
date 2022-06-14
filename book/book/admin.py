from django.contrib import admin
from book.models import Category, Company, Book


admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Company)