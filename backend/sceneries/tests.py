from django.test import TestCase
from vuedj.urls import urlpatterns as app_patterns
from django.test.utils import override_settings
from rest_framework.test import APITestCase
from django.urls import set_urlconf
from odpr_shared_models.test_util.scenery_tests.scenery_list_tests import \
	verify_unauthenticated_scenerylist_request_should_return_expected_data, \
	verify_authenticated_scenerylist_request_should_return_expected_data, \
	verify_staff_scenerylist_request_should_return_expected_data, \
	verify_admin_scenerylist_request_should_return_expected_data
from odpr_shared_models.test_util.scenery_tests.scenery_detail_tests import \
	verify_unauthenticated_scenerydetail_request_should_return_expected_data, \
	verify_authenticated_other_scenerydetail_request_should_return_expected_data, \
	verify_authenticated_author_scenerydetail_request_should_return_expected_data, \
	verify_authenticated_staff_scenerydetail_request_should_return_expected_data, \
	verify_authenticated_admin_scenerydetail_request_should_return_expected_data
from odpr_shared_models.test_util.scenery_tests.scenery_create_tests import \
	verify_unauthenticated_scenery_create_fails, \
	verify_authenticated_scenery_create_succeeds, \
	verify_authenticated_scenery_create_fails, \
	verify_scenery_create_ignores_unexpected_argument
from odpr_shared_models.test_util.scenery_tests.scenery_update_tests import \
	verify_unauthenticated_scenery_update_fails, \
	verify_authenticated_other_user_scenery_update_fails, \
	verify_authenticated_author_scenery_update_succeeds, \
	verify_authenticated_author_cannot_update_readonly_fields, \
	verify_authenticated_staff_can_update_other_user_scenery, \
	verify_authenticated_admin_can_update_other_user_scenery, \
	verify_authenticated_author_scenery_update_with_new_elements_succeeds
from odpr_shared_models.test_util.scenery_tests.scenery_delete_tests import \
	verify_unauthenticated_scenery_delete_fails, \
	verify_authenticated_viewer_scenery_delete_fails, \
	verify_authenticated_author_scenery_delete_succeeds, \
	verify_authenticated_staff_can_delete_other_user_scenery, \
	verify_authenticated_admin_can_delete_other_user_scenery
from odpr_shared_models.test_util.scenery_tests.scenery_image_tests import \
	verify_scenery_create_image_create_succeeds

class SceneryListTests(TestCase):
	fixtures = (
		'user_fixtures',
		'badge_fixtures',
		'text_with_history_fixtures',
		'filter_property_fixtures',
		'filter_properties_fixtures',
		'scenery_fixtures',
		'tag_fixtures',
	)

	def test_unauthenticated_scenery_list_matches_expected_data(self):
		print('=================== Test 1:  Scenery list should return correct data ======================================')
		verify_unauthenticated_scenerylist_request_should_return_expected_data(self)
		print('================================================= End of Test 1 ===========================================')

	def test_authenticated_scenery_list_matches_expected_data(self):
		print('=================== Test 2:  Scenery list should return correct data ======================================')
		verify_authenticated_scenerylist_request_should_return_expected_data(self)
		print('================================================= End of Test 2 ===========================================')

	def test_staff_scenery_list_matches_expected_data(self):
		print('=================== Test 3:  Scenery list should return correct data ======================================')
		verify_staff_scenerylist_request_should_return_expected_data(self)
		print('================================================= End of Test 3 ===========================================')

	def test_admin_scenery_list_matches_expected_data(self):
		print('=================== Test 4:  Scenery list should return correct data ======================================')
		verify_admin_scenerylist_request_should_return_expected_data(self)
		print('================================================= End of Test 4 ===========================================')


