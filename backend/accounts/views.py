from django.shortcuts import render
from rest_auth.registration.views import RegisterView
from rest_auth.registration.app_settings import register_permission_classes
from rest_auth.views import LoginView
from rest_auth.views import LogoutView
from rest_auth.views import PasswordResetConfirmView
from django.contrib.auth import get_user_model
from rest_framework import generics
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from rest_auth.utils import jwt_encode
from rest_auth.app_settings import create_token
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.views import APIView
from rest_framework import parsers, renderers, status
from rest_framework.response import Response
from .serializers import CustomTokenSerializer, UserSerializer
from django_rest_passwordreset.models import ResetPasswordToken
from django_rest_passwordreset.views import get_password_reset_token_expiry_time
from django.utils import timezone
from datetime import timedelta
from rest_framework import permissions
from .permissions import IsUnauthenticatedOrAdminOrStaff, IsOwnerOrAdminOrStaffOrReadOnly
from .forms import UserLoginForm
from odpr_shared_models.views import NestedRetrieveUpdateDestroyAPIView
from .models import User
from django import forms
from filer.models import FolderRoot, Folder
from django.core.exceptions import ObjectDoesNotExist

class NewFolderForm(forms.ModelForm):
	class Meta(object):
		model = Folder
		fields = ('name',)

def get_user_by_id(pk):
	return User.objects.get(pk=pk)

def get_user_serializer_permission_type(self):
	if self.request.user.is_authenticated and self.request.user.is_admin:
		return UserSerializer.ADMIN
	elif self.request.user.is_authenticated and self.request.user.is_staff:
		return UserSerializer.STAFF
	elif self.request.user.is_authenticated and \
		'kwargs' in self.request.parser_context and \
		'id' in self.request.parser_context['kwargs'] and \
		get_user_by_id(self.request.parser_context['kwargs']['id']).pk == self.request.user.id:
		return UserSerializer.AUTHOR
	elif self.request.user.is_authenticated:
		return UserSerializer.VIEWER
	else:
		return UserSerializer.GUEST

class CustomRegisterView(RegisterView):
	queryset = get_user_model().objects.all()
	permission_classes = register_permission_classes() + (IsUnauthenticatedOrAdminOrStaff, )

	def get_response_data(self, user):
		token = super(CustomRegisterView, self).get_response_data(user)
		response = UserSerializer(instance=user, permission_type=UserSerializer.AUTHOR).data
		response.update(token)
		return response

	def create(self, request, *args, **kwargs):
		response = super(CustomRegisterView, self).create(request, *args, **kwargs)
		if response.status_code == status.HTTP_201_CREATED:
			# Create folder for user for django-filer, where all user-provided content will be stored.
			self.create_user_folder(get_user_by_id(response.data['id']))
		return response

	def perform_create(self, serializer):
		user = super(CustomRegisterView, self).perform_create(serializer)
		if self.queryset.count() == 1:
			user.is_superuser = True
			user.is_staff = True
			user.is_admin = True
			user.user_type = get_user_model().ADMIN
			user.save()
		return user

	def create_user_folder(self, user):
		root_folder = self.get_or_create_root_folder()
		new_folder_form = NewFolderForm({'name': 'user_{}'.format(user.id)})
		if new_folder_form.is_valid():
			new_folder = new_folder_form.save(commit=False)
			if root_folder.contains_folder(new_folder.name):
				raise ValueError('Folder with this name already exists.')
			else:
				new_folder.parent = root_folder
				new_folder.owner = user
				new_folder.save()

	def get_or_create_root_folder(self):
		try:
			return Folder.objects.get(name='filer_root')
		except ObjectDoesNotExist:
			root_folder_form = NewFolderForm({'name': 'filer_root'})
			if root_folder_form.is_valid():
				new_folder = root_folder_form.save(commit=True)
				return new_folder
			else:
				raise AttributeError('Could not create root folder')


