from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import PasswordResetSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from allauth.account.forms import ResetPasswordForm
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


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

	def update(self, instance, validated_data):
		pass

	def create(self, validated_data):
		pass


class UserSerializer(serializers.ModelSerializer):
	ADMIN, STAFF, AUTHOR, VIEWER, GUEST = range(0, 5)
	permission_type = GUEST  # defined by request.user (type and authentication=True/False)

	class Meta:
		model = get_user_model()
		fields = ['id', 'username', 'email']

	def create(self, validated_data):
		validated_data.update(self.deserialize_nested_data_by_reuse_or_create(
			ElementModel=get_user_model(),
			ElementSerializer=UserSerializer,
			element=validated_data
		))
		return super(UserSerializer, self).create(validated_data)

	def update(self, instance, validated_data):
		pass
