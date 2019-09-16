from .test_util import \
	perform_post_and_retrieve_and_analyze, delete_scenery_instance_and_verify_status_code
from ..test_util import AUTHOR, VIEWER, ADMIN, STAFF
from .test_data import create_scenery_test_data
from sceneries.models import Scenery
from django.core.exceptions import ObjectDoesNotExist

def create_and_delete_scenery(
	self, authenticated=True, expected_success=True, user_type=AUTHOR
):
	test_data, normalized_test_data = create_scenery_test_data()
	response = perform_post_and_retrieve_and_analyze(self, test_data, normalized_test_data)
	scenery_id = response.data['id']
	return delete_scenery_instance_and_verify_status_code(
		self=self, scenery_id=scenery_id, authenticated=authenticated,
		expected_success=expected_success, user_type=user_type
	), scenery_id

def verify_unauthenticated_scenery_delete_fails(self):
	response, scenery_id = create_and_delete_scenery(
		self=self, authenticated=False, expected_success=False
	)
	Scenery.objects.get(pk=scenery_id)

def verify_authenticated_viewer_scenery_delete_fails(self):
	response, scenery_id = create_and_delete_scenery(
		self=self, expected_success=False, user_type=VIEWER
	)
	Scenery.objects.get(pk=scenery_id)

def verify_authenticated_author_scenery_delete_succeeds(self):
	response, scenery_id = create_and_delete_scenery(
		self=self, expected_success=True
	)
	self.assertRaises(ObjectDoesNotExist, Scenery.objects.get, pk=scenery_id)

def verify_authenticated_staff_can_delete_other_user_scenery(self):
	response, scenery_id = create_and_delete_scenery(
		self=self, expected_success=True, user_type=STAFF
	)
	self.assertRaises(ObjectDoesNotExist, Scenery.objects.get, pk=scenery_id)

def verify_authenticated_admin_can_delete_other_user_scenery(self):
	response, scenery_id = create_and_delete_scenery(
		self=self, expected_success=True, user_type=ADMIN
	)
	self.assertRaises(ObjectDoesNotExist, Scenery.objects.get, pk=scenery_id)
