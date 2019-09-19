from odpr_shared_models.test_util.test_util import make_get_request, assert_response_200, \
	assert_detail_response_matches_whitelist, authenticate_admin, authenticate_author_user, authenticate_staff, \
	authenticate_viewer_user, assert_has_data_field
from sceneries.permissions import UNAUTHENTICATED_SCENERY_DETAIL_DATA_ACCESS_FULL, \
	AUTHENTICATED_OTHER_SCENERY_DETAIL_DATA_ACCESS_FULL, \
	AUTHENTICATED_SELF_SCENERY_DETAIL_DATA_ACCESS_FULL, \
	STAFF_SCENERY_DETAIL_DATA_ACCESS_FULL, \
	ADMIN_SCENERY_DETAIL_DATA_ACCESS_FULL
from sceneries.views import SceneryDetailView

def verify_scenerydetail_request_returns_expected_data(self, request, whitelist):
	scenery_detail_view = SceneryDetailView.as_view()
	response = scenery_detail_view(request=request, id=1)
	assert_response_200(self, response)
	assert_has_data_field(self, response)
	assert_detail_response_matches_whitelist(response, whitelist=whitelist)
	return response

def perform_scenery_detail_get_request(self, whitelist, authenticate_function=None):
	request = make_get_request()
	if authenticate_function is not None:
		authenticate_function(request)
	verify_scenerydetail_request_returns_expected_data(
		self, request=request, whitelist=whitelist
	)

def verify_unauthenticated_scenerydetail_request_should_return_expected_data(self):
	perform_scenery_detail_get_request(
		self=self, whitelist=UNAUTHENTICATED_SCENERY_DETAIL_DATA_ACCESS_FULL
	)

def verify_authenticated_other_scenerydetail_request_should_return_expected_data(self):
	perform_scenery_detail_get_request(
		self=self, authenticate_function=authenticate_viewer_user,
		whitelist=AUTHENTICATED_OTHER_SCENERY_DETAIL_DATA_ACCESS_FULL
	)

def verify_authenticated_author_scenerydetail_request_should_return_expected_data(self):
	perform_scenery_detail_get_request(
		self=self, authenticate_function=authenticate_author_user,
		whitelist=AUTHENTICATED_SELF_SCENERY_DETAIL_DATA_ACCESS_FULL
	)

def verify_authenticated_staff_scenerydetail_request_should_return_expected_data(self):
	perform_scenery_detail_get_request(
		self=self, authenticate_function=authenticate_staff,
		whitelist=STAFF_SCENERY_DETAIL_DATA_ACCESS_FULL
	)

def verify_authenticated_admin_scenerydetail_request_should_return_expected_data(self):
	perform_scenery_detail_get_request(
		self=self, authenticate_function=authenticate_admin,
		whitelist=ADMIN_SCENERY_DETAIL_DATA_ACCESS_FULL
	)
