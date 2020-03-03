from odpr_shared_models.test_util.scenery_tests.test_util import post_scenery_test_data_and_verify_status_code, \
	perform_post_and_retrieve_and_analyze
from odpr_shared_models.test_util.scenery_tests.test_data import create_scenery_test_data, create_complex_test_data

def verify_unauthenticated_scenery_create_fails(self):
	post_scenery_test_data_and_verify_status_code(
		self=self, test_data=create_scenery_test_data(), authenticated=False, expected_success=False
	)

def test_scenery_create_simple_keys_only(self):
	test_data, normalized_test_data = create_scenery_test_data()
	perform_post_and_retrieve_and_analyze(self, test_data, normalized_test_data)

def test_scenery_create_multiple_keys_only(self):
	test_data, normalized_test_data = create_scenery_test_data(
		effects=[1, 2, 5],
		materials=[3, 6],
		lights=[7, 4],
		tags=[2, 3, 11, 12]
	)
	perform_post_and_retrieve_and_analyze(self, test_data, normalized_test_data)

def test_scenery_create_mixed_keys(self):
	test_data, normalized_test_data = create_complex_test_data()
	perform_post_and_retrieve_and_analyze(self, test_data, normalized_test_data)

def verify_authenticated_scenery_create_succeeds(self):
	test_scenery_create_simple_keys_only(self)
	test_scenery_create_multiple_keys_only(self)
	test_scenery_create_mixed_keys(self)

	# TODO: add preview images and files to createSerializer. (as required)
	# Note: this can be done by posting a file, with a nested Scenery dict, thus the serializer will do it...
	# Nice benefit: if the file upload is not finished, the scenery will automatically NOT be posted.

def verify_scenery_create_ignores_unexpected_argument(self):
	test_data, normalized_test_data = create_scenery_test_data()
	test_data.update({'unexpected_argument': 'should_be_ignored'})
	post_scenery_test_data_and_verify_status_code(
		self=self, test_data=test_data
	)

def verify_create_serializer_succeeds_if_optional_args_missing(self):
	test_data, normalized_test_data = create_scenery_test_data()
	test_data.update({'description': {}})  # missing content, but optional in Model.
	post_scenery_test_data_and_verify_status_code(
		self=self, test_data=test_data
	)

def test_scenery_create_fails_due_missing_argument(self):
	test_data, normalized_test_data = create_scenery_test_data()
	test_data.pop('title', None)  # title is not optional in model
	post_scenery_test_data_and_verify_status_code(
		self=self, test_data=test_data, expected_success=False
	)

def test_scenery_create_fails_due_invalid_argument_value(self):
	test_data, normalized_test_data = create_scenery_test_data(
		title={'invalid': 'value, expected string, got dict...'}, strict_types=False
	)
	post_scenery_test_data_and_verify_status_code(
		self=self, test_data=test_data, expected_success=False
	)

def test_scenery_create_fails_due_pk_of_nonexistent_object(self):
	test_data, normalized_test_data = create_scenery_test_data(tags=[2, 3, 11, 120, {'tag': 'Create-And-Reuse-Test'}])
	post_scenery_test_data_and_verify_status_code(
		self=self, test_data=test_data, expected_success=False
	)

def verify_authenticated_scenery_create_fails(self):
	"""
		Possible cases of a failing post:
		* Request data is missing needed parameter
		* Request data contains invalid parameter (a parameter which is never expected by its type or by invalid value)
		* Request data contains pk of non existent object
	"""
	test_scenery_create_fails_due_missing_argument(self)
	test_scenery_create_fails_due_invalid_argument_value(self)
	test_scenery_create_fails_due_pk_of_nonexistent_object(self)
