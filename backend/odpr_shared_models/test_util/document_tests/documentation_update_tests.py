from odpr_shared_models.test_util.document_tests.test_util import perform_post_and_retrieve_and_analyze, perform_put_and_retrieve_and_analyze
from odpr_shared_models.test_util.test_util import AUTHOR, STAFF, ADMIN, VIEWER
from odpr_shared_models.test_util.document_tests.test_data import create_complex_test_data, modify_existing_document, normalize_list
from documentation.models import DocumentationTag

def create_and_update_document(
	self, authenticated=True, expected_success=True, user_type=AUTHOR
):
	test_data, normalized_test_data = create_complex_test_data()
	response = perform_post_and_retrieve_and_analyze(self, test_data, normalized_test_data)
	update_test_data, normalized_update_test_data = modify_existing_document(response.data)
	return perform_put_and_retrieve_and_analyze(
		self=self, test_data=update_test_data, normalized_test_data=normalized_update_test_data,
		authenticated=authenticated, expected_success=expected_success, user_type=user_type
	)

def verify_unauthenticated_document_update_fails(self):
	create_and_update_document(self=self, authenticated=False, expected_success=False)

def verify_authenticated_other_user_document_update_fails(self):
	create_and_update_document(self=self, expected_success=False, user_type=VIEWER)

def verify_authenticated_author_document_update_succeeds(self):
	create_and_update_document(self=self)

def verify_authenticated_author_cannot_update_readonly_fields(self):
	""" Note: these are only pseudo-readonly fields, e.g. fields which can be retrieved but are neither listed as
		fields in the serializer nor as readonly fields. There are no readonly fields in the serializer to be used ...
		Two fields in the model which are readonly are: visit_count and download_count.
	"""
	test_data, normalized_test_data = create_complex_test_data()
	response = perform_post_and_retrieve_and_analyze(self, test_data, normalized_test_data)
	update_test_data, normalized_update_test_data = modify_existing_document(response.data)
	update_test_data.update({'visit_count': 5050})
	response = perform_put_and_retrieve_and_analyze(
		self, update_test_data, normalized_update_test_data, expected_success=True
	)
	from documentation.models import Document
	sc = Document.objects.get(pk=response.data['id'])
	self.assertNotEqual(sc.visit_count, 5050)

def verify_authenticated_staff_can_update_other_user_document(self):
	create_and_update_document(self=self, user_type=STAFF)

def verify_authenticated_admin_can_update_other_user_document(self):
	create_and_update_document(self=self, user_type=ADMIN)

def verify_authenticated_author_document_update_with_new_elements_succeeds(self):
	test_data, normalized_test_data = create_complex_test_data()
	response = perform_post_and_retrieve_and_analyze(self, test_data, normalized_test_data)
	update_test_data, normalized_update_test_data = modify_existing_document(response.data)
	update_test_data.update(
		{'tags': [
			{'tag': 'Very New Testy Tag'},
			{'tag': 'Another New Testy Tag'},
		]}
	)
	normalized_tags = normalize_list(update_test_data['tags'], 'tag', DocumentationTag)
	normalized_update_test_data.update({'tags': normalized_tags})
	perform_put_and_retrieve_and_analyze(
		self, update_test_data, normalized_update_test_data
	)
