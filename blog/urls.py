from django.contrib import admin
from django.urls import path, include

from posts.views import *
from django.contrib.auth import views as auth_views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static
# operate post


urlpatterns = [
    path('', home, name='blog-home'),
    path('admin/', admin.site.urls),
    path('blog/', events, name='post-list'),
    path('post/<id>/', post, name='post-detail'),
    path('post/<id>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<id>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('blog/new/', PostCreateView.as_view(), name='post-create'),
    path('search/', search, name='search'),
    path('tinymce/', include('tinymce.urls')),
    path('register/', user_views.register, name='register'),
    path('contact/', contact, name='contact'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    # email to reset password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),
    # confirm email has been sent
    path('password-reset/done',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('profile/', user_views.profile, name='profile'),
    path('user/<int:author_id>', user_events, name='user-posts'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
