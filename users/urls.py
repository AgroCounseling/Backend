from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('token/', CustomTokenView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),

    path('signup/client', RegistrationClientViewSet.as_view({'post': 'create'})),
    path('signup/consultant', RegistrationConsultantViewSet.as_view({'post': 'create'})),

    path('profile/', UserViewSet.as_view({'get': 'list'})),
    path('profile/edit/<str:name>/', UserViewSet.as_view({'get': 'retrieve','put': 'update'})),

    path('consultants/', ConsultantListViewSet.as_view({'get': 'list'})),
    path('consultants/<int:pk>/', ConsultantListViewSet.as_view({'get': 'retrieve'})),
    path('specialty/<int:pk>/consultants/', ConsultantViewSet.as_view({'get': 'list'})),


    path('reviews/', ReviewsViewSet.as_view({'get': 'list'})),
    path('reviews/<int:pk>/', ReviewsViewSet.as_view({'get': 'retrieve'})),
    path('reviews/delete/<int:pk>/', ReviewsViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    path('reviews/create/<int:pk>/', ReviewsViewSet.as_view({'post': 'create'})),
]
