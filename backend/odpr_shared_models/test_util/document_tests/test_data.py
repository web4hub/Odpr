from odpr_shared_models.models import TextWithHistory
from odpr_shared_models.test_util.test_data import normalize_list, normalize_element
from documentation.models import DocumentationTag
import copy

test_data_create_minimal_document = {
	'title': 'Default title content',
	'description': {
		'content': 'Default description content'
	},
	'tags': [2, ],
}

def get_normalized_test_data(test_data: dict):
	normalized_test_data = copy.deepcopy(test_data)
	description = normalize_element(normalized_test_data['description'], 'content', TextWithHistory)
	normalized_test_data['description'].update({'content': description})
	tags = normalize_list(normalized_test_data['tags'], 'tag', DocumentationTag)
	normalized_test_data.update({'tags': tags})
	return normalized_test_data

def create_document_test_data(
	id=None, title=None, description=None, tags=None,
	description_id=None, strict_types=True
):
	"""
	Will use the default document test data's content for unprovided arguments.
	:return: A document dict for posting and updating new documents.
	"""
	def assert_type(element, expected_type):
		nonlocal strict_types
		if strict_types:
			assert isinstance(element, expected_type)

	final_document = copy.deepcopy(test_data_create_minimal_document)
	if id is not None:
		assert_type(id, int)
		final_document.update({'id': id})
	if title is not None:
		assert_type(title, str)
		final_document.update({'title': title})
	if description_id is not None:
		assert_type(description_id, int)
		final_document['description'].update({'id': description_id})
	if description is not None:
		assert_type(description, str)
		final_document['description'].update({'content': description})
	if tags is not None:
		assert_type(tags, list)
		final_document.update({'tags': tags})
	normalized_test_data = get_normalized_test_data(final_document)
	return final_document, normalized_test_data

def create_complex_test_data():
	return create_document_test_data(
		tags=[2, 3, 11, 12, {'tag': 'New Tag'}]
	)

def modify_existing_document(existing_data: dict):
	final_document = copy.deepcopy(existing_data)
	final_document.update({'title': 'Updated title'})
	final_document['description'].update({'content': 'Updated description'})
	final_document.update({'tags': [1, 2]})
	normalized_test_data = get_normalized_test_data(final_document)
	return final_document, normalized_test_data

def partially_modify_existing_document(existing_data: dict):
	final_document = copy.deepcopy(existing_data)
	final_document.update({'title': 'Updated title'})
	final_document['description'].update({'content': 'Updated description'})
	final_document.pop('tags', None)
	normalized_test_data = get_normalized_test_data(final_document)
	return final_document, normalized_test_data
