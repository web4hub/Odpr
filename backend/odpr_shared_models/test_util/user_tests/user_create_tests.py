from odpr_shared_models.test_util.user_tests.test_util import perform_post_and_retrieve_and_analyze
from odpr_shared_models.test_util.user_tests.test_data import create_user_test_data
from odpr_shared_models.test_util.test_util import AUTHOR, ADMIN

def verify_unauthenticated_user_create_succeeds(self):
	test_data, normalized_test_data = create_user_test_data()
	perform_post_and_retrieve_and_analyze(
		self=self, test_data=test_data, normalized_test_data=normalized_test_data,
		authenticated_write=False, authenticated_retrieve=True, expected_success=True,
		user_type_retrieve=ADMIN
	)

def verify_user_create_ignores_unexpected_argument(self):
	test_data, normalized_test_data = create_user_test_data()
	test_data.update({'unexpected': 'argument'})
	perform_post_and_retrieve_and_analyze(
		self=self, test_data=test_data, normalized_test_data=normalized_test_data,
		authenticated_write=False, authenticated_retrieve=True, expected_success=True,
		user_type_retrieve=ADMIN
	)

def test_user_create_fails_due_missing_argument(self):
	test_data, normalized_test_data = create_user_test_data()
	test_data.pop('email', None)  # email is not optional in model
	perform_post_and_retrieve_and_analyze(
		self=self, test_data=test_data, normalized_test_data=normalized_test_data,
		authenticated_write=False, expected_success=False
	)

def verify_authenticated_user_create_fails(self):
	test_data, normalized_test_data = create_user_test_data()
	perform_post_and_retrieve_and_analyze(
		self=self, test_data=test_data, normalized_test_data=normalized_test_data,
		authenticated_write=True, expected_success=False,	user_type_write=AUTHOR
	)
