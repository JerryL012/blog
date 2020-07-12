from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from posts.views import index, blog, post, search

urlpatterns = [
    path('', index, name='blog-home'),
    path('admin/', admin.site.urls),
    path('blog/', blog, name='post-list'),
    path('post/<id>/', post, name='post-detail'),
    path('search/', search, name='search'),
    path('tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
