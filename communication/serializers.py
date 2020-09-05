from rest_framework import serializers
from .models import *
from users.serializers import UsersListSerializer


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'thread', 'user', 'message', 'video', 'audio', 'image', 'file', 'timestamp', 'status']


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
    # last_message = serializers.CharField()

    class Meta:
        model = Thread
        fields = ['id', 'first', 'second', 'time', 'access', 'times_rooms', 'timestamp']
        read_only_fields = ['first', 'second', 'time', 'times_rooms', 'timestamp']


class ThreadGetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ['id', 'first', 'second', 'time', 'access', 'timestamp']
        read_only_fields = ['first', 'second', 'timestamp']


class MessageCreateSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    message = serializers.CharField()
    audio = serializers.FileField(required=False)
    image = serializers.ImageField(required=False)
    video = serializers.FileField(required=False)
    file = serializers.FileField(required=False)

    def create(self, validated_data):
        return ChatMessage.objects.create(**validated_data)

