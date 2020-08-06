from rest_framework import serializers
from .models import *
from users.serializers import UsersListSerializer


class VoteSerializer(serializers.ModelSerializer):
    user = UsersListSerializer(read_only=True, many=False)
    article = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Vote
        fields = ['id', 'user', 'vote', 'article', 'pub_date']
        read_only_fields = ['user', 'pub_date']

    def create(self, validated_data):
        vote, _ = Vote.objects.update_or_create(
            user=validated_data.get('user', None),
            article=validated_data.get('article', None),
            defaults={'vote': validated_data.get('vote')}
        )
        return vote


class VoteSelfSerializer(serializers.ModelSerializer):
    user = UsersListSerializer(many=False, read_only=True)
    article = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Vote
        fields = ['id', 'user', 'vote', 'article', 'pub_date']
        read_only_fields = ['pub_date', 'vote']


class ArticleAdditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleAddition
        fields = ['id', 'article', 'subtitle', 'subtext']
        read_only_fields = ['article']


class ArticleListSerializer(serializers.ModelSerializer):
    additions = ArticleAdditionSerializer(read_only=True, many=True)
    votes = serializers.IntegerField(source='total_votes', read_only=True)
    user = UsersListSerializer(read_only=True, many=False)

    class Meta:
        model = Article
        fields = ['id', 'user', 'category', 'subcategory', 'types', 'subtypes', 'title', 'text', 'additions',
                  'pub_date', 'status',
                  'votes']
        read_only_fields = ['user', 'pub_date', 'votes', 'status', 'additions']


class ArticleDetailSerializer(serializers.ModelSerializer):
    additions = ArticleAdditionSerializer(many=True)
    votes = serializers.IntegerField(source='total_votes', read_only=True)
    user = UsersListSerializer(read_only=True, many=False)

    class Meta:
        model = Article
        fields = ['id', 'user', 'category', 'subcategory', 'types', 'subtypes', 'title', 'text', 'additions',
                  'pub_date', 'status', 'votes']
        read_only_fields = ['user', 'pub_date', 'votes', 'status']

    def create(self, validated_data):
        additions_data = validated_data.pop('additions')
        article = Article.objects.create(**validated_data)
        for addition_data in additions_data:
            ArticleAddition.objects.create(article=article, **addition_data)
        return article
