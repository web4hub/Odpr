from accounts.models import User
from django.contrib.auth import get_user_model
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.core.exceptions import ObjectDoesNotExist

GUEST, VIEWER, AUTHOR, STAFF, ADMIN, CUSTOM_ID = range(0, 6)

test_user = {
	'username': 'testuser',
	'email': 'testuser@testmailserver.com',
	'password': 'testpassword'
}

def assert_has_data_field(self, response):
	self.assertIsNotNone(obj=response.data, msg='Response should contain some data')
	self.assertGreaterEqual(len(response.data), 1, 'Response should contain some data')

def assert_detail_response_matches_whitelist(response, whitelist):
	"""
	Works with and without pagination and accepts the response object as well as response.data as argument.
	:param response: response from a view or its data.
	:param whitelist: A tuple of expected fields contained in data
	:return: None
	"""
	assert_detail_response_has_only_data_of(response, whitelist=whitelist)
	if hasattr(response, 'data'):
		if 'results' in response.data:
			for field in whitelist:
				assert field in response.data.get('results')
		else:
			for field in whitelist:
				assert field in response.data
	else:
		for field in whitelist:
			assert field in response

def assert_list_response_matches_whitelist(response, whitelist):
	if 'results' in response.data:
		for element in response.data.get('results'):
			assert_detail_response_matches_whitelist(element, whitelist)
	else:
		for element in response.data:
			assert_detail_response_matches_whitelist(element, whitelist)

def assert_list_response_has_only_data_of(response, whitelist):
	if 'results' in response.data:
		for element in response.data.get('results'):
			assert_detail_response_has_only_data_of(element, whitelist)
	else:
		for element in response.data:
			assert_detail_response_has_only_data_of(element, whitelist)

def assert_detail_response_has_only_data_of(response, whitelist):
	if hasattr(response, 'data'):
		if 'results' in response.data:
			for field in response.data.get('results'):
				assert field in whitelist
		else:
			for field in response.data:
				assert field in whitelist
	else:
		for field in response:
			assert field in whitelist

def assert_response_200(self, response):
	self.assertGreaterEqual(response.status_code, 200)
	self.assertLess(response.status_code, 300)

def assert_response_between(self, response, a, b):
	self.assertGreaterEqual(response.status_code, a)
	self.assertLess(response.status_code, b)

def make_register_request(**kwargs):
	factory = APIRequestFactory(enforce_csrf_checks=True)
	request = factory.post(path='', **kwargs)
	session_middleware = SessionMiddleware()
	message_middleware = MessageMiddleware()
	session_middleware.process_request(request)
	message_middleware.process_request(request)
	return request

def get_factory():
	return APIRequestFactory()

def make_get_request(**kwargs):
	return get_factory().get(path='', **kwargs)

def make_post_request(**kwargs):
	return get_factory().post(path='', **kwargs)

def make_put_request(**kwargs):
	return get_factory().put(path='', **kwargs)

def make_patch_request(**kwargs):
	return get_factory().patch(path='', **kwargs)

def make_delete_request(**kwargs):
	return get_factory().delete(path='', **kwargs)

def create_user_directly(user):
	return get_user_model().objects.create_user(username=user['username'], email=user['email'], password=user['password'])

def get_admin_user():
	admins = User.objects.filter(is_admin=True)
	if len(admins) >= 1:
		assert admins[0].is_admin
		return admins[0]
	else:
		raise ObjectDoesNotExist('Tried to authenticate test-request with admin user, but could not find any admin user. '
														 'Maybe you did not load fixtures for this test or there is no admin in the fixtures?')

def get_staff_user():
	staffs = User.objects.filter(is_staff=True, is_admin=False)
	if len(staffs) >= 1:
		assert staffs[0].is_staff
		return staffs[0]
	else:
		raise ObjectDoesNotExist('Tried to authenticate test-request with staff user, but could not find any staff user '
														 'who is not admin at the same time.'
														 'Maybe you did not load fixtures for this test or there is no staff user in the fixtures?')

def get_author_user():
	users = User.objects.filter(is_admin=False, is_staff=False)
	if len(users) >= 1:
		assert not users[0].is_staff and not users[0].is_admin
		return users[0]
	else:
		raise ObjectDoesNotExist('Tried to authenticate test-request with normal user, but could not find any normal user '
														 'who is neither admin nor staff.'
														 'Maybe you did not load fixtures for this test or there is no normal user in the fixtures?')

def get_viewer_user():
	users = User.objects.filter(is_admin=False, is_staff=False)
	if len(users) >= 2:
		assert not users[1].is_staff and not users[1].is_admin
		return users[1]
	else:
		raise ObjectDoesNotExist('Tried to authenticate test-request with normal user, but could not find enough normal '
														 'users who are neither admin nor staff.'
														 'Maybe you did not load fixtures for this test or there is no normal user in the '
														 'fixtures? Note that you need at least 2 normal users in your fixtures for this purpose.')

def authenticate(request, user_id=2):
	force_authenticate(request, user=User.objects.get(pk=user_id))

def authenticate_admin(request):
	authenticate(request=request, user_id=get_admin_user().pk)

def authenticate_staff(request):
	authenticate(request=request, user_id=get_staff_user().pk)

def authenticate_author_user(request):
	authenticate(request=request, user_id=get_author_user().pk)

def authenticate_viewer_user(request):
	authenticate(request=request, user_id=get_viewer_user().pk)

def authenticate_by_user_type(request, user_type=AUTHOR, custom_id=1):
	if user_type is VIEWER:
		authenticate_viewer_user(request)
	elif user_type is AUTHOR:
		authenticate_author_user(request)
	elif user_type is STAFF:
		authenticate_staff(request)
	elif user_type is ADMIN:
		authenticate_admin(request)
	elif user_type is CUSTOM_ID:
		authenticate(request, user_id=custom_id)

def verify_response_status_code(self, response, expected_success=True):
	if expected_success:
		assert_response_200(self, response)
	else:
		assert_response_between(self, response, 400, 500)
