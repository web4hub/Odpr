from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import LoginSerializer
from rest_auth.serializers import PasswordResetSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from allauth.account.forms import ResetPasswordForm
from django.conf import settings
from odpr_shared_models.serializer_util import NestedModelSerializer
from odpr_shared_models.serializers import TextWithHistorySerializer
from django.utils.translation import ugettext_lazy as _
from rest_framework.fields import empty
from .permissions import ADMIN_USER_DETAIL_DATA_ACCESS_FULL,\
	STAFF_USER_DETAIL_DATA_ACCESS_FULL,\
	AUTHENTICATED_OTHER_USER_DETAIL_DATA_ACCESS_FULL,\
	UNAUTHENTICATED_USER_DETAIL_DATA_ACCESS_FULL, \
	AUTHENTICATED_SELF_USER_DETAIL_DATA_ACCESS_FULL, \
	ADMIN_USER_DETAIL_READ_ONLY_DATA_ACCESS, AUTHENTICATED_OTHER_USER_DETAIL_READ_ONLY_DATA_ACCESS, \
	AUTHENTICATED_SELF_USER_DETAIL_READ_ONLY_DATA_ACCESS, STAFF_USER_DETAIL_READ_ONLY_DATA_ACCESS, \
	UNAUTHENTICATED_USER_DETAIL_READ_ONLY_DATA_ACCESS, UNAUTHENTICATED_USER_LIST_DATA_ACCESS_FULL, \
	ADMIN_USER_LIST_DATA_ACCESS_FULL, AUTHENTICATED_USER_LIST_DATA_ACCESS_FULL, STAFF_USER_LIST_DATA_ACCESS_FULL, \
	ADMIN_USER_LIST_READ_ONLY_DATA_ACCESS, AUTHENTICATED_USER_LIST_READ_ONLY_DATA_ACCESS, \
	STAFF_USER_LIST_READ_ONLY_DATA_ACCESS, UNAUTHENTICATED_USER_LIST_READ_ONLY_DATA_ACCESS


class CustomRegisterSerializer(RegisterSerializer):
	def update(self, instance, validated_data):
		pass

	def create(self, validated_data):
		pass

	username = serializers.CharField(required=True)
	email = serializers.EmailField(required=True)
	password1 = serializers.CharField(write_only=True, style={'input_type': 'password'})
	password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

	def get_cleaned_data(self):
		super(CustomRegisterSerializer, self).get_cleaned_data()

		return {
			'password1': self.validated_data.get('password1', ''),
			'email': self.validated_data.get('email', ''),
			'username': self.validated_data.get('username', ''),
		}

class CustomUserLoginSerializer(LoginSerializer):
	def update(self, instance, validated_data):
		pass

	def create(self, validated_data):
		pass

	username = serializers.CharField(required=False, allow_blank=True)
	email = serializers.EmailField(required=False, allow_blank=True)
	password = serializers.CharField(style={'input_type': 'password'})


class CustomPasswordResetSerializer(PasswordResetSerializer):
	email = serializers.EmailField()
	password_reset_form_class = ResetPasswordForm

	def validate_email(self, value):
		# Create PasswordResetForm with the serializer
		self.reset_form = self.password_reset_form_class(data=self.initial_data)
		if not self.reset_form.is_valid():
			raise serializers.ValidationError(self.reset_form.errors)

		###### FILTER YOUR USER MODEL ######
		if not get_user_model().objects.filter(email=value).exists():
			raise serializers.ValidationError(_('Invalid e-mail address'))

		return value

	def save(self):
		request = self.context.get('request')
		# Set some values to trigger the send_email method.
		opts = {
			'use_https': request.is_secure(),
			'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
			'request': request,
		}
		opts.update(self.get_email_options())
		self.reset_form.save(**opts)

	def update(self, instance, validated_data):
		pass

	def create(self, validated_data):
		pass


class CustomTokenSerializer(serializers.Serializer):
	token = serializers.CharField()


