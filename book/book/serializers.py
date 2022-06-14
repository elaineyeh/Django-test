from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from django.contrib.auth.models import User as UserModel

from book.models import Category, Company, Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'category', 'company', 'publish_date', 'user')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'category')


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'company', 'address', 'phone')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username = validated_data['username'],
            password = validated_data['password']
        )

        return user

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'password')