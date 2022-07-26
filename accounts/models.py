from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from django.core.validators import RegexValidator


# ugettext_lazy(多言語対応)は用意しない。


class CustomUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email Required!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Permission Denied: is_staff=False')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Permission Denied: is_superuser=False')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    validate_tcu_email = RegexValidator(
        regex=r"g([0-9]{2})([0-9]{2})([0-9]{3})@tcu\.ac\.jp",
        message="TCU Students Only",
    )
    email = models.EmailField('email address', unique=True, validators=[validate_tcu_email])
    first_name = models.CharField('given name', max_length=30, blank=True)
    last_name = models.CharField('family name', max_length=30, blank=True)
    cafeteria_ticket = models.IntegerField('cafeteria ticket', default=5)

    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Permission to access to the admin page'
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text='Set False to deactivate accounts'
    )
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    # send email to self
    def email_user(self, subject, message, from_email, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def username(self):
        return self.email
