from rest_framework import serializers
from .models import *
from users.serializers import UsersListSerializer


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'thread', 'user', 'message', 'timestamp', 'status']


class ThreadDetailSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    first = UsersListSerializer(many=False, read_only=True)
    second = UsersListSerializer(many=False, read_only=True)

    class Meta:
        model = Thread
        fields = ['id', 'first', 'second', 'time', 'access', 'timestamp', 'messages']
        read_only_fields = ['first', 'second', 'time', 'timestamp', 'messages']


class ThreadListSerializer(serializers.ModelSerializer):
    first = UsersListSerializer(many=False, read_only=True)
    second = UsersListSerializer(many=False, read_only=True)
    new_messages = serializers.IntegerField(source='unreaded', read_only=True)

    class Meta:
        model = Thread
        fields = ['id', 'first', 'second', 'time', 'access', 'timestamp', 'new_messages']
        read_only_fields = ['first', 'second', 'time', 'timestamp', 'new_messages']


class ThreadGetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ['id', 'first', 'second', 'time', 'access', 'timestamp']
        read_only_fields = ['first', 'second', 'time', 'timestamp']


class MessageCreateSerializer(serializers.Serializer):
    message = serializers.CharField()

    def create(self, validated_data):
        return ChatMessage.objects.create(**validated_data)
