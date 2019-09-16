from ..test_util import make_get_request, make_post_request, make_put_request, make_patch_request, \
	make_delete_request, verify_response_status_code, \
	AUTHOR, authenticate_by_user_type, get_author_user
from sceneries.views import SceneryDetailView, SceneryCreateView, SceneryImageDetailView#, SceneryImageCreateView
from django.urls import reverse
from requests_toolbelt import MultipartEncoder


def assert_created_scenery_matches(
	self,
	created_scenery: dict,
	normalized_compare_data: dict,
	author_pk
):
	def received_list_contains_expected(
		inner_self,
		expected_elements,
		received_elements,
		received_identifier,
	):
		for expected_tag in expected_elements:
			contained = False
			for received_tag in received_elements:
				if received_tag[received_identifier] == expected_tag:
					contained = True
					break
			inner_self.assertTrue(contained)

	self.assertEqual(created_scenery['title'], normalized_compare_data['title'])
	self.assertEqual(created_scenery['description']['content'], normalized_compare_data['description']['content'])
	self.assertEqual(created_scenery['author'], author_pk)
	self.assertEqual(len(created_scenery['tags']), len(normalized_compare_data['tags']))
	received_list_contains_expected(self, normalized_compare_data['tags'], created_scenery['tags'], 'tag')
	created_filter_properties = created_scenery['filter_properties']
	self.assertEqual(
		len(created_filter_properties['effects']),
		len(normalized_compare_data['filter_properties']['effects'])
	)
	received_list_contains_expected(
		self, normalized_compare_data['filter_properties']['effects'],
		created_filter_properties['effects'], 'name'
	)
	self.assertEqual(
		len(created_filter_properties['materials']),
		len(normalized_compare_data['filter_properties']['materials'])
	)
	received_list_contains_expected(
		self, normalized_compare_data['filter_properties']['materials'],
		created_filter_properties['materials'], 'name'
	)
	self.assertEqual(
		len(created_filter_properties['lights']),
		len(normalized_compare_data['filter_properties']['lights'])
	)
	received_list_contains_expected(
		self, normalized_compare_data['filter_properties']['lights'],
		created_filter_properties['lights'], 'name'
	)

def get_scenery_test_data_and_verify_status_code(
	self, scenery_id, authenticated=True, expected_success=True, user_type=AUTHOR
):
	request = make_get_request()
	scenery_detail_view = SceneryDetailView.as_view()
	if authenticated:
		authenticate_by_user_type(request, user_type)
	response = scenery_detail_view(request=request, id=scenery_id)
	verify_response_status_code(self, response, expected_success)
	return response

def post_scenery_test_data_and_verify_status_code(
	self, test_data, authenticated=True, expected_success=True, user_type=AUTHOR
):
	request = make_post_request(data=test_data, format='json')
	scenery_create_view = SceneryCreateView.as_view()
	if authenticated:
		authenticate_by_user_type(request, user_type)
	response = scenery_create_view(request=request)
	verify_response_status_code(self, response, expected_success)
	return response

def put_scenery_test_data_and_verify_status_code(
	self, test_data, authenticated=True, expected_success=True, user_type=AUTHOR
):
	request = make_put_request(data=test_data, format='json')
	scenery_update_view = SceneryDetailView.as_view()
	if authenticated:
		authenticate_by_user_type(request, user_type)
	response = scenery_update_view(request=request, id=test_data['id'])
	verify_response_status_code(self, response, expected_success)
	return response

def patch_scenery_test_data_and_verify_status_code(
	self, test_data, authenticated=True, expected_success=True, user_type=AUTHOR
):
	request = make_patch_request(data=test_data, format='json')
	scenery_update_view = SceneryDetailView.as_view()
	if authenticated:
		authenticate_by_user_type(request, user_type)
	response = scenery_update_view(request=request, id=test_data['id'])
	verify_response_status_code(self, response, expected_success)
	return response

