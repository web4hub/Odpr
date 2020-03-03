from odpr_shared_models.test_util.test_util import make_get_request, assert_response_200, assert_has_data_field, \
	assert_list_response_matches_whitelist, authenticate_admin, authenticate_staff, \
	authenticate_viewer_user
from documentation.permissions import UNAUTHENTICATED_DOCUMENT_LIST_DATA_ACCESS_FULL, \
	ADMIN_DOCUMENT_LIST_DATA_ACCESS_FULL, \
	STAFF_DOCUMENT_LIST_DATA_ACCESS_FULL, \
	AUTHENTICATED_DOCUMENT_LIST_DATA_ACCESS_FULL
from documentation.views import DocumentListView


def perform_documentdetail_document_and_validate_response(self, request, whitelist):
	document_list_view = DocumentListView.as_view()
	response = document_list_view(request=request)
	assert_response_200(self, response)
	assert_has_data_field(self, response)
	assert_list_response_matches_whitelist(response, whitelist=whitelist)
	return response

def perform_document_list_get_request(self, whitelist, authenticate_function=None):
	request = make_get_request()
	if authenticate_function is not None:
		authenticate_function(request)
	perform_documentdetail_document_and_validate_response(
		self=self, request=request, whitelist=whitelist
	)

def verify_unauthenticated_documentlist_request_should_return_expected_data(self):
	perform_document_list_get_request(
		self=self, whitelist=UNAUTHENTICATED_DOCUMENT_LIST_DATA_ACCESS_FULL
	)

def verify_authenticated_documentlist_request_should_return_expected_data(self):
	perform_document_list_get_request(
		self=self, authenticate_function=authenticate_viewer_user, whitelist=AUTHENTICATED_DOCUMENT_LIST_DATA_ACCESS_FULL
	)

def verify_staff_documentlist_request_should_return_expected_data(self):
	perform_document_list_get_request(
		self=self, authenticate_function=authenticate_staff, whitelist=STAFF_DOCUMENT_LIST_DATA_ACCESS_FULL
	)

def verify_admin_documentlist_request_should_return_expected_data(self):
	perform_document_list_get_request(
		self=self, authenticate_function=authenticate_admin, whitelist=ADMIN_DOCUMENT_LIST_DATA_ACCESS_FULL
	)
