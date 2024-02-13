"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import index_view, task_test_view, data_test_view
from accounts.views import SignupView, VerifyEmailView, PasswordResetRequestView, PasswordResetConfirmView, CustomTokenObtainPairView, CustomTokenRefreshView
from files.views import ImgUploadView

urlpatterns = [
    path('api/', index_view, name='index'),

    # accounts
    path('api/signup/', SignupView.as_view(), name='signup'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/verify/<str:uidb64>/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/password_reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('api/password_reset_confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # examples
    path('api/rest/notes/', include("notes.urls")),
    path('api/test_task', task_test_view, name='test_task'),
    path('api/test_data', data_test_view, name='test_data'),

    # long running tasks
    path('api/tasks/', include('tasks.urls')),

    # file uploads
    path('api/img_upload/', ImgUploadView.as_view(), name='img_upload'),

    # admin
    path('api/admin/', admin.site.urls),
]
