from django.test import TestCase
from odpr_shared_models.test_util.document_tests.documentation_list_tests import \
	verify_unauthenticated_documentlist_request_should_return_expected_data, \
	verify_authenticated_documentlist_request_should_return_expected_data, \
	verify_staff_documentlist_request_should_return_expected_data, \
	verify_admin_documentlist_request_should_return_expected_data
from odpr_shared_models.test_util.document_tests.documentation_detail_tests import \
	verify_unauthenticated_documentdetail_request_should_return_expected_data, \
	verify_authenticated_other_documentdetail_request_should_return_expected_data, \
	verify_authenticated_author_documentdetail_request_should_return_expected_data, \
	verify_authenticated_staff_documentdetail_request_should_return_expected_data, \
	verify_authenticated_admin_documentdetail_request_should_return_expected_data
from odpr_shared_models.test_util.document_tests.documentation_create_tests import \
	verify_unauthenticated_document_create_fails, \
	verify_authenticated_document_create_succeeds, \
	verify_authenticated_document_create_fails, \
	verify_document_create_ignores_unexpected_argument
from odpr_shared_models.test_util.document_tests.documentation_update_tests import \
	verify_unauthenticated_document_update_fails, \
	verify_authenticated_other_user_document_update_fails, \
	verify_authenticated_author_document_update_succeeds, \
	verify_authenticated_author_cannot_update_readonly_fields, \
	verify_authenticated_staff_can_update_other_user_document, \
	verify_authenticated_admin_can_update_other_user_document, \
	verify_authenticated_author_document_update_with_new_elements_succeeds
from odpr_shared_models.test_util.document_tests.documentation_delete_tests import \
	verify_unauthenticated_document_delete_fails, \
	verify_authenticated_viewer_document_delete_fails, \
	verify_authenticated_author_document_delete_succeeds, \
	verify_authenticated_staff_can_delete_other_user_document, \
	verify_authenticated_admin_can_delete_other_user_document

class DocumentListTests(TestCase):
	fixtures = (
		'user_fixtures',
		'badge_fixtures',
		'text_with_history_fixtures',
		'filter_property_fixtures',
		'filter_properties_fixtures',
		'document_fixtures',
		'documentation_tag_fixtures',
	)

	def test_unauthenticated_document_list_matches_expected_data(self):
		print('=================== Test 1:  Document list should return correct data =====================================')
		verify_unauthenticated_documentlist_request_should_return_expected_data(self)
		print('================================================= End of Test 1 ===========================================')

	def test_authenticated_document_list_matches_expected_data(self):
		print('=================== Test 2:  Document list should return correct data =====================================')
		verify_authenticated_documentlist_request_should_return_expected_data(self)
		print('================================================= End of Test 2 ===========================================')

	def test_staff_document_list_matches_expected_data(self):
		print('=================== Test 3:  Document list should return correct data =====================================')
		verify_staff_documentlist_request_should_return_expected_data(self)
		print('================================================= End of Test 3 ===========================================')

	def test_admin_document_list_matches_expected_data(self):
		print('=================== Test 4:  Document list should return correct data =====================================')
		verify_admin_documentlist_request_should_return_expected_data(self)
		print('================================================= End of Test 4 ===========================================')


class DocumentDetailTests(TestCase):
	fixtures = (
		'user_fixtures',
		'badge_fixtures',
		'text_with_history_fixtures',
		'filter_property_fixtures',
		'filter_properties_fixtures',
		'document_fixtures',
		'documentation_tag_fixtures',
	)

	def test_unauthenticated_document_detail_matches_expected_data(self):
		print('=================== Test 1:  Document detail should return correct data ===================================')
		verify_unauthenticated_documentdetail_request_should_return_expected_data(self)
		print('================================================= End of Test 1 ===========================================')

	def test_authenticated_other_user_document_detail_matches_expected_data(self):
		print('=================== Test 2:  Document detail should return correct data ===================================')
		verify_authenticated_other_documentdetail_request_should_return_expected_data(self)
		print('================================================= End of Test 2 ===========================================')

	def test_authenticated_author_document_detail_matches_expected_data(self):
		print('=================== Test 3:  Document detail should return correct data ===================================')
		verify_authenticated_author_documentdetail_request_should_return_expected_data(self)
		print('================================================= End of Test 3 ===========================================')

	def test_staff_document_detail_matches_expected_data(self):
		print('=================== Test 4:  Document detail should return correct data ===================================')
		verify_authenticated_staff_documentdetail_request_should_return_expected_data(self)
		print('================================================= End of Test 4 ===========================================')

	def test_admin_document_detail_matches_expected_data(self):
		print('=================== Test 5:  Document detail should return correct data ===================================')
		verify_authenticated_admin_documentdetail_request_should_return_expected_data(self)
		print('================================================= End of Test 5 ===========================================')


