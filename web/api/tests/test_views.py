from django.test import TestCase
from rest_framework.test import APIClient
from web.models import CustomUser
from rest_framework import status
import json
from rest_framework_simplejwt.tokens import RefreshToken



class TestLoginSignupViews(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_signup_view_complete_data(self):
        data = {
            'firstName': 'hello',
            'lastName': 'world',
            'email': 'hello@world.com',
            'password': 'hunter2',
            'phones':[{
                "number": 988887888,
                "area_code": 81,
                "country_code": "+55"
            }]
        }
        response = self.client.post('/signup/', data, format='json')
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(CustomUser.objects.all().count(), 1)
        self.assertNotEquals(response_data.get('access'), None)
        self.assertNotEquals(response_data.get('refresh'), None)

    def test_signup_view_missing_data(self):
        data = {
            'lastName': 'world',
            'email': 'hello@world.com',
            'password': 'hunter2',
            'phones':[{
                "number": 988887888,
                "area_code": 81,
                "country_code": "+55"
            }]
        }
        response = self.client.post('/signup/', data, format='json')
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(CustomUser.objects.all().count(), 0)
        self.assertEquals(response_data['message'], 'Missing fields')


    def test_signup_invalid_email_data(self):
        data = {
            'firstName': 'hello',
            'lastName': 'world',
            'email': 'helloworld.com',
            'password': 'hunter2',
            'phones':[{
                "number": 988887888,
                "area_code": 81,
                "country_code": "+55"
            }]
        }
        response = self.client.post('/signup/', data, format='json')
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(CustomUser.objects.all().count(), 0)
        self.assertEquals(response_data['message'], 'Invalid fields')

    def test_signup_exists_email_data(self):
        CustomUser.objects.create(
            firstName='user1',
            lastName='user12',
            email='hello@world.com',
            password='hunter3',
        )
        data = {
            'firstName': 'hello',
            'lastName': 'world',
            'email': 'hello@world.com',
            'password': 'hunter2',
            'phones':[{
                "number": 988887888,
                "area_code": 81,
                "country_code": "+55"
            }]
        }
        response = self.client.post('/signup/', data, format='json')
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEquals(response_data['message'], 'E-mail already exists')

class TestLoginSigninViews(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_signin_complete_correct_data(self):
        user = CustomUser(
            firstName='hello',
            lastName='world',
            email='hello@world.com',
        )
        user.set_password('hunter2')
        user.save()
        data = {
            'email': 'hello@world.com',
            'password': 'hunter2'
        }
        response = self.client.post('/signin/', data, format='json')
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertNotEquals(response_data.get('access'), None)
        self.assertNotEquals(response_data.get('refresh'), None)
        self.assertEquals(response_data['email'], 'hello@world.com')

    def test_signin_incorrect_data(self):
        user = CustomUser(
            firstName='hello',
            lastName='world',
            email='hello@world.com',
        )
        user.set_password('hunter2')
        user.save()
        data = {
            'email': 'hello2@world.com',
            'password': 'hunter2'
        }
        response = self.client.post('/signin/', data, format='json')
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(response_data.get('access'), None)
        self.assertEquals(response_data.get('detail'), 'Invalid e-mail or password')

    def test_signin_missing_email_data(self):
        user = CustomUser(
            firstName='hello',
            lastName='world',
            email='hello@world.com',
        )
        user.set_password('hunter2')
        user.save()
        data = {
            'email': '',
            'password': 'hunter2'
        }
        response = self.client.post('/signin/', data, format='json')
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response_data['message'], 'Missing fields')


class TestMeViews(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_me_correct_token_get_data(self):
        user = CustomUser(
            firstName='hello',
            lastName='world',
            email='hello@world.com',
        )
        user.set_password('hunter2')
        user.save()
        token = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token.access_token))
        response = self.client.get('/me/', format='json')
        response_data = json.loads(response.content)
        print(response_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response_data['email'], 'hello@world.com')


    def test_me_correct_missing_token_error(self):
        token = ''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get('/me/', format='json')
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(response_data['code'], 'bad_authorization_header')