from django.shortcuts import render
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from agrarie.pagintions import CustomResultsSetPagination
from rest_framework.response import Response


class MessageViewSet(ModelViewSet):
    serializer_class = MessageCreateSerializer

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_email = self.kwargs.get("email")
        obj, created = Thread.objects.get_user(self.request.user, other_email)
        if obj == None:
            raise NotFound
        return obj

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        thread = self.get_object()
        if not thread.access:
            raise PermissionDenied
        user = self.request.user
        message = serializer.validated_data.get("message")
        serializer.save(user=user, thread=thread, message=message)


class ThreadViewSet(ModelViewSet):
    queryset = Thread.objects.all()
    pagination_class = CustomResultsSetPagination

    def list(self, request, *args, **kwargs):
        queryset = Thread.objects.by_user(self.request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        for item in range(len(serializer.data['messages'])):
            serializer.data['messages'][item]['status'] = True
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ThreadDetailSerializer
        elif self.action == 'list':
            return ThreadListSerializer
        else:
            return ThreadGetUpdateSerializer
