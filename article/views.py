from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAdminUser
from users.permissions import IsClient, IsConsultant
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .serializers import *
from .models import *
from users.models import User
from rest_framework.permissions import AllowAny
from agrarie.pagintions import CustomResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters


class VoteViewSet(ModelViewSet):
    # permission_classes = [IsClient | IsConsultant | IsAdminUser]
    permission_classes = [AllowAny]
    serializer_class = VoteSerializer
    pagination_class = CustomResultsSetPagination

    def get_queryset(self):
        queryset = Vote.objects.filter(article_id=self.kwargs["pk"])
        return queryset

    def perform_create(self, serializer):
        article = Article.objects.get(id=self.kwargs['pk'], status=True)
        return serializer.save(user=self.request.user, article=article)

    def list(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.user.pk)
            queryset = Vote.objects.filter(article_id=kwargs["pk"], user=user)
            serializer = VoteSelfSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            raise PermissionDenied



class ArticleViewSet(ModelViewSet):
    # permission_classes = [IsConsultant | IsAdminUser]
    permission_classes = [AllowAny]
    queryset = Article.objects.all()
    pagination_class = CustomResultsSetPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['category', 'subcategory', 'types', 'subtypes']
    search_fields = ['title']

    def get_queryset(self):
        queryset = Article.objects.filter(status=True)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        else:
            return ArticleDetailSerializer


class PopularArticleViewSet(ReadOnlyModelViewSet):
    # permission_classes = [IsConsultant | IsAdminUser]
    permission_classes = [AllowAny]
    serializer_class = ArticleListSerializer
    pagination_class = CustomResultsSetPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['category', 'subcategory', 'types', 'subtypes']
    search_fields = ['title']

    def get_queryset(self):
        queryset = Article.objects.order_by('-votes').filter(status=True)
        return queryset


class NewArticleViewSet(ReadOnlyModelViewSet):
    # permission_classes = [IsConsultant | IsAdminUser]
    permission_classes = [AllowAny]
    serializer_class = ArticleListSerializer
    pagination_class = CustomResultsSetPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['category', 'subcategory', 'types', 'subtypes']
    search_fields = ['title']

    def get_queryset(self):
        queryset = Article.objects.order_by('-pub_date').filter(status=True)
        return queryset
