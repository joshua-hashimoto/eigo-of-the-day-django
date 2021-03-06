from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from pages.views import MarkdownImageUploader

urlpatterns = [
    # django admin
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('headquarters/', admin.site.urls),
    # user management
    path('accounts/', include('allauth.urls')),
    # third party
    path('martor/', include('martor.urls')),
    # local apps
    path('api/uploader/', MarkdownImageUploader.as_view(),
         name='markdown_uploader_page'),
    path('', include('eigo.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
