from .test_util import \
	perform_post_and_retrieve_and_analyze, delete_request_instance_and_verify_status_code
from ..test_util import AUTHOR, VIEWER, ADMIN, STAFF
from .test_data import create_request_test_data
from scenery_requests.models import Request
from django.core.exceptions import ObjectDoesNotExist

def create_and_delete_request(
	self, authenticated=True, expected_success=True, user_type=AUTHOR
):
	test_data, normalized_test_data = create_request_test_data()
	response = perform_post_and_retrieve_and_analyze(self, test_data, normalized_test_data)
	request_id = response.data['id']
	return delete_request_instance_and_verify_status_code(
		self=self, request_id=request_id, authenticated=authenticated,
		expected_success=expected_success, user_type=user_type
	), request_id

def verify_unauthenticated_request_delete_fails(self):
	response, request_id = create_and_delete_request(
		self=self, authenticated=False, expected_success=False
	)
	Request.objects.get(pk=request_id)

def verify_authenticated_viewer_request_delete_fails(self):
	response, request_id = create_and_delete_request(
		self=self, expected_success=False, user_type=VIEWER
	)
	Request.objects.get(pk=request_id)

def verify_authenticated_author_request_delete_succeeds(self):
	response, request_id = create_and_delete_request(
		self=self, expected_success=True
	)
	self.assertRaises(ObjectDoesNotExist, Request.objects.get, pk=request_id)

def verify_authenticated_staff_can_delete_other_user_request(self):
	response, request_id = create_and_delete_request(
		self=self, expected_success=True, user_type=STAFF
	)
	self.assertRaises(ObjectDoesNotExist, Request.objects.get, pk=request_id)

def verify_authenticated_admin_can_delete_other_user_request(self):
	response, request_id = create_and_delete_request(
		self=self, expected_success=True, user_type=ADMIN
	)
	self.assertRaises(ObjectDoesNotExist, Request.objects.get, pk=request_id)
