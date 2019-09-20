from odpr_shared_models.models import TextWithHistory
from odpr_shared_models.test_util.test_data import normalize_element
import copy

test_data_create_minimal_user = {
	'username': 'Default_username',
	'email': 'default@email.com',
	'password1': 'default password',
	'password2': 'default password'
}

def get_normalized_test_data(test_data: dict):
	normalized_test_data = copy.deepcopy(test_data)
	if 'bio' in normalized_test_data:
		bio = normalize_element(normalized_test_data['bio'], 'content', TextWithHistory)
		normalized_test_data['bio'].update({'content': bio})
	return normalized_test_data

def create_user_test_data(
	id=None, username=None, email=None, password1=None, password2=None, strict_types=True
):
	"""
	Will use the default user test data's content for unprovided arguments.
	:return: A user dict for posting and updating new accounts.
	"""
	def assert_type(element, expected_type):
		nonlocal strict_types
		if strict_types:
			assert isinstance(element, expected_type)

	final_user = copy.deepcopy(test_data_create_minimal_user)
	if id is not None:
		assert_type(id, int)
		final_user.update({'id': id})
	if username is not None:
		assert_type(username, str)
		final_user.update({'username': username})
	if password1 is not None:
		assert_type(password1, str)
		final_user.update({'password1': password1})
	if password2 is not None:
		assert_type(password2, str)
		final_user.update({'password2': password2})
	if email is not None:
		assert_type(email, str)
		final_user.update({'email': email})
	normalized_test_data = get_normalized_test_data(final_user)
	return final_user, normalized_test_data

def modify_existing_user(existing_data: dict):
	final_user = copy.deepcopy(existing_data)
	final_user.update({'username': 'Updated_username'})
	final_user.update({'email': 'updated@email.com'})
	final_user.update({'bio': {'content': 'Updated bio'}})
	normalized_test_data = get_normalized_test_data(final_user)
	return final_user, normalized_test_data

def partially_modify_existing_user(existing_data: dict):
	final_user = copy.deepcopy(existing_data)
	final_user.update({'username': 'Updated_username'})
	final_user.pop('email', None)
	final_user.update({'bio': {'content': 'Updated bio'}})
	normalized_test_data = get_normalized_test_data(final_user)
	return final_user, normalized_test_data
