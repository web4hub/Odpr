from django.test import TestCase
from odpr_shared_models.test_util.request_tests.request_list_tests import \
	verify_unauthenticated_requestlist_request_should_return_expected_data, \
	verify_authenticated_requestlist_request_should_return_expected_data, \
	verify_staff_requestlist_request_should_return_expected_data, \
	verify_admin_requestlist_request_should_return_expected_data
from odpr_shared_models.test_util.request_tests.request_detail_tests import \
	verify_unauthenticated_requestdetail_request_should_return_expected_data, \
	verify_authenticated_other_requestdetail_request_should_return_expected_data, \
	verify_authenticated_author_requestdetail_request_should_return_expected_data, \
	verify_authenticated_staff_requestdetail_request_should_return_expected_data, \
	verify_authenticated_admin_requestdetail_request_should_return_expected_data
from odpr_shared_models.test_util.request_tests.request_create_tests import \
	verify_unauthenticated_request_create_fails, \
	verify_authenticated_request_create_succeeds, \
	verify_authenticated_request_create_fails, \
	verify_request_create_ignores_unexpected_argument
from odpr_shared_models.test_util.request_tests.request_update_tests import \
	verify_unauthenticated_request_update_fails, \
	verify_authenticated_other_user_request_update_fails, \
	verify_authenticated_author_request_update_succeeds, \
	verify_authenticated_author_cannot_update_readonly_fields, \
	verify_authenticated_staff_can_update_other_user_request, \
	verify_authenticated_admin_can_update_other_user_request, \
	verify_authenticated_author_request_update_with_new_elements_succeeds
from odpr_shared_models.test_util.request_tests.request_delete_tests import \
	verify_unauthenticated_request_delete_fails, \
	verify_authenticated_viewer_request_delete_fails, \
	verify_authenticated_author_request_delete_succeeds, \
	verify_authenticated_staff_can_delete_other_user_request, \
	verify_authenticated_admin_can_delete_other_user_request

class RequestListTests(TestCase):
	fixtures = (
		'user_fixtures',
		'badge_fixtures',
		'text_with_history_fixtures',
		'filter_property_fixtures',
		'filter_properties_fixtures',
		'request_fixtures',
		'tag_fixtures',
	)

	def test_unauthenticated_request_list_matches_expected_data(self):
		print('=================== Test 1:  Request list should return correct data ======================================')
		verify_unauthenticated_requestlist_request_should_return_expected_data(self)
		print('================================================= End of Test 1 ===========================================')

	def test_authenticated_request_list_matches_expected_data(self):
		print('=================== Test 2:  Request list should return correct data ======================================')
		verify_authenticated_requestlist_request_should_return_expected_data(self)
		print('================================================= End of Test 2 ===========================================')

	def test_staff_request_list_matches_expected_data(self):
		print('=================== Test 3:  Request list should return correct data ======================================')
		verify_staff_requestlist_request_should_return_expected_data(self)
		print('================================================= End of Test 3 ===========================================')

	def test_admin_request_list_matches_expected_data(self):
		print('=================== Test 4:  Request list should return correct data ======================================')
		verify_admin_requestlist_request_should_return_expected_data(self)
		print('================================================= End of Test 4 ===========================================')


class RequestDetailTests(TestCase):
	fixtures = (
		'user_fixtures',
		'badge_fixtures',
		'text_with_history_fixtures',
		'filter_property_fixtures',
		'filter_properties_fixtures',
		'request_fixtures',
		'tag_fixtures',
	)

	def test_unauthenticated_request_detail_matches_expected_data(self):
		print('=================== Test 1:  Request detail should return correct data ====================================')
		verify_unauthenticated_requestdetail_request_should_return_expected_data(self)
		print('================================================= End of Test 1 ===========================================')

	def test_authenticated_other_user_request_detail_matches_expected_data(self):
		print('=================== Test 2:  Request detail should return correct data ====================================')
		verify_authenticated_other_requestdetail_request_should_return_expected_data(self)
		print('================================================= End of Test 2 ===========================================')

	def test_authenticated_author_request_detail_matches_expected_data(self):
		print('=================== Test 3:  Request detail should return correct data ====================================')
		verify_authenticated_author_requestdetail_request_should_return_expected_data(self)
		print('================================================= End of Test 3 ===========================================')

	def test_staff_request_detail_matches_expected_data(self):
		print('=================== Test 4:  Request detail should return correct data ====================================')
		verify_authenticated_staff_requestdetail_request_should_return_expected_data(self)
		print('================================================= End of Test 4 ===========================================')

	def test_admin_request_detail_matches_expected_data(self):
		print('=================== Test 5:  Request detail should return correct data ====================================')
		verify_authenticated_admin_requestdetail_request_should_return_expected_data(self)
		print('================================================= End of Test 5 ===========================================')