class SceneryDetailTests(TestCase):
	fixtures = (
		'user_fixtures',
		'badge_fixtures',
		'text_with_history_fixtures',
		'filter_property_fixtures',
		'filter_properties_fixtures',
		'scenery_fixtures',
		'tag_fixtures',
	)

	def test_unauthenticated_scenery_detail_matches_expected_data(self):
		print('=================== Test 1:  Scenery detail should return correct data ====================================')
		verify_unauthenticated_scenerydetail_request_should_return_expected_data(self)
		print('================================================= End of Test 1 ===========================================')

	def test_authenticated_other_user_scenery_detail_matches_expected_data(self):
		print('=================== Test 2:  Scenery detail should return correct data ====================================')
		verify_authenticated_other_scenerydetail_request_should_return_expected_data(self)
		print('================================================= End of Test 2 ===========================================')

	def test_authenticated_author_scenery_detail_matches_expected_data(self):
		print('=================== Test 3:  Scenery detail should return correct data ====================================')
		verify_authenticated_author_scenerydetail_request_should_return_expected_data(self)
		print('================================================= End of Test 3 ===========================================')

	def test_staff_scenery_detail_matches_expected_data(self):
		print('=================== Test 4:  Scenery detail should return correct data ====================================')
		verify_authenticated_staff_scenerydetail_request_should_return_expected_data(self)
		print('================================================= End of Test 4 ===========================================')

	def test_admin_scenery_detail_matches_expected_data(self):
		print('=================== Test 5:  Scenery detail should return correct data ====================================')
		verify_authenticated_admin_scenerydetail_request_should_return_expected_data(self)
		print('================================================= End of Test 5 ===========================================')


class SceneryCreateTests(TestCase):
	fixtures = (
		'user_fixtures',
		'badge_fixtures',
		'text_with_history_fixtures',
		'filter_property_fixtures',
		'filter_properties_fixtures',
		'scenery_fixtures',
		'tag_fixtures',
	)

	def test_unauthenticated_scenery_create_fails(self):
		print('=================== Test 1:  Scenery create should fail ===================================================')
		verify_unauthenticated_scenery_create_fails(self)
		print('================================================= End of Test 1 ===========================================')

	def test_authenticated_user_scenery_create_should_succeed(self):
		print('=================== Test 2:  Scenery create should create scenery =========================================')
		verify_authenticated_scenery_create_succeeds(self)
		# TODO modify this test so that View will use File/Image Create Serializer instead of SceneryCreateSerializer
		# TODO and the scenery itself is just nested content of the file creation.
		print('================================================= End of Test 2 ===========================================')

	def test_authenticated_user_scenery_create_with_unexpected_additional_argument_should_succeed(self):
		''' Additional arguments are simply ignored '''
		print('=================== Test 3:  Scenery create should create scenery unexpected arg ==========================')
		verify_scenery_create_ignores_unexpected_argument(self)
		print('================================================= End of Test 3 ===========================================')

	def test_authenticated_user_scenery_create_should_fail(self):
		print('=================== Test 4:  Scenery create should fail ===================================================')
		verify_authenticated_scenery_create_fails(self)
		print('================================================= End of Test 4 ===========================================')


#urlpatterns = app_patterns + []  # Add custom patterns if needed.

#@override_settings(ROOT_URLCONF=__name__)
# class FileTests(APITestCase):
# 	#urls = 'vuedj.urls'
#
# 	fixtures = (
# 		'user_fixtures',
# 		'badge_fixtures',
# 		'text_with_history_fixtures',
# 		'filter_property_fixtures',
# 		'filter_properties_fixtures',
# 		'scenery_fixtures',
# 		'tag_fixtures',
# 	)
#
# 	@classmethod
# 	def setUpClass(cls):
# 		super().setUpClass()
# 		set_urlconf('vuedj.urls')
#
# 	def test_authenticated_user_scenery_image_create_should_succeed(self):
# 		print('=================== Test 5:  Scenery Image create should succeed ==========================================')
#
# 		verify_scenery_create_image_create_succeeds(self)
# 		print('================================================= End of Test 5 ===========================================')


