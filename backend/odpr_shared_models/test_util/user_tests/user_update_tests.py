# TODO: test pw-change, test if username/email change fails if already existing.
# TODO: pw-reset tests are omitted, due to complexity.
# TODO: maybe add a test which verifies that the pw is never returned.

from odpr_shared_models.test_util.user_tests.test_util import perform_post_and_retrieve_and_analyze, perform_put_and_retrieve_and_analyze
from odpr_shared_models.test_util.test_util import AUTHOR, STAFF, ADMIN, VIEWER, GUEST, CUSTOM_ID
from odpr_shared_models.test_util.user_tests.test_data import modify_existing_user, create_user_test_data

def create_and_update_user(
	self, authenticated=True, expected_success=True, user_type_write=AUTHOR, user_type_retrieve=AUTHOR
):
	test_data, normalized_test_data = create_user_test_data()
	response = perform_post_and_retrieve_and_analyze(self, test_data, normalized_test_data, user_type_retrieve=CUSTOM_ID)
	user_id = response.data['id']
	update_test_data, normalized_update_test_data = modify_existing_user(response.data)
	return perform_put_and_retrieve_and_analyze(
		self=self, test_data=update_test_data, normalized_test_data=normalized_update_test_data,
		authenticated=authenticated, expected_success=expected_success, user_type_write=user_type_write,
		user_type_retrieve=user_type_retrieve, custom_user_id=user_id
	)

def verify_unauthenticated_user_update_fails(self):
	create_and_update_user(self=self, authenticated=False, expected_success=False, user_type_write=GUEST)

def verify_authenticated_viewer_user_update_fails(self):
	create_and_update_user(self=self, expected_success=False, user_type_write=VIEWER)

def verify_authenticated_author_user_update_succeeds(self):
	create_and_update_user(self=self, user_type_write=CUSTOM_ID, user_type_retrieve=CUSTOM_ID)

def verify_authenticated_author_cannot_update_readonly_fields(self):
	test_data, normalized_test_data = create_user_test_data()
	response = perform_post_and_retrieve_and_analyze(self, test_data, normalized_test_data, user_type_retrieve=CUSTOM_ID)
	user_id = response.data['id']
	update_test_data, normalized_update_test_data = modify_existing_user(response.data)
	update_test_data.update({'password': 'trying to update password via normal user update view'})
	update_test_data.update({'is_admin': 'trying to admin status'})
	response = perform_put_and_retrieve_and_analyze(
		self, update_test_data, normalized_update_test_data, expected_success=True, custom_user_id=user_id,
		user_type_write=CUSTOM_ID, user_type_retrieve=CUSTOM_ID
	)
	from accounts.models import User
	sc = User.objects.get(pk=response.data['id'])
	if hasattr(sc, 'password'):
		self.assertNotEqual(sc.password, 'trying to update password via normal user update view')
	self.assertNotEqual(sc.is_admin, 'trying to admin status')

def verify_authenticated_staff_can_update_other_user(self):
	create_and_update_user(self=self, user_type_write=STAFF, user_type_retrieve=STAFF)

def verify_authenticated_admin_can_update_other_user(self):
	create_and_update_user(self=self, user_type_write=ADMIN, user_type_retrieve=ADMIN)