class RequestCreateTests(TestCase):
	fixtures = (
		'user_fixtures',
		'badge_fixtures',
		'text_with_history_fixtures',
		'filter_property_fixtures',
		'filter_properties_fixtures',
		'request_fixtures',
		'tag_fixtures',
	)

	def test_unauthenticated_request_create_fails(self):
		print('=================== Test 1:  Request create should fail ===================================================')
		verify_unauthenticated_request_create_fails(self)
		print('================================================= End of Test 1 ===========================================')

	def test_authenticated_user_request_create_should_succeed(self):
		print('=================== Test 2:  Request create should create request =========================================')
		verify_authenticated_request_create_succeeds(self)
		# TODO modify this test so that View will use File/Image Create Serializer instead of RequestCreateSerializer
		# TODO and the request itself is just nested content of the file creation.
		print('================================================= End of Test 2 ===========================================')

	def test_authenticated_user_request_create_with_unexpected_additional_argument_should_succeed(self):
		''' Additional arguments are simply ignored '''
		print('=================== Test 3:  Request create should create request unexpected arg ==========================')
		verify_request_create_ignores_unexpected_argument(self)
		print('================================================= End of Test 3 ===========================================')

	def test_authenticated_user_request_create_should_fail(self):
		print('=================== Test 4:  Request create should fail ===================================================')
		verify_authenticated_request_create_fails(self)
		print('================================================= End of Test 4 ===========================================')


class RequestUpdateTests(TestCase):
	fixtures = (
		'user_fixtures',
		'badge_fixtures',
		'text_with_history_fixtures',
		'filter_property_fixtures',
		'filter_properties_fixtures',
		'request_fixtures',
		'tag_fixtures',
	)

	def test_unauthenticated_request_update_fails(self):
		print('=================== Test 1:  Request update should fail ===================================================')
		verify_unauthenticated_request_update_fails(self)
		print('================================================= End of Test 1 ===========================================')

	def test_authenticated_other_user_request_update_should_return_error(self):
		print('=================== Test 2:  Request update should return permission error ================================')
		verify_authenticated_other_user_request_update_fails(self)
		print('================================================= End of Test 2 ===========================================')

	def test_authenticated_author_request_update_should_succeed(self):
		print('=================== Test 3:  Request update should succeed ================================================')
		verify_authenticated_author_request_update_succeeds(self)
		print('================================================= End of Test 3 ===========================================')

	def test_authenticated_author_request_update_read_only_should_succeed(self):
		print('=================== Test 4:  Request update on readonly fields should ignore readonly fields and succeed ==')
		verify_authenticated_author_cannot_update_readonly_fields(self)
		print('================================================= End of Test 4 ===========================================')

	def test_authenticated_staff_request_update_other_author_should_succeed(self):
		print('=================== Test 5:  Request update by staff of other user should succeed =========================')
		verify_authenticated_staff_can_update_other_user_request(self)
		print('================================================= End of Test 5 ===========================================')

	def test_authenticated_admin_request_update_other_author_should_succeed(self):
		print('=================== Test 6:  Request update by admin of other user should succeed =========================')
		verify_authenticated_admin_can_update_other_user_request(self)
		print('================================================= End of Test 6 ===========================================')

	def test_authenticated_author_request_update_with_new_elements_should_succeed(self):
		print('=================== Test 7:  Request update by with new elements to be created should work ================')
		verify_authenticated_author_request_update_with_new_elements_succeeds(self)
		print('================================================= End of Test 7 ===========================================')


class RequestDeleteTests(TestCase):
	fixtures = (
		'user_fixtures',
		'badge_fixtures',
		'text_with_history_fixtures',
		'filter_property_fixtures',
		'filter_properties_fixtures',
		'request_fixtures',
		'tag_fixtures',
	)

	def test_unauthenticated_request_delete_fails(self):
		print('=================== Test 1:  Request delete should redirect to login ======================================')
		verify_unauthenticated_request_delete_fails(self)
		print('================================================= End of Test 1 ===========================================')

	def test_authenticated_other_user_request_delete_should_return_error(self):
		print('=================== Test 2:  Request delete should return permission error ================================')
		verify_authenticated_viewer_request_delete_fails(self)
		print('================================================= End of Test 2 ===========================================')

	def test_authenticated_author_request_delete_should_succeed(self):
		print('=================== Test 3:  Request delete should succeed ================================================')
		verify_authenticated_author_request_delete_succeeds(self)
		print('================================================= End of Test 3 ===========================================')

	def test_authenticated_staff_request_delete_other_author_should_succeed(self):
		print('=================== Test 4:  Request delete by staff of other user should succeed =========================')
		verify_authenticated_staff_can_delete_other_user_request(self)
		print('================================================= End of Test 4 ===========================================')

	def test_authenticated_admin_request_delete_other_author_should_succeed(self):
		print('=================== Test 5:  Request delete by admin of other user should succeed =========================')
		verify_authenticated_admin_can_delete_other_user_request(self)
		print('================================================= End of Test 5 ===========================================')
