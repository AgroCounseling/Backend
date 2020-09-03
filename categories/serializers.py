from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', ]


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'title', 'category']


class TypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Types
        fields = ['id', 'title', 'subcategory']


class SubTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTypes
        fields = ['id', 'title', 'type']


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['id', 'title', 'description', 'image', 'icon_image']


class CategoryConsultantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryConsultant
        fields = ('id', 'consultant', 'category',)
        read_only_fields = ('id', 'consultant',)


class CategoryConsultantDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryConsultant
        fields = ('id', 'consultant', 'category',)
