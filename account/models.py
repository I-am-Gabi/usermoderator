from django.db import models
from django.core import validators
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
from institutes.models import Institute

import re
import logging
logger = logging.getLogger(__name__)

class UserManager(BaseUserManager): 
    def _create_user(self, username, email, password, status, is_staff, is_superuser, **extra_fields): 
        now = timezone.now()
        if not username:
            raise ValueError(_('The given username must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                 is_staff=is_staff, is_active=True,
                 is_superuser=is_superuser, last_login=now,
                 date_joined=now, **extra_fields)
        user.set_password(password)
        user.status = status
        user.save(using=self._db)
        logger.debug('save {}'.format(user.get_full_name()))
        return user

    def create_user(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, 0, False, False,
                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        user=self._create_user(username, email, password, 1, True, True,
                 **extra_fields)
        user.is_active=True 
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin): 
    ORDER_STATUS = ((0, 'pending'), (1, 'approved'), (2, 'denied')) 
 
    username = models.CharField(_('username'), max_length=15, unique=True,
        help_text=_('Obrigatório. 15 caracteres ou menos. Letras, \
                    números e @/./+/-/_'),
        validators=[validators.RegexValidator(
                                            re.compile('^[\w.@+-]+$'),
                                            _('Digite um username válido.'),
                                            _('invalid'))])
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as active. \
                    Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    status = models.PositiveSmallIntegerField(choices=ORDER_STATUS)
    password = models.CharField(max_length=50)
    institute = models.ForeignKey(Institute, on_delete=models.SET_NULL, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])