class UserListView(generics.ListAPIView):
	queryset = get_user_model().objects.all()
	serializer_class = UserSerializer
	permission_classes = (permissions.AllowAny,)

	def get_serializer(self, *args, **kwargs):
		serializer_class = self.get_serializer_class()
		kwargs['context'] = self.get_serializer_context()
		return serializer_class(permission_type=get_user_serializer_permission_type(self), *args, **kwargs)


class UserDetailView(NestedRetrieveUpdateDestroyAPIView):
	queryset = get_user_model().objects.all()
	serializer_class = UserSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
												IsOwnerOrAdminOrStaffOrReadOnly,)
	lookup_field = 'id'

	def get_serializer(self, *args, **kwargs):
		serializer_class = self.get_serializer_class()
		kwargs['context'] = self.get_serializer_context()
		return serializer_class(permission_type=get_user_serializer_permission_type(self), *args, **kwargs)


class UserDataView(generics.RetrieveAPIView):
	"""
		This class provides functionality to fetch user data by token, just for the logged in user.
	"""
	queryset = get_user_model().objects.all()
	serializer_class = UserSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def get_object(self):
		return self.request.user


class UserLoginView(LoginView):
	def login(self):
		try:
			self.user = self.serializer.validated_data['user']
		except KeyError:
			try:
				self.user = self.serializer.validated_data['email']
			except KeyError:
				return HttpResponse('No username or email given.')

		if getattr(settings, 'REST_USE_JWT', False):
			self.token = jwt_encode(self.user)
		else:
			self.token = create_token(self.token_model, self.user,
																self.serializer)

		if getattr(settings, 'REST_SESSION_LOGIN', True):
			self.process_login()


class UserLogoutView(LogoutView):
	pass


class CustomPasswordResetView:
	@receiver(reset_password_token_created)
	def password_reset_token_created(sender, reset_password_token, *args, **kwargs):
		"""
			Handles password reset tokens
			When a token is created, an e-mail needs to be sent to the user
		"""
		# send an e-mail to the user
		site_url = os.environ.get('DJANGO_ALLOWED_HOST_1') or 'localhost:8000'
		site_full_name = os.environ.get('DJANGO_ALLOWED_HOST_1') or 'localhost:8000'
		site_shortcut_name = os.environ.get('DJANGO_ALLOWED_HOST_1') or 'localhost:8000'

		context = {
			'current_user': reset_password_token.user,
			'username': reset_password_token.user.username,
			'email': reset_password_token.user.email,
			'reset_password_url': "{}/password-reset/{}".format(site_url, reset_password_token.key),
			'site_name': site_shortcut_name,
			'site_domain': site_url
		}

		# render email text
		email_html_message = render_to_string('email/user_reset_password.html', context)
		email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

		msg = EmailMultiAlternatives(
			# title:
			"Password Reset for {}".format(site_full_name),
			# message:
			email_plaintext_message,
			# from:
			"noreply@{}".format(site_url),
			# to:
			[reset_password_token.user.email]
		)
		msg.attach_alternative(email_html_message, "text/html")
		msg.send()


class CustomPasswordTokenVerificationView(APIView):
	"""
		An Api View which provides a method to verifiy that a given pw-reset token is valid before actually confirming the
		reset.
	"""
	throttle_classes = ()
	permission_classes = ()
	parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
	renderer_classes = (renderers.JSONRenderer,)
	serializer_class = CustomTokenSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		token = serializer.validated_data['token']

		# get token validation time
		password_reset_token_validation_time = get_password_reset_token_expiry_time()

		# find token
		reset_password_token = ResetPasswordToken.objects.filter(key=token).first()

		if reset_password_token is None:
			return Response({'status': 'invalid'}, status=status.HTTP_404_NOT_FOUND)

		# check expiry date
		expiry_date = reset_password_token.created_at + timedelta(hours=password_reset_token_validation_time)

		if timezone.now() > expiry_date:
			# delete expired token
			reset_password_token.delete()
			return Response({'status': 'expired'}, status=status.HTTP_404_NOT_FOUND)

		# check if user has password to change
		if not reset_password_token.user.has_usable_password():
			return Response({'status': 'irrelevant'})

		return Response({'status': 'OK'})


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
	pass