def delete_scenery_instance_and_verify_status_code(
	self, scenery_id, authenticated=True, expected_success=True, user_type=AUTHOR
):
	request = make_delete_request()
	scenery_delete_view = SceneryDetailView.as_view()
	if authenticated:
		authenticate_by_user_type(request, user_type)
	response = scenery_delete_view(request=request, id=scenery_id)
	verify_response_status_code(self, response, expected_success)
	return response

def perform_write_and_verify(
	self, test_data, normalized_test_data, write_function, authenticated=True, expected_success=True, user_type=AUTHOR
):
	write_response = write_function(
		self=self, test_data=test_data, authenticated=authenticated,
		expected_success=expected_success, user_type=user_type
	)
	if 200 <= write_response.status_code < 300:
		response = get_scenery_test_data_and_verify_status_code(self=self, scenery_id=write_response.data['id'])
		if expected_success and 200 <= response.status_code < 300:
			author_pk = write_response.data.pop('author', None)
			created_scenery = response.data
			assert_created_scenery_matches(
				self=self,
				created_scenery=created_scenery,
				normalized_compare_data=normalized_test_data,
				author_pk=author_pk
			)
		return response
	else:
		return write_response

def perform_post_and_retrieve_and_analyze(
	self, test_data, normalized_test_data, authenticated=True, expected_success=True
):
	return perform_write_and_verify(
		self=self, test_data=test_data, normalized_test_data=normalized_test_data, expected_success=expected_success,
		write_function=post_scenery_test_data_and_verify_status_code, authenticated=authenticated
	)

def perform_put_and_retrieve_and_analyze(
	self, test_data, normalized_test_data, authenticated=True, expected_success=True, user_type=AUTHOR
):
	return perform_write_and_verify(
		self=self, test_data=test_data, normalized_test_data=normalized_test_data, expected_success=expected_success,
		write_function=put_scenery_test_data_and_verify_status_code, authenticated=authenticated,
		user_type=user_type
	)

def perform_patch_and_retrieve_and_analyze(
	self, test_data, normalized_test_data, authenticated=True, expected_success=True
):
	return perform_write_and_verify(
		self=self, test_data=test_data, normalized_test_data=normalized_test_data, expected_success=expected_success,
		write_function=patch_scenery_test_data_and_verify_status_code, authenticated=authenticated
	)

def get_scenery_image_and_verify_status_code(
	self, image_id, authenticated=True, expected_success=True, user_type=AUTHOR
):
	request = make_get_request()
	scenery_image_detail_view = SceneryImageDetailView.as_view()
	if authenticated:
		authenticate_by_user_type(request, user_type)
	response = scenery_image_detail_view(request=request, id=image_id)
	verify_response_status_code(self, response, expected_success)
	return response

def post_scenery_image_and_verify_status_code(
	self, test_data, authenticated=True, expected_success=True, user_type=AUTHOR
):
	from rest_framework.test import APIRequestFactory
	from django.test.client import MULTIPART_CONTENT

	#APIRequestFactory().put('', format='multipart', content_type=MULTIPART_CONTENT, {''})
	#request = make_put_request(data=test_data, format='multipart', content_type=MULTIPART_CONTENT)
	#request = make_put_request(data=test_data, format='multipart')

#	request = make_put_request(data=test_data, content_type=MULTIPART_CONTENT)
#	scenery_image_create_view = SceneryImageDetailView.as_view()
#	if authenticated:
#		authenticate_by_user_type(request, user_type)
#	response = scenery_image_create_view(request=request)
	#set_urlconf('vuedj.urls')
	#import requests

	m = MultipartEncoder(test_data, boundary='cmon_baby_go_vegan_now_and_save_the_planet__trust_me_i_am_an_engineer')

	self.client.force_authenticate(get_author_user())
	response = self.client.put(
		# path=reverse('api:sceneries:scenery-image-detail'), data=test_data, content_type='multipart/form-data'
		path=reverse('api:sceneries:scenery-image-detail'), data=m.to_string(), content_type=m.content_type
	)

	verify_response_status_code(self, response, expected_success)
	return response
