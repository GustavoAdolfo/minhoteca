from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have a valid email address.')
        if not password:
            raise ValueError('Users must have a valid password.')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        # user.save(using=self._db)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('email_confirmed', False)
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_staff', False)
        user = self._create_user(email, password, **extra_fields)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('email_confirmed', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        user = self._create_user(email, password, **extra_fields)
        return user


class MinhotecaUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)
    # date_joined = models.DateTimeField(auto_now_add=True)
    use_term_accepted_at = models.DateTimeField(
        null=False,
        blank=True,
        auto_now_add=True)
    contact_phone = models.CharField(max_length=11, null=True)
    zip_code = models.CharField(max_length=8, null=True)
    address = models.CharField(max_length=100, null=True)
    address_number = models.CharField(max_length=10, null=True)
    address_complement = models.CharField(
        max_length=50, null=True, default=None)
    neighborhood = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=2, null=True, default='SP')
    can_borrow = models.BooleanField(default=False)


    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_username(self):
        return self.email


