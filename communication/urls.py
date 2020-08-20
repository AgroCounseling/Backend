from django.urls import path, re_path
from .views import *

urlpatterns = [
    path("messages/<str:email>", MessageViewSet.as_view({'post': 'create'})),
    path("rooms/", ThreadViewSet.as_view({'get': 'list'})),
    path("rooms/<int:pk>", ThreadViewSet.as_view({'get': 'retrieve'})),
    path("rooms/edit/<int:pk>", ThreadViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
]
