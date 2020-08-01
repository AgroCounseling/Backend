from categories.serializers import CategoryConsultantListSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from categories.models import CategoryConsultant
from .models import *
from agrarie.settings import SIMPLE_JWT


class CustomTokenSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super(CustomTokenSerializer, self).validate(attrs)
        data.update({'status_client': self.user.is_client})
        data.update({'status_consultant': self.user.is_consultant})
        data.update({'time_access': SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']})
        data.update({'time_refresh': SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']})
        return data


class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'photo', 'phone')
        read_only_fields = ['email']


class UsersDetailSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, style={'input_type': 'password'},
                                     label='Пароль')

    class Meta:
        model = User
        fields = (
            'id', 'email', 'password', 'first_name', 'last_name', 'photo', 'phone')


class RatingStarSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingStart
        fields = '__all__'


class RatingCreateSerializer(serializers.ModelSerializer):
    user = UsersListSerializer(many=False, read_only=True)

    class Meta:
        model = Rating
        fields = ('id', 'user', 'consultant', 'star',)
        read_only_fields = ('id', 'user',)

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            user=validated_data.get('user', None),
            consultant=validated_data.get('consultant', None),
            defaults={'star': validated_data.get('star')}
        )
        return rating


class RatingListSerializer(serializers.ModelSerializer):
    user = UsersListSerializer(many=False, read_only=True)
    star = RatingStarSerializer(many=False, read_only=True)

    class Meta:
        model = Rating
        fields = ('id', 'user', 'consultant', 'star',)
        read_only_fields = ('id', 'user',)


class ImageConsultantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageConsultant
        fields = ('id', 'consultant', 'certificate_image',)
        read_only_fields = ('consultant',)


class ConsultantListSerializer(serializers.ModelSerializer):
    user = UsersListSerializer(many=False)
    specialty = CategoryConsultantListSerializer(many=True, read_only=True)
    middle_star = serializers.FloatField()

    class Meta:
        model = Consultant
        fields = ('id', 'user', 'specialty', 'title', 'description', 'middle_star')


class ProfileConsultantSerializer(serializers.ModelSerializer):
    user = UsersListSerializer(many=False)
    specialty = CategoryConsultantListSerializer(many=True)

    class Meta:
        model = Consultant
        fields = ('id', 'user', 'title', 'description', 'specialty')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        user.email = user_data.get('email', user.email)
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.photo = user_data.get('photo', user.photo)
        user.phone = user_data.get('phone', user.phone)
        user.save()
        return instance


class ReviewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ('id', 'consultant', 'text')


class ReviewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ("id", 'consultant', "name", 'email', "text")


class ConsultantDetailSerializer(serializers.ModelSerializer):
    user = UsersListSerializer(many=False)
    specialty = CategoryConsultantListSerializer(many=True, read_only=True)
    reviews = ReviewsDetailSerializer(many=True, read_only=True)
    ratings = RatingListSerializer(many=True, read_only=True)

    class Meta:
        model = Consultant
        fields = ('id', 'user', 'specialty', 'title', 'description', 'reviews', 'ratings')


class ConsultantSearchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultant
        fields = ('id', 'user', 'title', 'description')


class RegistrationClientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        style={'input_type': 'password'},
        label='Пароль'
    )
    password1 = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        style={'input_type': 'password'},
        label='Потверждение пароля'
    )

    class Meta:
        model = User
        fields = (
            'email', 'password', 'password1', 'first_name', 'last_name', 'photo', 'phone')
        read_only_fields = ('is_client', 'is_consultant', 'is_active')

    def create(self, validated_data):
        password = validated_data.pop('password')
        password1 = validated_data.pop('password1')
        if password1 and password and password != password1:
            raise serializers.ValidationError('Пароль не совпадает')
        user = User.objects.create_user(password=password, **validated_data)
        user.save()
        return user


class RegistrationConsultantSerializer(serializers.ModelSerializer):
    user = UsersDetailSerializer(many=False)
    specialty = CategoryConsultantListSerializer(many=True)
    certificates = ImageConsultantListSerializer(many=True)
    password1 = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        style={'input_type': 'password'},
        label='Потверждение пароля'
    )

    class Meta:
        model = Consultant
        fields = ('id', 'user', 'specialty', 'certificates', 'password1', 'description', 'comment')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password1 = validated_data.pop('password1')
        categories_data = validated_data.pop('specialty')
        certificates_data = validated_data.pop('certificates')
        password = user_data['password']
        if password1 and password and password != password1:
            raise serializers.ValidationError('Пароль не совпадает')
        user = User.objects.create_consultant(**user_data)
        consultant = Consultant.objects.create(user=user, **validated_data)
        for category_data in categories_data:
            CategoryConsultant.objects.create(consultant=consultant, **category_data)
        for certificate_data in certificates_data:
            ImageConsultant.objects.create(consultant=consultant, **certificate_data)
        user.save()
        return consultant
