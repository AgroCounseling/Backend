from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .yasg import urlpatterns as doc_urls
from django.conf.urls.i18n import i18n_patterns
from agrarie.search import GlobalSearchAPIView

urlpatterns = i18n_patterns(
                  path('admin/', admin.site.urls),
                  path('api/', include('users.urls')),
                  path('api/text/', GlobalSearchAPIView.as_view()),
                  path('api/', include('forums.urls')),
                  path('api/', include('article.urls')),
                  path('api/', include('categories.urls')),
                  path('i18n/', include('django.conf.urls.i18n')),
                  path('jet/', include('jet.urls', 'jet')),
                  path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
                  path('api/auth/', include('djoser.urls')),
                  path('api/', include('informations.urls')),
                  path('api/', include('communication.urls')),
                  path('auth/', include('rest_framework_social_oauth2.urls')),
                  # path('api-auth/', include('rest_framework.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += doc_urls

