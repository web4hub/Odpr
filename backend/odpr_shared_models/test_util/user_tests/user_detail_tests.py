from ..test_util import make_get_request, assert_response_200, \
	assert_detail_response_matches_whitelist, authenticate_admin, authenticate_author_user, authenticate_staff, \
	authenticate_viewer_user, assert_has_data_field
from accounts.permissions import UNAUTHENTICATED_USER_DETAIL_DATA_ACCESS_FULL, \
	AUTHENTICATED_OTHER_USER_DETAIL_DATA_ACCESS_FULL, \
	AUTHENTICATED_SELF_USER_DETAIL_DATA_ACCESS_FULL, \
	STAFF_USER_DETAIL_DATA_ACCESS_FULL, \
	ADMIN_USER_DETAIL_DATA_ACCESS_FULL
from accounts.views import UserDetailView
from .test_util import get_first_testuser_instance

def verify_userdetail_request_returns_expected_data(self, request, whitelist):
	user_detail_view = UserDetailView.as_view()
	user_id = get_first_testuser_instance().id
	response = user_detail_view(request=request, id=user_id)
	assert_response_200(self, response)
	assert_has_data_field(self, response)
	assert_detail_response_matches_whitelist(response, whitelist=whitelist)
	return response

def perform_user_detail_get_request(self, whitelist, authenticate_function=None):
	request = make_get_request()
	if authenticate_function is not None:
		authenticate_function(request)
	verify_userdetail_request_returns_expected_data(
		self, request=request, whitelist=whitelist
	)

def verify_unauthenticated_userdetail_request_should_return_expected_data(self):
	perform_user_detail_get_request(
		self=self, whitelist=UNAUTHENTICATED_USER_DETAIL_DATA_ACCESS_FULL
	)

def verify_authenticated_viewer_userdetail_request_should_return_expected_data(self):
	perform_user_detail_get_request(
		self=self, authenticate_function=authenticate_viewer_user,
		whitelist=AUTHENTICATED_OTHER_USER_DETAIL_DATA_ACCESS_FULL
	)

def verify_authenticated_author_userdetail_request_should_return_expected_data(self):
	perform_user_detail_get_request(
		self=self, authenticate_function=authenticate_author_user,
		whitelist=AUTHENTICATED_SELF_USER_DETAIL_DATA_ACCESS_FULL
	)

def verify_authenticated_staff_userdetail_request_should_return_expected_data(self):
	perform_user_detail_get_request(
		self=self, authenticate_function=authenticate_staff,
		whitelist=STAFF_USER_DETAIL_DATA_ACCESS_FULL
	)

def verify_authenticated_admin_userdetail_request_should_return_expected_data(self):
	perform_user_detail_get_request(
		self=self, authenticate_function=authenticate_admin,
		whitelist=ADMIN_USER_DETAIL_DATA_ACCESS_FULL
	)
