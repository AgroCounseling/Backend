from rest_framework import serializers
from .models import *


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ['image', 'pub_date']
        read_only_fields = ['pub_date']


class PhonesInfo(serializers.ModelSerializer):
    class Meta:
        model = PhonesInfo
        fields = ['phone', 'address']


class ContactInfoSerializer(serializers.ModelSerializer):
    phones = PhonesInfo(many=True, read_only=True)

    class Meta:
        model = ContactInfo
        fields = ['address', 'phones']
        read_only_fields = ['phones', 'address']
