from django.test import TestCase
from rest_framework.test import APIRequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from test_util.test_util import assert_response_200, assert_has_data_field
from .views import CustomRegisterView
from django.contrib.auth import get_user_model
from django.test import TestCase
from odpr_shared_models.test_util.user_tests.user_list_tests import \
	verify_unauthenticated_userlist_request_should_return_expected_data, \
	verify_authenticated_userlist_request_should_return_expected_data, \
	verify_staff_userlist_request_should_return_expected_data, \
	verify_admin_userlist_request_should_return_expected_data
from odpr_shared_models.test_util.user_tests.user_detail_tests import \
	verify_unauthenticated_userdetail_request_should_return_expected_data, \
	verify_authenticated_viewer_userdetail_request_should_return_expected_data, \
	verify_authenticated_author_userdetail_request_should_return_expected_data, \
	verify_authenticated_staff_userdetail_request_should_return_expected_data, \
	verify_authenticated_admin_userdetail_request_should_return_expected_data
from odpr_shared_models.test_util.user_tests.user_create_tests import \
	verify_unauthenticated_user_create_succeeds, \
	verify_authenticated_user_create_fails, \
	verify_user_create_ignores_unexpected_argument, \
	test_user_create_fails_due_missing_argument
from odpr_shared_models.test_util.user_tests.user_update_tests import \
	verify_unauthenticated_user_update_fails, \
	verify_authenticated_viewer_user_update_fails, \
	verify_authenticated_author_user_update_succeeds, \
	verify_authenticated_author_cannot_update_readonly_fields, \
	verify_authenticated_staff_can_update_other_user, \
	verify_authenticated_admin_can_update_other_user
from odpr_shared_models.test_util.user_tests.user_delete_tests import \
	verify_unauthenticated_user_delete_fails, \
	verify_authenticated_viewer_user_delete_fails, \
	verify_authenticated_author_user_delete_succeeds, \
	verify_authenticated_staff_can_delete_other_user, \
	verify_authenticated_admin_can_delete_other_user
# https://www.django-rest-framework.org/api-guide/testing/


"""
	Test 1:  User registration should succeed if not existing
	Test 2:  User registration should fail if existing
	Test 3:  User list should return restricted data (unauthenticated request)
	Test 4:  User list should return normal data (authenticated but not admin or staff)
	Test 5:  Unauthenticated User Details-Request should return restricted data
	Test 6:  Authenticated User Details-Request should show normal infos (more than unauthenticated, less than admin/staff
						or the same user requesting their own information)
	Test 7:  Authenticated User Details-Request should give all infos to same user
	TODO: test username change by uniqueness
	TODO: test email change by uniqueness
	TODO: test password change through password change view
	TODO: test whether only admins can give more rights to users.
"""

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


class UserCreateTestsNoFixtures(TestCase):
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

class UserCreateTests(TestCase):
	""" Register tests """
	fixtures = ('user_fixtures',)

	def test_unauthenticated_user_create_registers_new_user_successfully(self):
		print('=================== Test 1:  User create should succeed ===================================================')
		verify_unauthenticated_user_create_succeeds(self)  # This is the register test
		print('================================================= End of Test 1 ===========================================')

	def test_authenticated_user_user_create_with_unexpected_additional_argument_should_succeed(self):
		''' Additional arguments are simply ignored '''
		print('=================== Test 2:  User create should create user unexpected arg ================================')
		verify_user_create_ignores_unexpected_argument(self)
		print('================================================= End of Test 2 ===========================================')

	def test_authenticated_user_create_should_fail(self):
		print('=================== Test 3:  User create should fail ======================================================')
		verify_authenticated_user_create_fails(self)
		print('================================================= End of Test 3 ===========================================')

	def test_unauthenticated_user_create_should_fail_due_missing_argument(self):
		print('=================== Test 4:  User create should fail ======================================================')
		test_user_create_fails_due_missing_argument(self)
		print('================================================= End of Test 4 ===========================================')

# TODO: add special login logout register testcases which do not force auth but via views.

class UserListTests(TestCase):
	fixtures = ('user_fixtures',)

	def test_unauthenticated_user_list_matches_expected_data(self):
		print('=================== Test 1:  User list should return correct data =========================================')
		verify_unauthenticated_userlist_request_should_return_expected_data(self)
		print('================================================= End of Test 1 ===========================================')

	def test_authenticated_user_list_matches_expected_data(self):
		print('=================== Test 2:  User list should return correct data =========================================')
		verify_authenticated_userlist_request_should_return_expected_data(self)
		print('================================================= End of Test 2 ===========================================')

	def test_staff_user_list_matches_expected_data(self):
		print('=================== Test 3:  User list should return correct data =========================================')
		verify_staff_userlist_request_should_return_expected_data(self)
		print('================================================= End of Test 3 ===========================================')

	def test_admin_user_list_matches_expected_data(self):
		print('=================== Test 4:  User list should return correct data =========================================')
		verify_admin_userlist_request_should_return_expected_data(self)
		print('================================================= End of Test 4 ===========================================')


