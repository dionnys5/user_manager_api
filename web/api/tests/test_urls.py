from django.test import SimpleTestCase
from django.urls import reverse, resolve
from web.api.views import Me, Signup, Signin
from rest_framework_simplejwt.views import TokenRefreshView

class testLoginUrls(SimpleTestCase):
    
    def test_signup_url_is_resolved(self):
        url = reverse('user_signup')
        self.assertEquals(resolve(url).func.view_class, Signup)

    def test_sign_url_is_resolved(self):
        url = reverse('token_obtain_pair')
        self.assertEquals(resolve(url).func.view_class, Signin)

    def test_refrash_token_url_is_resolved(self):
        url = reverse('token_refresh')
        self.assertEquals(resolve(url).func.view_class, TokenRefreshView)


class testUserUrls(SimpleTestCase):

    def test_me_url_is_resolved(self):
        url = reverse('my_user')
        self.assertEquals(resolve(url).func.view_class, Me)


# path('signup/', views.Signup.as_view(), name='user_signup'),
# path('signin/', views.SigninView.as_view(), name='token_obtain_pair'),
# path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),