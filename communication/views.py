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
        audio = serializer.validated_data.get("audio")
        image = serializer.validated_data.get("image")
        video = serializer.validated_data.get("video")
        file = serializer.validated_data.get("file")
        serializer.save(user=user, thread=thread, message=message, audio=audio, image=image, video=video, file=file)


class ThreadViewSet(ModelViewSet):
    queryset = Thread.objects.all()
    pagination_class = CustomResultsSetPagination

    def list(self, request, *args, **kwargs):
        queryset = Thread.objects.by_user(self.request.user)
        serializer = self.get_serializer(queryset, many=True)
        serializer.data[0]['new_messages'] = ChatMessage.objects.filter(status=False).count()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        query = ChatMessage.objects.all()
        query.update(status=True)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ThreadDetailSerializer
        elif self.action == 'list':
            return ThreadListSerializer
        else:
            return ThreadGetUpdateSerializer
