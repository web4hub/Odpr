from django.test import TestCase
from rest_framework.test import APIRequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from test_util.test_util import assert_response_200, assert_has_data_field
from .views import CustomRegisterView
from django.contrib.auth import get_user_model

# https://www.django-rest-framework.org/api-guide/testing/

valid_test_user1 = {
	'username': 'valid_test_user1',
	'email': 'valid_test_user1@test.test',
	'password1': 'Pwdpwd11$',
	'password2': 'Pwdpwd11$'
}

valid_test_user2 = {
	'username': 'valid_test_user2',
	'email': 'valid_test_user2@test.test',
	'password1': 'Pwdpwd11$',
	'password2': 'Pwdpwd11$'
}


def make_register_request(request):
	session_middleware = SessionMiddleware()
	message_middleware = MessageMiddleware()
	session_middleware.process_request(request)
	message_middleware.process_request(request)
	return request


def register_test_user(userdata):
	factory = APIRequestFactory()
	request = factory.post('/api/v1/auth/register/', userdata, format='json')
	make_register_request(request)
	view = CustomRegisterView.as_view()
	return view(request)


def get_user_by_token(token):
	queryset = get_user_model().objects.filter(auth_token=token)
	assert len(queryset) == 1
	return queryset[0]


def assert_register_response_has_expected_content_and_user_created(self, response):
	assert_response_200(self, response)
	assert_has_data_field(self, response)
	assert "key" in response.data
	assert get_user_by_token(response.data['key']) is not None


class UserCreateTests(TestCase):

	def test_first_user_becomes_superuser(self):
		response = register_test_user(valid_test_user1)
		assert_register_response_has_expected_content_and_user_created(self, response)
		assert get_user_by_token(response.data['key']).is_admin

	def test_second_user_has_no_admin_privileges(self):
		response = register_test_user(valid_test_user1)
		assert_response_200(self, response)
		assert_register_response_has_expected_content_and_user_created(self, response)
		assert get_user_by_token(response.data['key']).is_admin
		response = register_test_user(valid_test_user2)
		assert_response_200(self, response)
		assert_register_response_has_expected_content_and_user_created(self, response)
		second_user = get_user_by_token(response.data['key'])
		assert not second_user.is_admin
		assert not second_user.is_staff
