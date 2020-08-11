from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from .models import Slider
from .serializers import *
from agrarie.pagintions import CustomResultsSetPagination


class SliderViewSet(ReadOnlyModelViewSet):
    # permission_classes = [IsClient | IsConsultant | IsAdminUser]
    permission_classes = [AllowAny]
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    pagination_class = CustomResultsSetPagination


class ContactInfoViewSet(ReadOnlyModelViewSet):
    # permission_classes = [IsClient | IsConsultant | IsAdminUser]
    permission_classes = [AllowAny]
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer
    pagination_class = CustomResultsSetPagination

