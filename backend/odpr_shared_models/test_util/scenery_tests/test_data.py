from odpr_shared_models.models import FilterProperty, Tag, TextWithHistory
from odpr_shared_models.test_util.test_data import normalize_list, normalize_element
from django.utils.six import BytesIO
from django.core.files import File
from PIL import Image
from io import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile
import copy
import io

test_data_create_minimal_scenery = {
	'title': 'Default title content',
	'description': {
		'content': 'Default description content'
	},
	'filter_properties': {
		'scenery_complexity': 1,
		'effects': [8, {'name': 'bla', 'description': {'content': 'bla2'}}, {'name': 'awd', 'description': {'content': 'aaegeasg'}}],
		'materials': [8, ],
		'lights': [7, ],
	},
	'tags': [2, ],
}

def get_normalized_test_data(test_data: dict):
	normalized_test_data = copy.deepcopy(test_data)

	description = normalize_element(normalized_test_data['description'], 'content', TextWithHistory)
	normalized_test_data['description'].update({'content': description})

	effects = normalize_list(normalized_test_data['filter_properties']['effects'], 'name', FilterProperty)
	materials = normalize_list(normalized_test_data['filter_properties']['materials'], 'name', FilterProperty)
	lights = normalize_list(normalized_test_data['filter_properties']['lights'], 'name', FilterProperty)
	tags = normalize_list(normalized_test_data['tags'], 'tag', Tag)
	normalized_test_data['filter_properties'].update({'effects': effects})
	normalized_test_data['filter_properties'].update({'materials': materials})
	normalized_test_data['filter_properties'].update({'lights': lights})
	normalized_test_data.update({'tags': tags})
	return normalized_test_data

def create_scenery_test_data(
	id=None, title=None, description=None, scenery_complexity=None, effects=None, materials=None, lights=None, tags=None,
	description_id=None, filter_properties_id=None, strict_types=True
):
	"""
	Will use the default scenery test data's content for unprovided arguments.
	:return: A scenery dict for posting and updating new sceneries.
	"""
	def assert_type(element, expected_type):
		nonlocal strict_types
		if strict_types:
			assert isinstance(element, expected_type)

	final_scenery = copy.deepcopy(test_data_create_minimal_scenery)
	if id is not None:
		assert_type(id, int)
		final_scenery.update({'id': id})
	if title is not None:
		assert_type(title, str)
		final_scenery.update({'title': title})
	if description_id is not None:
		assert_type(description_id, int)
		final_scenery['description'].update({'id': description_id})
	if description is not None:
		assert_type(description, str)
		final_scenery['description'].update({'content': description})
	if filter_properties_id is not None:
		assert_type(filter_properties_id, int)
		final_scenery['filter_properties'].update({'id': filter_properties_id})
	if scenery_complexity is not None:
		assert_type(scenery_complexity, int)
		final_scenery['filter_properties'].update({'scenery_complexity': scenery_complexity})
	if effects is not None:
		assert_type(effects, list)
		final_scenery['filter_properties'].update({'effects': effects})
	if materials is not None:
		assert_type(materials, list)
		final_scenery['filter_properties'].update({'materials': materials})
	if lights is not None:
		assert_type(lights, list)
		final_scenery['filter_properties'].update({'lights': lights})
	if tags is not None:
		assert_type(tags, list)
		final_scenery.update({'tags': tags})
	normalized_test_data = get_normalized_test_data(final_scenery)
	return final_scenery, normalized_test_data

def create_complex_test_data():
	return create_scenery_test_data(
		effects=[
			1, 3, 6,
			{'name': 'Reflection', 'description': 3},
			{'name': 'Translucency', 'description': {'content': 'Reusing translucent effect even with different content'}},
			{'name': 'New Effect', 'description': {'content': 'Some new effect'}}
		],
		materials=[
			{'name': 'New Material', 'description': {'content': 'First new material'}},
			{'name': 'Second New', 'description': {'content': 'Second new material'}},
			{'name': 'Translucent', 'description': 8},
			3
		],
		lights=[7, {'name': 'Spotlight', 'description': {'content': 'A simple spotlight'}}],
		tags=[2, 3, 11, 12, {'tag': 'New Tag'}]
	)

def modify_existing_scenery(existing_data: dict):
	final_scenery = copy.deepcopy(existing_data)
	final_scenery.update({'title': 'Updated title'})
	final_scenery['description'].update({'content': 'Updated description'})
	final_scenery['filter_properties'].update({'scenery_complexity': 2})
	final_scenery['filter_properties'].update({'effects': [1, 2, 4]})
	final_scenery['filter_properties'].update({'materials': [3, 5, 6]})
	final_scenery['filter_properties'].update({'lights': [2, ]})
	final_scenery.update({'tags': [1, 2]})
	normalized_test_data = get_normalized_test_data(final_scenery)
	return final_scenery, normalized_test_data

def partially_modify_existing_scenery(existing_data: dict):
	final_scenery = copy.deepcopy(existing_data)
	final_scenery.update({'title': 'Updated title'})
	final_scenery['description'].update({'content': 'Updated description'})
	final_scenery.pop('filter_properties', None)
	final_scenery.pop('tags', None)
	normalized_test_data = get_normalized_test_data(final_scenery)
	return final_scenery, normalized_test_data

def create_image(filename, storage=None, size=(100, 100), image_mode='RGB', image_format='PNG'):
	"""
	Generate a test image, returning the filename that it was saved as.

	If ``storage`` is ``None``, the BytesIO containing the image data
	will be passed instead.
	"""
	data = BytesIO()
	#data = io.FileIO(name=filename, mode='w+')
	Image.new(image_mode, size).save(data, image_format)
	data.seek(0)
	if not storage:
		return data
	image_file = ContentFile(data.read())
	return storage.save(filename, image_file)
