from ..test_util import make_get_request, assert_response_200, assert_has_data_field, \
	assert_list_response_matches_whitelist, authenticate_admin, authenticate_staff, \
	authenticate_viewer_user
from scenery_requests.permissions import UNAUTHENTICATED_REQUEST_LIST_DATA_ACCESS_FULL, \
	ADMIN_REQUEST_LIST_DATA_ACCESS_FULL, \
	STAFF_REQUEST_LIST_DATA_ACCESS_FULL, \
	AUTHENTICATED_REQUEST_LIST_DATA_ACCESS_FULL
from scenery_requests.views import RequestListView


def perform_requestdetail_request_and_validate_response(self, request, whitelist):
	request_list_view = RequestListView.as_view()
	response = request_list_view(request=request)
	assert_response_200(self, response)
	assert_has_data_field(self, response)
	assert_list_response_matches_whitelist(response, whitelist=whitelist)
	return response

def perform_request_list_get_request(self, whitelist, authenticate_function=None):
	request = make_get_request()
	if authenticate_function is not None:
		authenticate_function(request)
	perform_requestdetail_request_and_validate_response(
		self=self, request=request, whitelist=whitelist
	)

def verify_unauthenticated_requestlist_request_should_return_expected_data(self):
	perform_request_list_get_request(
		self=self, whitelist=UNAUTHENTICATED_REQUEST_LIST_DATA_ACCESS_FULL
	)

def verify_authenticated_requestlist_request_should_return_expected_data(self):
	perform_request_list_get_request(
		self=self, authenticate_function=authenticate_viewer_user, whitelist=AUTHENTICATED_REQUEST_LIST_DATA_ACCESS_FULL
	)

def verify_staff_requestlist_request_should_return_expected_data(self):
	perform_request_list_get_request(
		self=self, authenticate_function=authenticate_staff, whitelist=STAFF_REQUEST_LIST_DATA_ACCESS_FULL
	)

def verify_admin_requestlist_request_should_return_expected_data(self):
	perform_request_list_get_request(
		self=self, authenticate_function=authenticate_admin, whitelist=ADMIN_REQUEST_LIST_DATA_ACCESS_FULL
	)
