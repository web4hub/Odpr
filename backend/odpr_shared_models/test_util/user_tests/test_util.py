from accounts.views import CustomRegisterView, UserDetailView
from odpr_shared_models.test_util.test_util import ADMIN, AUTHOR, CUSTOM_ID, make_get_request, make_patch_request, \
	make_put_request, make_delete_request, make_register_request, authenticate_by_user_type, verify_response_status_code, \
	STAFF
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

def assert_created_user_matches(
	self,
	created_user: dict,
	normalized_compare_data: dict,
	user_type:int=AUTHOR
):
	self.assertEqual(created_user['username'], normalized_compare_data['username'])
	if 'email' in normalized_compare_data and (user_type is AUTHOR or user_type is STAFF or user_type is ADMIN):
		self.assertEqual(created_user['email'], normalized_compare_data['email'])
	if 'bio' in normalized_compare_data:
		self.assertEqual(created_user['bio']['content'], normalized_compare_data['bio']['content'])

def get_user_test_data_and_verify_status_code(
	self, user_id, authenticated=True, expected_success=True, user_type=AUTHOR, custom_user_id=1
):
	request = make_get_request()
	user_detail_view = UserDetailView.as_view()
	if authenticated:
		authenticate_by_user_type(request, user_type, custom_id=custom_user_id)
	response = user_detail_view(request=request, id=user_id)
	verify_response_status_code(self, response, expected_success)
	return response

def post_user_test_data_and_verify_status_code(
	self, test_data, authenticated=True, expected_success=True, user_type=AUTHOR, custom_user_id=1
):
	request = make_register_request(data=test_data, format='json')
	user_create_view = CustomRegisterView.as_view()
	if authenticated:
		authenticate_by_user_type(request, user_type, custom_id=custom_user_id)
	response = user_create_view(request=request)
	verify_response_status_code(self, response, expected_success)
	return response

def put_user_test_data_and_verify_status_code(
	self, test_data, authenticated=True, expected_success=True, user_type=AUTHOR, custom_user_id=1
):
	request = make_put_request(data=test_data, format='json')
	user_update_view = UserDetailView.as_view()
	if authenticated:
		authenticate_by_user_type(request, user_type, custom_id=custom_user_id)
	response = user_update_view(request=request, id=test_data['id'])
	verify_response_status_code(self, response, expected_success)
	return response

def patch_user_test_data_and_verify_status_code(
	self, test_data, authenticated=True, expected_success=True, user_type=AUTHOR, custom_user_id=1
):
	request = make_patch_request(data=test_data, format='json')
	user_update_view = UserDetailView.as_view()
	if authenticated:
		authenticate_by_user_type(request, user_type, custom_id=custom_user_id)
	response = user_update_view(request=request, id=test_data['id'])
	verify_response_status_code(self, response, expected_success)
	return response

def delete_user_instance_and_verify_status_code(
	self, user_id, authenticated=True, expected_success=True, user_type=AUTHOR, custom_user_id=1
):
	request = make_delete_request()
	user_delete_view = UserDetailView.as_view()
	if authenticated:
		authenticate_by_user_type(request, user_type, custom_id=custom_user_id)
	response = user_delete_view(request=request, id=user_id)
	verify_response_status_code(self, response, expected_success)
	return response

def perform_write_and_verify(
	self, test_data, normalized_test_data, write_function, authenticated_write=True, custom_user_id=1,
	authenticated_retrieve=True, expected_success=True, user_type_write=AUTHOR, user_type_retrieve=AUTHOR
):
	write_response = write_function(
		self=self, test_data=test_data, authenticated=authenticated_write, custom_user_id=custom_user_id,
		expected_success=expected_success, user_type=user_type_write
	)
	if 200 <= write_response.status_code < 300:
		if user_type_write is not CUSTOM_ID and user_type_retrieve is CUSTOM_ID:
			custom_user_id = write_response.data['id']
		response = get_user_test_data_and_verify_status_code(
			self=self, user_id=write_response.data['id'], authenticated=authenticated_retrieve, user_type=user_type_retrieve,
			custom_user_id=custom_user_id
		)
		if expected_success and 200 <= response.status_code < 300:
			created_user = response.data
			assert_created_user_matches(
				self=self,
				created_user=created_user,
				normalized_compare_data=normalized_test_data,
				user_type=user_type_retrieve
			)
		return response
	else:
		return write_response

def perform_post_and_retrieve_and_analyze(
	self, test_data, normalized_test_data, authenticated_write=False, authenticated_retrieve=True, expected_success=True,
	user_type_write=AUTHOR, user_type_retrieve=AUTHOR, custom_user_id=1
):
	return perform_write_and_verify(
		self=self, test_data=test_data, normalized_test_data=normalized_test_data, expected_success=expected_success,
		write_function=post_user_test_data_and_verify_status_code, authenticated_write=authenticated_write,
		authenticated_retrieve=authenticated_retrieve, user_type_write=user_type_write,
		user_type_retrieve=user_type_retrieve, custom_user_id=custom_user_id
	)

def perform_put_and_retrieve_and_analyze(
	self, test_data, normalized_test_data, authenticated=True, expected_success=True,
	user_type_write=AUTHOR, user_type_retrieve=AUTHOR, custom_user_id=1
):
	return perform_write_and_verify(
		self=self, test_data=test_data, normalized_test_data=normalized_test_data, expected_success=expected_success,
		write_function=put_user_test_data_and_verify_status_code, authenticated_retrieve=authenticated,
		user_type_write=user_type_write, user_type_retrieve=user_type_retrieve, custom_user_id=custom_user_id
	)

def perform_patch_and_retrieve_and_analyze(
	self, test_data, normalized_test_data, authenticated=True, expected_success=True,
	user_type_write=AUTHOR, user_type_retrieve=AUTHOR, custom_user_id=1
):
	return perform_write_and_verify(
		self=self, test_data=test_data, normalized_test_data=normalized_test_data, expected_success=expected_success,
		write_function=patch_user_test_data_and_verify_status_code, authenticated_retrieve=authenticated,
		user_type_write=user_type_write, user_type_retrieve=user_type_retrieve, custom_user_id=custom_user_id
	)

def get_first_testuser_instance():
	users = get_user_model().objects.all()
	if len(users) >= 1:
		return users[0]
	raise ObjectDoesNotExist('Tried to fetch user instance, but could not find any users in db.'
													 ' Maybe you did not load fixtures for this test or there is no user in the fixtures?')
