import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager
import jwt
from votingBackend import settings


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + datetime.timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS512')

        return token.decode('utf-8')


class User(AbstractUser):
    OPTIONS = [('Voter', 'Voter'), ('Staff', 'Staff'), ('Candidate', 'Candidate')]
    username = None
    email = models.CharField(max_length=200, null=True, unique=True)
    sex = models.CharField(max_length=2, default='')
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    phoneNumber = models.CharField(max_length=11, default='')
    # lastName = models.CharField(max_length=50, default='')
    face_id = models.CharField(max_length=50, default='')
    password = models.CharField(null=False, max_length=200)
    image_url = models.CharField(max_length=200, blank=True, null=True)
    NiN = models.CharField(max_length=11, null=True, blank=True, default='')
    token = models.CharField(null=False, max_length=255, default='')
    activatedBy = models.CharField(max_length=11,blank=True, null=True, default='')
    status = models.BooleanField(default=False)
    user_type = models.CharField(max_length=200, choices=OPTIONS, default='Voter')
    updatedAt = models.DateTimeField(null=True)
    createdAt = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.first_name
