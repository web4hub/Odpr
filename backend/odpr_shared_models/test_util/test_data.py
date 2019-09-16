from django.core.exceptions import ObjectDoesNotExist

def normalize_element(element, identifier, ElementModel):
	if isinstance(element, int):
		try:
			return getattr(ElementModel.objects.get(pk=element), identifier)
		except ObjectDoesNotExist:
			return None
	elif isinstance(element, str):
		return element
	elif isinstance(element, dict):
		return element[identifier]
	elif isinstance(element, ElementModel):
		return element.name

def normalize_list(element_list, identifier, ElementModel):
	final_list = []
	for value in element_list:
		final_list.append(normalize_element(value, identifier, ElementModel))
	return final_list

def make_nested_serializer_filterproperty_test_data(
	test_author_instance, filter_property_type
):
	from odpr_shared_models.models import TextWithHistory, FilterProperty
	test_description_instance = TextWithHistory.objects.create(content='test_content_{}'.format(filter_property_type))
	test_description_instance_2 = TextWithHistory.objects.create(content='test_content_{}_3'.format(filter_property_type))
	test_description_instance_3 = TextWithHistory.objects.create(content='test_content_{}_4'.format(filter_property_type))

	reuse_name = 'Test {} Reuse'.format(filter_property_type)
	reuse_by_instance_name = 'Test {} Reuse by instance'.format(filter_property_type)
	reuse_by_pk_name = 'Test {} Reuse by pk'.format(filter_property_type)
	create_name = 'Test {} Create'.format(filter_property_type)

	FilterProperty.objects.create(
		author=test_author_instance,
		description=test_description_instance,
		name=reuse_name
	)
	filter_property_1 = {
		'author': test_author_instance,
		'description': {'content': 'test_content_e'},
		'name': reuse_name
	}
	filter_property_2 = {
		'author': test_author_instance,
		'description': {'content': 'new effect'},
		'name': create_name
	}
	filter_property_3 = FilterProperty.objects.create(
		author=test_author_instance,
		description=test_description_instance_2,
		name=reuse_by_instance_name
	)
	filter_property_4_instance_for_reuse = FilterProperty.objects.create(
		author=test_author_instance,
		description=test_description_instance_3,
		name=reuse_by_pk_name
	)
	filter_property_4 = filter_property_4_instance_for_reuse.pk
	result = (
		filter_property_1, filter_property_2, filter_property_3, filter_property_4,
		normalize_element(filter_property_1, 'name', FilterProperty),
		normalize_element(filter_property_2, 'name', FilterProperty),
		normalize_element(filter_property_3, 'name', FilterProperty),
		normalize_element(filter_property_4, 'name', FilterProperty)
	)
	return result

def make_nested_serializer_effects_test_data(test_author_instance):
	return make_nested_serializer_filterproperty_test_data(test_author_instance, 'effect')

def make_nested_serializer_materials_test_data(test_author_instance):
	return make_nested_serializer_filterproperty_test_data(test_author_instance, 'material')

def make_nested_serializer_lights_test_data(test_author_instance):
	return make_nested_serializer_filterproperty_test_data(test_author_instance, 'light')