class DocumentCreateTests(TestCase):
	fixtures = (
		'user_fixtures',
		'badge_fixtures',
		'text_with_history_fixtures',
		'filter_property_fixtures',
		'filter_properties_fixtures',
		'document_fixtures',
		'documentation_tag_fixtures',
	)

	def test_unauthenticated_document_create_fails(self):
		print('=================== Test 1:  Document create should fail ==================================================')
		verify_unauthenticated_document_create_fails(self)
		print('================================================= End of Test 1 ===========================================')

	def test_authenticated_user_document_create_should_succeed(self):
		print('=================== Test 2:  Document create should create document =======================================')
		verify_authenticated_document_create_succeeds(self)
		# TODO modify this test so that View will use File/Image Create Serializer instead of DocumentCreateSerializer
		# TODO and the document itself is just nested content of the file creation.
		print('================================================= End of Test 2 ===========================================')

	def test_authenticated_user_document_create_with_unexpected_additional_argument_should_succeed(self):
		''' Additional arguments are simply ignored '''
		print('=================== Test 3:  Document create should create document unexpected arg ========================')
		verify_document_create_ignores_unexpected_argument(self)
		print('================================================= End of Test 3 ===========================================')

	def test_authenticated_user_document_create_should_fail(self):
		print('=================== Test 4:  Document create should fail ==================================================')
		verify_authenticated_document_create_fails(self)
		print('================================================= End of Test 4 ===========================================')


class DocumentUpdateTests(TestCase):
	fixtures = (
		'user_fixtures',
		'badge_fixtures',
		'text_with_history_fixtures',
		'filter_property_fixtures',
		'filter_properties_fixtures',
		'document_fixtures',
		'documentation_tag_fixtures',
	)

	def test_unauthenticated_document_update_fails(self):
		print('=================== Test 1:  Document update should fail ==================================================')
		verify_unauthenticated_document_update_fails(self)
		print('================================================= End of Test 1 ===========================================')

	def test_authenticated_other_user_document_update_should_return_error(self):
		print('=================== Test 2:  Document update should return permission error ===============================')
		verify_authenticated_other_user_document_update_fails(self)
		print('================================================= End of Test 2 ===========================================')

	def test_authenticated_author_document_update_should_succeed(self):
		print('=================== Test 3:  Document update should succeed ===============================================')
		verify_authenticated_author_document_update_succeeds(self)
		print('================================================= End of Test 3 ===========================================')

	def test_authenticated_author_document_update_read_only_should_succeed(self):
		print('=================== Test 4:  Document update on readonly fields should ignore readonly fields and succeed =')
		verify_authenticated_author_cannot_update_readonly_fields(self)
		print('================================================= End of Test 4 ===========================================')

	def test_authenticated_staff_document_update_other_author_should_succeed(self):
		print('=================== Test 5:  Document update by staff of other user should succeed ========================')
		verify_authenticated_staff_can_update_other_user_document(self)
		print('================================================= End of Test 5 ===========================================')

	def test_authenticated_admin_document_update_other_author_should_succeed(self):
		print('=================== Test 6:  Document update by admin of other user should succeed ========================')
		verify_authenticated_admin_can_update_other_user_document(self)
		print('================================================= End of Test 6 ===========================================')

	def test_authenticated_author_document_update_with_new_elements_should_succeed(self):
		print('=================== Test 7:  Document update by with new elements to be created should work ===============')
		verify_authenticated_author_document_update_with_new_elements_succeeds(self)
		print('================================================= End of Test 7 ===========================================')


class DocumentDeleteTests(TestCase):
	fixtures = (
		'user_fixtures',
		'badge_fixtures',
		'text_with_history_fixtures',
		'filter_property_fixtures',
		'filter_properties_fixtures',
		'document_fixtures',
		'documentation_tag_fixtures',
	)

	def test_unauthenticated_document_delete_fails(self):
		print('=================== Test 1:  Document delete should redirect to login =====================================')
		verify_unauthenticated_document_delete_fails(self)
		print('================================================= End of Test 1 ===========================================')

	def test_authenticated_other_user_document_delete_should_return_error(self):
		print('=================== Test 2:  Document delete should return permission error ===============================')
		verify_authenticated_viewer_document_delete_fails(self)
		print('================================================= End of Test 2 ===========================================')

	def test_authenticated_author_document_delete_should_succeed(self):
		print('=================== Test 3:  Document delete should succeed ===============================================')
		verify_authenticated_author_document_delete_succeeds(self)
		print('================================================= End of Test 3 ===========================================')

	def test_authenticated_staff_document_delete_other_author_should_succeed(self):
		print('=================== Test 4:  Document delete by staff of other user should succeed ========================')
		verify_authenticated_staff_can_delete_other_user_document(self)
		print('================================================= End of Test 4 ===========================================')

	def test_authenticated_admin_document_delete_other_author_should_succeed(self):
		print('=================== Test 5:  Document delete by admin of other user should succeed ========================')
		verify_authenticated_admin_can_delete_other_user_document(self)
		print('================================================= End of Test 5 ===========================================')
