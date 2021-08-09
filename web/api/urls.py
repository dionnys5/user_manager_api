from django.urls import include, path
from web.api import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('me/', views.Me.as_view(), name='my_user'),
    path('signup/', views.Signup.as_view(), name='user_signup'),
    path('signin/', views.Signin.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
