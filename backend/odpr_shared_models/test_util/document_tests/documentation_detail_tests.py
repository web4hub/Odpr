from ..test_util import make_get_request, assert_response_200, \
	assert_detail_response_matches_whitelist, authenticate_admin, authenticate_author_user, authenticate_staff, \
	authenticate_viewer_user, assert_has_data_field
from documentation.permissions import UNAUTHENTICATED_DOCUMENT_DETAIL_DATA_ACCESS_FULL, \
	AUTHENTICATED_OTHER_DOCUMENT_DETAIL_DATA_ACCESS_FULL, \
	AUTHENTICATED_SELF_DOCUMENT_DETAIL_DATA_ACCESS_FULL, \
	STAFF_DOCUMENT_DETAIL_DATA_ACCESS_FULL, \
	ADMIN_DOCUMENT_DETAIL_DATA_ACCESS_FULL
from documentation.views import DocumentDetailView

def verify_documentdetail_request_returns_expected_data(self, request, whitelist):
	document_detail_view = DocumentDetailView.as_view()
	response = document_detail_view(request=request, id=1)
	assert_response_200(self, response)
	assert_has_data_field(self, response)
	assert_detail_response_matches_whitelist(response, whitelist=whitelist)
	return response

def perform_document_detail_get_request(self, whitelist, authenticate_function=None):
	request = make_get_request()
	if authenticate_function is not None:
		authenticate_function(request)
		verify_documentdetail_request_returns_expected_data(
		self, request=request, whitelist=whitelist
	)

def verify_unauthenticated_documentdetail_request_should_return_expected_data(self):
	perform_document_detail_get_request(
		self=self, whitelist=UNAUTHENTICATED_DOCUMENT_DETAIL_DATA_ACCESS_FULL
	)

def verify_authenticated_other_documentdetail_request_should_return_expected_data(self):
	perform_document_detail_get_request(
		self=self, authenticate_function=authenticate_viewer_user,
		whitelist=AUTHENTICATED_OTHER_DOCUMENT_DETAIL_DATA_ACCESS_FULL
	)

def verify_authenticated_author_documentdetail_request_should_return_expected_data(self):
	perform_document_detail_get_request(
		self=self, authenticate_function=authenticate_author_user,
		whitelist=AUTHENTICATED_SELF_DOCUMENT_DETAIL_DATA_ACCESS_FULL
	)

def verify_authenticated_staff_documentdetail_request_should_return_expected_data(self):
	perform_document_detail_get_request(
		self=self, authenticate_function=authenticate_staff,
		whitelist=STAFF_DOCUMENT_DETAIL_DATA_ACCESS_FULL
	)

def verify_authenticated_admin_documentdetail_request_should_return_expected_data(self):
	perform_document_detail_get_request(
		self=self, authenticate_function=authenticate_admin,
		whitelist=ADMIN_DOCUMENT_DETAIL_DATA_ACCESS_FULL
	)
