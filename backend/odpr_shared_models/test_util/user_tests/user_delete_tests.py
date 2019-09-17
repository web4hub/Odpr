from odpr_shared_models.test_util.user_tests.test_util import \
	perform_post_and_retrieve_and_analyze, delete_user_instance_and_verify_status_code
from odpr_shared_models.test_util.test_util import AUTHOR, VIEWER, ADMIN, STAFF, CUSTOM_ID
from odpr_shared_models.test_util.user_tests.test_data import create_user_test_data
from accounts.models import User
from django.core.exceptions import ObjectDoesNotExist

def create_and_delete_user(
	self, authenticated=True, expected_success=True, user_type=AUTHOR
):
	test_data, normalized_test_data = create_user_test_data()
	response = perform_post_and_retrieve_and_analyze(self, test_data, normalized_test_data, user_type_retrieve=CUSTOM_ID)
	user_id = response.data['id']
	return delete_user_instance_and_verify_status_code(
		self=self, user_id=user_id, authenticated=authenticated,
		expected_success=expected_success, user_type=user_type, custom_user_id=user_id
	), user_id

def verify_unauthenticated_user_delete_fails(self):
	response, user_id = create_and_delete_user(
		self=self, authenticated=False, expected_success=False
	)
	User.objects.get(pk=user_id)

def verify_authenticated_viewer_user_delete_fails(self):
	response, user_id = create_and_delete_user(
		self=self, expected_success=False, user_type=VIEWER
	)
	User.objects.get(pk=user_id)

def verify_authenticated_author_user_delete_succeeds(self):
	response, user_id = create_and_delete_user(
		self=self, expected_success=True, user_type=CUSTOM_ID
	)
	self.assertRaises(ObjectDoesNotExist, User.objects.get, pk=user_id)

def verify_authenticated_staff_can_delete_other_user(self):
	response, user_id = create_and_delete_user(
		self=self, expected_success=True, user_type=STAFF
	)
	self.assertRaises(ObjectDoesNotExist, User.objects.get, pk=user_id)

def verify_authenticated_admin_can_delete_other_user(self):
	response, user_id = create_and_delete_user(
		self=self, expected_success=True, user_type=ADMIN
	)
	self.assertRaises(ObjectDoesNotExist, User.objects.get, pk=user_id)
