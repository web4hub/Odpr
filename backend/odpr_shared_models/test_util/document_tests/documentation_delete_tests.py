from odpr_shared_models.test_util.document_tests.test_util import \
	perform_post_and_retrieve_and_analyze, delete_document_instance_and_verify_status_code
from odpr_shared_models.test_util.test_util import AUTHOR, VIEWER, ADMIN, STAFF
from odpr_shared_models.test_util.document_tests.test_data import create_document_test_data
from documentation.models import Document
from django.core.exceptions import ObjectDoesNotExist

def create_and_delete_document(
	self, authenticated=True, expected_success=True, user_type=AUTHOR
):
	test_data, normalized_test_data = create_document_test_data()
	response = perform_post_and_retrieve_and_analyze(self, test_data, normalized_test_data)
	document_id = response.data['id']
	return delete_document_instance_and_verify_status_code(
		self=self, document_id=document_id, authenticated=authenticated,
		expected_success=expected_success, user_type=user_type
	), document_id

def verify_unauthenticated_document_delete_fails(self):
	response, document_id = create_and_delete_document(
		self=self, authenticated=False, expected_success=False
	)
	Document.objects.get(pk=document_id)

def verify_authenticated_viewer_document_delete_fails(self):
	response, document_id = create_and_delete_document(
		self=self, expected_success=False, user_type=VIEWER
	)
	Document.objects.get(pk=document_id)

def verify_authenticated_author_document_delete_succeeds(self):
	response, document_id = create_and_delete_document(
		self=self, expected_success=True
	)
	self.assertRaises(ObjectDoesNotExist, Document.objects.get, pk=document_id)

def verify_authenticated_staff_can_delete_other_user_document(self):
	response, document_id = create_and_delete_document(
		self=self, expected_success=True, user_type=STAFF
	)
	self.assertRaises(ObjectDoesNotExist, Document.objects.get, pk=document_id)

def verify_authenticated_admin_can_delete_other_user_document(self):
	response, document_id = create_and_delete_document(
		self=self, expected_success=True, user_type=ADMIN
	)
	self.assertRaises(ObjectDoesNotExist, Document.objects.get, pk=document_id)
