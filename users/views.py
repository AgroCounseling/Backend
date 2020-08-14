from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *
from rest_framework.exceptions import PermissionDenied
from agrarie.pagintions import CustomResultsSetPagination
from rest_framework.permissions import IsAdminUser
from .permissions import IsClient


class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer
    permission_classes = [AllowAny]


class RegistrationClientViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegistrationClientSerializer


class RegistrationConsultantViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Consultant.objects.all()
    serializer_class = RegistrationConsultantSerializer


class RatingViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    # permission_classes = [IsClient | IsAdminUser]
    permission_classes = [AllowAny]
    pagination_class = CustomResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return RatingCreateSerializer
        else:
            return RatingListSerializer


class ConsultantViewSet(ReadOnlyModelViewSet):
    # permission_classes = [IsClient | IsConsultant | IsAdminUser]
    permission_classes = [AllowAny]
    serializer_class = ConsultantListSerializer
    pagination_class = CustomResultsSetPagination

    def get_queryset(self):
        specialty = CategoryConsultant.objects.filter(category=self.kwargs['pk'])
        consultants = []
        count = 0
        for spec in specialty:
            consultants += Consultant.objects.filter(id=specialty[count].consultant.pk, user__is_active=True).annotate(
                middle_star=models.Sum(models.F('ratings__star__value')) / models.Count(
                    models.F('ratings')),
            )
            count += 1
        return consultants


class ConsultantListViewSet(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ConsultantListSerializer
    pagination_class = CustomResultsSetPagination

    def get_queryset(self):
        return Consultant.objects.filter(user__is_active=True).annotate(
            middle_star=models.Sum(models.F('ratings__star__value')) / models.Count(
                models.F('ratings')),
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return ConsultantListSerializer
        elif self.action == 'retrieve':
            return ConsultantDetailSerializer


class ReviewsViewSet(ModelViewSet):
    # permission_classes = [IsClient | IsAdminUser]
    permission_classes = [AllowAny]
    queryset = Reviews.objects.all()
    pagination_class = CustomResultsSetPagination

    def perform_create(self, serializer):
        user = User.objects.get(id=self.request.user.pk)
        serializer.save(name='{} {}'.format(user.first_name, user.last_name), email=user.email)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'destroy' or self.action == 'update':
            return ReviewsListSerializer
        elif self.action == 'retrieve' or self.action == 'list':
            return ReviewsDetailSerializer


class UserViewSet(ModelViewSet):
    # permission_classes = [IsClient | IsConsultant | IsAdminUser]
    permission_classes = [AllowAny]

    def get_queryset(self):
        try:
            if self.request.user.is_consultant:
                return Consultant.objects.filter(user__id=self.request.user.pk)
            elif self.request.user.is_client:
                return User.objects.filter(id=self.request.user.pk)
        except:
            raise PermissionDenied

    def get_object(self):
        name = self.kwargs['name']
        pk = self.request.user.pk
        if self.request.user.is_consultant:
            obj = get_object_or_404(Consultant, user__first_name=name, user__id=pk)
        elif self.request.user.is_client:
            obj = get_object_or_404(User, first_name=name, id=pk)
        return obj

    def get_serializer_class(self):
        try:
            if self.request.user.is_consultant:
                return ProfileConsultantSerializer
            elif self.request.user.is_client:
                return UsersListSerializer
        except:
            raise PermissionDenied
