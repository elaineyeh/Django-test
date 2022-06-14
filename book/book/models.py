from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
    

class Category(models.Model):
    category = models.CharField(max_length=32)


class Company(models.Model):
    company = models.CharField(max_length=64)
    address = models.CharField(max_length=128)
    phone = models.CharField(max_length=32)


class Book(models.Model):
    title = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    publish_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)