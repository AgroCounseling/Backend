from django.urls import path
from .views import *

urlpatterns = [
    path('articles/', ArticleViewSet.as_view({'get': 'list'})),
    path('articles/<int:pk>', ArticleViewSet.as_view({'get': 'retrieve'})),
    path('articles/edit/<int:pk>', ArticleViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('articles/delete/<int:pk>', ArticleViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    path('articles/create', ArticleViewSet.as_view({'post': 'create'})),

    path('popular-articles/', PopularArticleViewSet.as_view({'get': 'list'})),
    path('new-articles/', NewArticleViewSet.as_view({'get': 'list'})),

    path('votes/create/<int:pk>', VoteViewSet.as_view({'post': 'create'})),
    path('votes/self/<int:pk>/', VoteViewSet.as_view({'get': 'list'})),
    path('votes/edit/<int:pk>', VoteViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('votes/delete/<int:pk>', VoteViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    path('votes/<int:pk>', VoteViewSet.as_view({'get': 'retrieve'})),

]