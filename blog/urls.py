from django.contrib import admin
from django.urls import path, include

from posts.views import index, blog, post, search, contact
from django.contrib.auth import views as auth_views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static
# operate post


urlpatterns = [
    path('', index, name='blog-home'),
    # path('', PostListView.as_view(), name='blog-home'),
    path('admin/', admin.site.urls),
    path('blog/', blog, name='post-list'),
    path('post/<id>/', post, name='post-detail'),
    path('search/', search, name='search'),
    path('tinymce/', include('tinymce.urls')),
    path('register/', user_views.register, name='register'),
    path('contact/', contact, name='contact'),
    # in-build
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', user_views.profile, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
