from .test_util import post_scenery_test_data_and_verify_status_code, \
	perform_post_and_retrieve_and_analyze, post_scenery_image_and_verify_status_code
from .test_data import create_scenery_test_data, create_complex_test_data, create_image
from django.core.files.uploadedfile import SimpleUploadedFile, InMemoryUploadedFile
import io

def verify_scenery_create_image_create_succeeds(self):
	test_data, normalized_test_data = create_complex_test_data()
	response = perform_post_and_retrieve_and_analyze(self, test_data, normalized_test_data)
	scenery_id = response.data['id']

	test_image = create_image('test_image.png')
	test_image_file = SimpleUploadedFile(
		name='front.png', content=test_image.getvalue(), content_type='image/png'
	)
	test_data = {
		'image': test_image_file,
		'scenery': str(scenery_id)
	}
	post_scenery_image_and_verify_status_code(
		self, test_data=test_data
	)

