from odpr_shared_models.test_util.test_util import make_get_request, assert_response_200, assert_has_data_field, \
	assert_list_response_matches_whitelist, authenticate_admin, authenticate_staff, \
	authenticate_viewer_user
from sceneries.permissions import UNAUTHENTICATED_SCENERY_LIST_DATA_ACCESS_FULL, \
	ADMIN_SCENERY_LIST_DATA_ACCESS_FULL, \
	STAFF_SCENERY_LIST_DATA_ACCESS_FULL, \
	AUTHENTICATED_SCENERY_LIST_DATA_ACCESS_FULL
from sceneries.views import SceneryListView


def perform_scenerydetail_request_and_validate_response(self, request, whitelist):
	scenery_list_view = SceneryListView.as_view()
	response = scenery_list_view(request=request)
	assert_response_200(self, response)
	assert_has_data_field(self, response)
	assert_list_response_matches_whitelist(response, whitelist=whitelist)
	return response

def perform_scenery_list_get_request(self, whitelist, authenticate_function=None):
	request = make_get_request()
	if authenticate_function is not None:
		authenticate_function(request)
	perform_scenerydetail_request_and_validate_response(
		self=self, request=request, whitelist=whitelist
	)

def verify_unauthenticated_scenerylist_request_should_return_expected_data(self):
	perform_scenery_list_get_request(
		self=self, whitelist=UNAUTHENTICATED_SCENERY_LIST_DATA_ACCESS_FULL
	)

def verify_authenticated_scenerylist_request_should_return_expected_data(self):
	perform_scenery_list_get_request(
		self=self, authenticate_function=authenticate_viewer_user, whitelist=AUTHENTICATED_SCENERY_LIST_DATA_ACCESS_FULL
	)

def verify_staff_scenerylist_request_should_return_expected_data(self):
	perform_scenery_list_get_request(
		self=self, authenticate_function=authenticate_staff, whitelist=STAFF_SCENERY_LIST_DATA_ACCESS_FULL
	)

def verify_admin_scenerylist_request_should_return_expected_data(self):
	perform_scenery_list_get_request(
		self=self, authenticate_function=authenticate_admin, whitelist=ADMIN_SCENERY_LIST_DATA_ACCESS_FULL
	)
