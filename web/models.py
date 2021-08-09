from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Usuário deve ter um e-mail')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save()
        return user

    def get_by_natural_key(self, email):
        return self.get(email=email)


class CustomUser(AbstractBaseUser):

    email = models.EmailField(null=False, unique=True)
    firstName = models.CharField(max_length=255, null=False)
    lastName = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self) -> str:
        return self.email


class CustomPhoneManager(BaseUserManager):

    def get_phones_by_user(self, user_id):
        return Phone.objects.filter(user_id=user_id) 

class Phone(models.Model):
    number = models.CharField(max_length=9, null=False)
    area_code = models.SmallIntegerField()
    country_code = models.CharField(max_length=3, null=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)

    objects = CustomPhoneManager()


    def __str__(self) -> str:
        return f'{self.country_code} ({self.area_code}){self.number}'