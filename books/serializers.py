from rest_framework import serializers
from .models import Bookmodel


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmodel
        fields = ['title',
                  'author',
                  'isbn',
                  'location']