class SceneryUpdateTests(TestCase):
	fixtures = (
		'user_fixtures',
		'badge_fixtures',
		'text_with_history_fixtures',
		'filter_property_fixtures',
		'filter_properties_fixtures',
		'scenery_fixtures',
		'tag_fixtures',
	)

	def test_unauthenticated_scenery_update_fails(self):
		print('=================== Test 1:  Scenery update should fail ===================================================')
		verify_unauthenticated_scenery_update_fails(self)
		print('================================================= End of Test 1 ===========================================')

	def test_authenticated_other_user_scenery_update_should_return_error(self):
		print('=================== Test 2:  Scenery update should return permission error ================================')
		verify_authenticated_other_user_scenery_update_fails(self)
		print('================================================= End of Test 2 ===========================================')

	def test_authenticated_author_scenery_update_should_succeed(self):
		print('=================== Test 3:  Scenery update should succeed ================================================')
		verify_authenticated_author_scenery_update_succeeds(self)
		print('================================================= End of Test 3 ===========================================')

	def test_authenticated_author_scenery_update_read_only_should_succeed(self):
		print('=================== Test 4:  Scenery update on readonly fields should ignore readonly fields and succeed ==')
		verify_authenticated_author_cannot_update_readonly_fields(self)
		print('================================================= End of Test 4 ===========================================')

	def test_authenticated_staff_scenery_update_other_author_should_succeed(self):
		print('=================== Test 5:  Scenery update by staff of other user should succeed =========================')
		verify_authenticated_staff_can_update_other_user_scenery(self)
		print('================================================= End of Test 5 ===========================================')

	def test_authenticated_admin_scenery_update_other_author_should_succeed(self):
		print('=================== Test 6:  Scenery update by admin of other user should succeed =========================')
		verify_authenticated_admin_can_update_other_user_scenery(self)
		print('================================================= End of Test 6 ===========================================')

	def test_authenticated_author_scenery_update_with_new_elements_should_succeed(self):
		print('=================== Test 7:  Scenery update by with new elements to be created should work ================')
		verify_authenticated_author_scenery_update_with_new_elements_succeeds(self)
		print('================================================= End of Test 7 ===========================================')


class SceneryDeleteTests(TestCase):
	fixtures = (
		'user_fixtures',
		'badge_fixtures',
		'text_with_history_fixtures',
		'filter_property_fixtures',
		'filter_properties_fixtures',
		'scenery_fixtures',
		'tag_fixtures',
	)

	def test_unauthenticated_scenery_delete_fails(self):
		print('=================== Test 1:  Scenery delete should redirect to login ======================================')
		verify_unauthenticated_scenery_delete_fails(self)
		print('================================================= End of Test 1 ===========================================')

	def test_authenticated_other_user_scenery_delete_should_return_error(self):
		print('=================== Test 2:  Scenery delete should return permission error ================================')
		verify_authenticated_viewer_scenery_delete_fails(self)
		print('================================================= End of Test 2 ===========================================')

	def test_authenticated_author_scenery_delete_should_succeed(self):
		print('=================== Test 3:  Scenery delete should succeed ================================================')
		verify_authenticated_author_scenery_delete_succeeds(self)
		print('================================================= End of Test 3 ===========================================')

	def test_authenticated_staff_scenery_delete_other_author_should_succeed(self):
		print('=================== Test 4:  Scenery delete by staff of other user should succeed =========================')
		verify_authenticated_staff_can_delete_other_user_scenery(self)
		print('================================================= End of Test 4 ===========================================')

	def test_authenticated_admin_scenery_delete_other_author_should_succeed(self):
		print('=================== Test 5:  Scenery delete by admin of other user should succeed =========================')
		verify_authenticated_admin_can_delete_other_user_scenery(self)
		print('================================================= End of Test 5 ===========================================')