class UserSerializer(NestedModelSerializer):
	ADMIN, STAFF, AUTHOR, VIEWER, GUEST = range(0, 5)
	permission_type = GUEST  # defined by request.user (type and authentication=True/False)

	bio = TextWithHistorySerializer()

	class Meta:
		model = get_user_model()
		# Fields and readonly fields are defined by the overwritten methods below!

	def create(self, validated_data):
		validated_data.update(self.deserialize_nested_data_by_reuse_or_create(
			ElementModel=get_user_model(),
			ElementSerializer=UserSerializer,
			element=validated_data
		))
		return super(UserSerializer, self).create(validated_data)

	def save(self, **kwargs):
		if self.serializer_type is NestedModelSerializer.PUT or self.serializer_type is NestedModelSerializer.PATCH:
			self.validated_data.update(self.deserialize_nested_update(
				ElementModel=get_user_model(),
				ElementSerializer=UserSerializer,
				element=self.validated_data,
				**kwargs
			))
			return self.overwritten_save_for_nested_update(**kwargs)
		else:
			return super(UserSerializer, self).save(**kwargs)

	def __init__(self, instance=None, data=empty, **kwargs):
		kwargs.pop('permission_type', None)
		super(UserSerializer, self).__init__(instance, data, **kwargs)

	@classmethod
	def __new__(cls, *args, **kwargs):
		serializer_type = kwargs.pop('serializer_type', None)
		cls.set_serializer_type(serializer_type)
		permission_type = kwargs.pop('permission_type', None)
		list_serializer = kwargs.get('many', None)
		cls.set_list_type(list_serializer)
		cls.set_permission_type(permission_type)
		return super(NestedModelSerializer, cls).__new__(*args, **kwargs)

	@classmethod
	def set_permission_type(cls, permission_type):
		if permission_type is not None:
			if type(permission_type) is not int:
				raise TypeError('permission_type must be int.')
			if permission_type < 0 or permission_type >= 5:
				raise ValueError('permission_type can only be one of 0, 1, 2, 3, 4')
			cls.permission_type = permission_type
		cls.update_fields()
		cls.update_readonly_fields()

	@classmethod
	def get_readonly_get_fields(cls):
		if cls.list_serializer:
			if cls.permission_type is UserSerializer.GUEST:
				return UNAUTHENTICATED_USER_LIST_READ_ONLY_DATA_ACCESS
			elif cls.permission_type is UserSerializer.VIEWER or cls.permission_type is UserSerializer.AUTHOR:
				return AUTHENTICATED_USER_LIST_READ_ONLY_DATA_ACCESS
			elif cls.permission_type is UserSerializer.STAFF:
				return STAFF_USER_LIST_READ_ONLY_DATA_ACCESS
			elif cls.permission_type is UserSerializer.ADMIN:
				return ADMIN_USER_LIST_READ_ONLY_DATA_ACCESS
		else:
			if cls.permission_type is UserSerializer.GUEST:
				return UNAUTHENTICATED_USER_DETAIL_READ_ONLY_DATA_ACCESS
			elif cls.permission_type is UserSerializer.VIEWER:
				return AUTHENTICATED_OTHER_USER_DETAIL_READ_ONLY_DATA_ACCESS
			elif cls.permission_type is UserSerializer.AUTHOR:
				return AUTHENTICATED_SELF_USER_DETAIL_READ_ONLY_DATA_ACCESS
			elif cls.permission_type is UserSerializer.STAFF:
				return STAFF_USER_DETAIL_READ_ONLY_DATA_ACCESS
			elif cls.permission_type is UserSerializer.ADMIN:
				return ADMIN_USER_DETAIL_READ_ONLY_DATA_ACCESS
		raise IndexError('Invalid permission type: Can only be one of 0, 1, 2, 3!')

	@classmethod
	def get_get_fields(cls):
		if cls.list_serializer:
			if cls.permission_type is UserSerializer.GUEST:
				return UNAUTHENTICATED_USER_LIST_DATA_ACCESS_FULL
			elif cls.permission_type is UserSerializer.VIEWER or cls.permission_type is UserSerializer.AUTHOR:
				return AUTHENTICATED_USER_LIST_DATA_ACCESS_FULL
			elif cls.permission_type is UserSerializer.STAFF:
				return STAFF_USER_LIST_DATA_ACCESS_FULL
			elif cls.permission_type is UserSerializer.ADMIN:
				return ADMIN_USER_LIST_DATA_ACCESS_FULL
		else:
			if cls.permission_type is UserSerializer.GUEST:
				return UNAUTHENTICATED_USER_DETAIL_DATA_ACCESS_FULL
			elif cls.permission_type is UserSerializer.VIEWER:
				return AUTHENTICATED_OTHER_USER_DETAIL_DATA_ACCESS_FULL
			elif cls.permission_type is UserSerializer.AUTHOR:
				return AUTHENTICATED_SELF_USER_DETAIL_DATA_ACCESS_FULL
			elif cls.permission_type is UserSerializer.STAFF:
				return STAFF_USER_DETAIL_DATA_ACCESS_FULL
			elif cls.permission_type is UserSerializer.ADMIN:
				return ADMIN_USER_DETAIL_DATA_ACCESS_FULL
		raise IndexError('Invalid permission type: Can only be one of 0, 1, 2, 3!')

	@classmethod
	def get_put_fields(cls):
		if cls.permission_type is UserSerializer.AUTHOR:
			return 'id', 'username', 'email', 'bio', 'profile_image_id'
		elif cls.permission_type is UserSerializer.STAFF:
			return 'id', 'username', 'email', 'bio', 'profile_image_id', 'is_active'
		elif cls.permission_type is UserSerializer.ADMIN:
			return 'id', 'username', 'email', 'bio', 'profile_image_id', 'is_active', 'user_type'
		raise IndexError('Invalid permission type: Can only be one of 0, 1, 2!')

	@classmethod
	def get_patch_fields(cls):
		return cls.get_put_fields()

