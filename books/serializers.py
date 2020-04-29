from rest_framework import serializers
from .models import Bookmodel, Locationmodel


class BookSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(many=True,
                            read_only=True,
                            slug_field='name')
    class Meta:
        model = Bookmodel
        fields = ['title',
                  'author',
                  'isbn',
                  'average_rating',
                  'location']