class UserDetailTests(TestCase):
	fixtures = ('user_fixtures',)

	def test_unauthenticated_user_detail_matches_expected_data(self):
		print('=================== Test 1:  User detail should return correct data =======================================')
		verify_unauthenticated_userdetail_request_should_return_expected_data(self)
		print('================================================= End of Test 1 ===========================================')

	def test_authenticated_viewer_user_user_detail_matches_expected_data(self):
		print('=================== Test 2:  User detail should return correct data =======================================')
		verify_authenticated_viewer_userdetail_request_should_return_expected_data(self)
		print('================================================= End of Test 2 ===========================================')

	def test_authenticated_author_user_detail_matches_expected_data(self):
		print('=================== Test 3:  User detail should return correct data =======================================')
		verify_authenticated_author_userdetail_request_should_return_expected_data(self)
		print('================================================= End of Test 3 ===========================================')

	def test_staff_user_detail_matches_expected_data(self):
		print('=================== Test 4:  User detail should return correct data =======================================')
		verify_authenticated_staff_userdetail_request_should_return_expected_data(self)
		print('================================================= End of Test 4 ===========================================')

	def test_admin_user_detail_matches_expected_data(self):
		print('=================== Test 5:  User detail should return correct data =======================================')
		verify_authenticated_admin_userdetail_request_should_return_expected_data(self)
		print('================================================= End of Test 5 ===========================================')


class UserUpdateTests(TestCase):
	fixtures = ('user_fixtures',)

	def test_unauthenticated_user_update_fails(self):
		print('=================== Test 1:  User update should fail ======================================================')
		verify_unauthenticated_user_update_fails(self)
		print('================================================= End of Test 1 ===========================================')

	def test_authenticated_viewer_user_update_should_return_error(self):
		print('=================== Test 2:  User update should return permission error ===================================')
		verify_authenticated_viewer_user_update_fails(self)
		print('================================================= End of Test 2 ===========================================')

	def test_authenticated_author_user_update_should_succeed(self):
		print('=================== Test 3:  User update should succeed ===================================================')
		verify_authenticated_author_user_update_succeeds(self)
		print('================================================= End of Test 3 ===========================================')

	def test_authenticated_author_user_update_read_only_should_succeed(self):
		print('=================== Test 4:  User update on readonly fields should ignore readonly fields and succeed =====')
		verify_authenticated_author_cannot_update_readonly_fields(self)
		print('================================================= End of Test 4 ===========================================')

	def test_authenticated_staff_user_update_viewer_author_should_succeed(self):
		print('=================== Test 5:  User update by staff of viewer user should succeed ===========================')
		verify_authenticated_staff_can_update_other_user(self)
		print('================================================= End of Test 5 ===========================================')

	def test_authenticated_admin_user_update_viewer_author_should_succeed(self):
		print('=================== Test 6:  User update by admin of viewer user should succeed ===========================')
		verify_authenticated_admin_can_update_other_user(self)
		print('================================================= End of Test 6 ===========================================')


class UserDeleteTests(TestCase):
	fixtures = ('user_fixtures',)

	def test_unauthenticated_user_delete_fails(self):
		print('=================== Test 1:  User delete should redirect to login =========================================')
		verify_unauthenticated_user_delete_fails(self)
		print('================================================= End of Test 1 ===========================================')

	def test_authenticated_viewer_user_user_delete_should_return_error(self):
		print('=================== Test 2:  User delete should return permission error ===================================')
		verify_authenticated_viewer_user_delete_fails(self)
		print('================================================= End of Test 2 ===========================================')

	def test_authenticated_author_user_delete_should_succeed(self):
		print('=================== Test 3:  User delete should succeed ===================================================')
		verify_authenticated_author_user_delete_succeeds(self)
		print('================================================= End of Test 3 ===========================================')

	def test_authenticated_staff_user_delete_viewer_author_should_succeed(self):
		print('=================== Test 4:  User delete by staff of viewer user should succeed ===========================')
		verify_authenticated_staff_can_delete_other_user(self)
		print('================================================= End of Test 4 ===========================================')

	def test_authenticated_admin_user_delete_viewer_author_should_succeed(self):
		print('=================== Test 5:  User delete by admin of viewer user should succeed ===========================')
		verify_authenticated_admin_can_delete_other_user(self)
		print('================================================= End of Test 5 ===========================================')


# TODO: test if badge-ownership is correctly created (compare creation strings and try to get badge-ownership in db directly)
# TODO: test if visited count incremented for every visitor (user-visited attribute)
# TODO: test if visited in usermodel incremented for every authenticated visit (everytime authenticated user-detail request)
# TODO: test viewer counters as well...
# TODO: we also want a date of visit to be able to sort it... thus an intermediate table is needed.
# TODO: test if upvoting a user will delete an existing downvote.
# TODO: test if upvoting again will neutralize votes on a user.
# TODO: test same vice versa
# TODO: test same with requests and comments.
# TODO: test if such votes do not affect viewer sceneries.
# TODO: test if response with user data has correct counts of votes? (maybe not needed)
