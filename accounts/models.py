import re
from django.db import models
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
	use_in_migrations = True

	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)
		user.set_password(password)
		user.user_type = User.USER
		user.save(using=self._db)
		return user

	def create_staffuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.staff = True
		user.is_staff = True
		user.user_type = User.STAFF
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.staff = True
		user.admin = True
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.user_type = User.ADMIN

		user.save(using=self._db)
		return user


class User(AbstractBaseUser, PermissionsMixin):
	class Meta:
		app_label = 'accounts'
		db_table = 'user'
	# ordering=["created"]

	username = models.CharField(_('username'), max_length=75, unique=True,
															help_text=_('Required. 30 characters or fewer. Letters, numbers and '
																					'@/./+/-/_ characters'),
															validators=[
																validators.RegexValidator(re.compile('^[\w.@+-]+$'),
																													_('Enter a valid username.'), 'invalid')
															])

	email = models.EmailField(_('email address'), max_length=254, unique=True)
	is_staff = models.BooleanField(_('staff status'), default=False,
																 help_text=_('Designates whether the user can log into this admin '
																						 'site.'))
	is_active = models.BooleanField(_('active'), default=True,
																	help_text=_('Designates whether this user should be treated as '
																							'active. Unselect this instead of deleting accounts.'))
	is_admin = models.BooleanField(_('admin status'), default=False,
																 help_text='Whether this account has access to all admin settings or not.')
	date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

	objects = CustomUserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	def get_full_name(self):
		return self.username

	def get_short_name(self):
		return self.username

	def __unicode__(self):
		return self.email

	def __str__(self):
		return self.email

	ADMIN, STAFF, MOD, USER, GUEST = range(0, 5)
	UserTypes = (
		(ADMIN, 'Admin'),
		(STAFF, 'Staff'),
		(MOD, 'Moderator'),
		(USER, 'User'),
		(GUEST, 'Guest'),
	)
	user_type = models.IntegerField(choices=UserTypes, default=3)
