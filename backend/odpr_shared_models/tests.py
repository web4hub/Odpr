from django.test import TestCase
from .serializer_util import IllegalArgumentError, NestedModelSerializer
from .models import TextWithHistory, ReputationRule, FilterProperty, FilterProperties
from .serializers import TextWithHistorySerializer, ReputationRuleSerializer,\
	FilterPropertySerializer, FilterPropertiesSerializer
from django.contrib.auth import get_user_model
from odpr_shared_models.test_util.test_data import make_nested_serializer_effects_test_data, \
	make_nested_serializer_materials_test_data, \
	make_nested_serializer_lights_test_data
from odpr_shared_models.test_util.scenery_tests.scenery_create_tests import \
	verify_create_serializer_succeeds_if_optional_args_missing


class NestedCreateSerializerUnitTests(TestCase):
	serializer = NestedModelSerializer()

	def test_nested_serializer__invalid_1(self):
		'''
			Input: bool
			Expected output: TypeError Exception
		'''
		test_data = False
		self.assertRaises(TypeError, self.serializer.deserialize_nested_data_by_reuse_or_create, element=test_data)

	def test_nested_serializer__invalid_2(self):
		'''
			Input: invalid nested value for expected type: given: dict, expected: str
			Expected output: ValidationError Exception
		'''
		test_data = {'content': {'bla': 'bla', 'yoyo': 'yaya'}}
		self.assertRaises(
			IllegalArgumentError, self.serializer.deserialize_nested_data_by_reuse_or_create, element=test_data,
			ElementModel=TextWithHistory, ElementSerializer=TextWithHistorySerializer
		)

	def test_nested_serializer__invalid_3(self):
		'''
			Input: missing argument ElementModel when input is a dict
			Expected output: IllegalArgumentError Exception
		'''
		test_data = {'content': {'bla': 'bla', 'yoyo': 'yaya'}}
		self.assertRaises(
			IllegalArgumentError, self.serializer.deserialize_nested_data_by_reuse_or_create, element=test_data,
			ElementSerializer=TextWithHistorySerializer
		)

	def test_nested_serializer__invalid_4(self):
		'''
			Input: missing argument element_serializer when input is a dict
			Expected output: IllegalArgumentError Exception
		'''
		test_data = {'content': {'bla': 'bla', 'yoyo': 'yaya'}}
		self.assertRaises(
			IllegalArgumentError, self.serializer.deserialize_nested_data_by_reuse_or_create, element=test_data,
			ElementModel=TextWithHistory
		)

	def test_nested_serializer__case_1(self):
		'''
			Input: int
			Expected output: int (equal to input)
		'''
		test_data = 7
		result = self.serializer.deserialize_nested_data_by_reuse_or_create(element=test_data, produce_model_instances=False)
		self.assertIsInstance(
			result,	type(test_data),
			'Expected {} as result from nested serializer but got {}'.format(type(test_data), type(result))
		)
		self.assertEqual(
			result,	test_data,
			'Expected result to have same value as input to nested serializer, but {} != {}'.format(result, test_data)
		)

	def test_nested_serializer__case_2(self):
		'''
			Input: str
			Expected output: str (equal to input)
		'''
		test_data = 'go_vegan'
		result = self.serializer.deserialize_nested_data_by_reuse_or_create(element=test_data, produce_model_instances=False)
		self.assertIsInstance(
			result, type(test_data),
			'Expected {} as result from nested serializer but got {}'.format(type(test_data), type(result))
		)
		self.assertEqual(
			result, test_data,
			'Expected result to have same value as input to nested serializer, but {} != {}'.format(result, test_data)
		)

	def test_nested_serializer__case_3(self):
		'''
			Input: Model instance. (Never a model class, always INSTANCE only). (Model means a django db Model)
			Expected output: PK   (The primary key as int of the model's instance).
		'''
		test_data = TextWithHistory.objects.create(content='test_content')  # chose a very simple model for the test
		self.assertIsInstance(test_data, TextWithHistory)
		result = self.serializer.deserialize_nested_data_by_reuse_or_create(
			ElementModel=TextWithHistory,
			element=test_data, produce_model_instances=False
		)
		self.assertIsInstance(
			result, int,
			'Expected int as result from nested serializer but got {}'.format(type(result))
		)
		self.assertGreaterEqual(result, 1, 'Expected result pk being greater or equal 1, but was: {}'.format(result))

	def test_nested_serializer__case_4___values(self):
		'''
			Note: This testcase DEPENDS on testcase__case_5 (not directly through testcode, but in context of the
						implementation code. If this test fails, AND testcase 5 also fails, it is very likely, this test succeeds,
						as soon as test 5 succeeds.
			Input: list      can be primary keys only, mixed, or values only.
			Expected output: list (only containing PK values)
		'''
		test_data = [
			{'content': 'first text with history'},
			{'content': 'second text with history'},
			{'content': 'third text with history'},
			{'content': 'fourth text with history'}
		]

		result = self.serializer.deserialize_nested_data_by_reuse_or_create(
			ElementModel=TextWithHistory,
			ElementSerializer=TextWithHistorySerializer,
			element=test_data, produce_model_instances=False
		)
		self.assertIsInstance(
			result, type(test_data),
			'Expected {} as result from nested serializer but got {}'.format(type(test_data), type(result))
		)
		self.assertEqual(
			len(result), 4,
			'Expected amount of elements in result-list to be {}, but was {}'.format(len(result), 4)
		)
		for result_element in result:
			self.assertIsInstance(
				result_element, int,
				'Expected result to be of type {}, but got {}'.format(int, type(result_element))
			)

	def test_nested_serializer__case_4___primary_keys(self):
		'''
			Note: This testcase DEPENDS on testcase__case_5 (not directly through testcode, but in context of the
						implementation code. If this test fails, AND testcase 5 also fails, it is very likely, this test succeeds,
						as soon as test 5 succeeds.
			Input: list      can be primary keys only, mixed, or values only.
			Expected output: list (only containing PK values)
		'''
		test_data = [1, 2, 3, 4]

		result = self.serializer.deserialize_nested_data_by_reuse_or_create(
			ElementModel=TextWithHistory,
			ElementSerializer=TextWithHistorySerializer,
			element=test_data, produce_model_instances=False
		)
		self.assertIsInstance(
			result, type(test_data),
			'Expected {} as result from nested serializer but got {}'.format(type(test_data), type(result))
		)
		self.assertEqual(
			len(result), 4,
			'Expected amount of elements in result-list to be {}, but was {}'.format(len(result), 4)
		)
		for result_element in result:
			self.assertIsInstance(
				result_element, int,
				'Expected result to be of type {}, but got {}'.format(int, type(result_element))
			)
		self.assertListEqual(
			result, test_data,
			msg='Expected result-list to equal test-data-list, but {} != {}'.format(result, test_data)
		)

	def test_nested_serializer__case_4___mixed(self):
		'''
			Note: This testcase DEPENDS on testcase__case_5 (not directly through testcode, but in context of the
						implementation code. If this test fails, AND testcase 5 also fails, it is very likely, this test succeeds,
						as soon as test 5 succeeds.
			Input: list      can be primary keys only, mixed, or values only.
			Expected output: list (only containing PK values)
		'''
		test_data = [
			9,
			{'content': 'second text with history'},
			7,
			{'content': 'fourth text with history'}
		]

		result = self.serializer.deserialize_nested_data_by_reuse_or_create(
			ElementModel=TextWithHistory,
			ElementSerializer=TextWithHistorySerializer,
			element=test_data, produce_model_instances=False
		)
		self.assertIsInstance(
			result, type(test_data),
			'Expected {} as result from nested serializer but got {}'.format(type(test_data), type(result))
		)
		self.assertEqual(
			len(result), 4,
			'Expected amount of elements in result-list to be {}, but was {}'.format(len(result), 4)
		)
		for result_element in result:
			self.assertIsInstance(
				result_element, int,
				'Expected result to be of type {}, but got {}'.format(int, type(result_element))
			)
		self.assertIn(9, result, msg='Expected result to contain element int(9).')
		self.assertIn(7, result, msg='Expected result to contain element int(7).')


class NestedCreateSerializerUnitTestsWithFixtures(TestCase):
	fixtures = (
		'user_fixtures',
		'badge_fixtures',
		'text_with_history_fixtures',
		'filter_property_fixtures',
		'filter_properties_fixtures',
		'scenery_fixtures',
		'tag_fixtures',
	)
	serializer = NestedModelSerializer()

	def test_nested_serializer__case_4___values__mixed__1_3_5(self):
		'''
			Note: This testcase DEPENDS on testcase__case_5 (not directly through testcode, but in context of the
						implementation code. If this test fails, AND testcase 5 also fails, it is very likely, this test succeeds,
						as soon as test 5 succeeds.
			Input: list      can be primary keys only, mixed, or values only.
			Expected output: list (only containing PK values)
		'''
		test_author_instance = get_user_model().objects.get(pk=2)
		effect_1, effect_2, effect_3, effect_4, normalized_effect_1, normalized_effect_2, normalized_effect_3, \
			normalized_effect_4 = make_nested_serializer_effects_test_data(test_author_instance)

		test_data = [effect_1, effect_2, effect_3, effect_4]

		result = self.serializer.deserialize_nested_data_by_reuse_or_create(
			element=test_data,
			ElementModel=FilterProperty,
			ElementSerializer=FilterPropertySerializer,
			produce_model_instances=False
		)

		self.assertIsInstance(result, list)
		self.assertIsInstance(result[0], int)
		self.assertIsInstance(result[1], int)
		self.assertIsInstance(result[2], int)
		self.assertIsInstance(result[3], int)


	def test_nested_serializer__case_5___dict_1(self):
		'''
			Input: dict (Integer values only)
			Expected output: dict   (Same structure like input, same values as input, as not nested objects used).
		'''
		test_data = {
			'key': 17,
			'condition': 500
		}
		result = self.serializer.deserialize_nested_data_by_reuse_or_create(
			element=test_data,
			ElementModel=ReputationRule,
			ElementSerializer=ReputationRuleSerializer,
			produce_model_instances=False
		)
		self.assertIsInstance(
			result, type(test_data),
			'Expected {} as result from nested serializer but got {}'.format(type(test_data), type(result))
		)
		self.assertEqual(
			result, test_data,
			'Expected result to have same value as input to nested serializer, but {} != {}'.format(result, test_data)
		)

	def test_nested_serializer__case_5___dict_2(self):
		'''
			Input: dict (String objects only)
			Expected output: dict   (Same structure like input, same values like input as no nested objects used).
		'''
		test_data = {
			'content': 'TestDataContent'
		}
		result = self.serializer.deserialize_nested_data_by_reuse_or_create(
			element=test_data,
			ElementModel=TextWithHistory,
			ElementSerializer=TextWithHistorySerializer,
			produce_model_instances=False
		)
		self.assertIsInstance(
			result, type(test_data),
			'Expected {} as result from nested serializer but got {}'.format(type(test_data), type(result))
		)
		self.assertEqual(
			result, test_data,
			'Expected result to have same value as input to nested serializer, but {} != {}'.format(result, test_data)
		)

	def test_nested_serializer__case_5___dict_3(self):
		'''
			Input: dict (Model instance)
			Expected output: dict   (primary key as value of model instance).
		'''
		test_model_instance = TextWithHistory.objects.create(content='test_content')  # chose a very simple model for the test
		test_author_instance = get_user_model().objects.get(pk=2)
		test_data = {
			'author': test_author_instance,
			'description': test_model_instance,
			'name': 'test_name'
		}
		self.assertIsInstance(test_data['author'], get_user_model())
		self.assertIsInstance(test_data['description'], TextWithHistory)
		self.assertIsInstance(test_data['name'], str)

		result = self.serializer.deserialize_nested_data_by_reuse_or_create(
			ElementModel=FilterProperty,
			ElementSerializer=FilterPropertySerializer,
			element=test_data,
			produce_model_instances=False
		)

		self.assertIsInstance(
			result, type(test_data),
			'Expected {} as result from nested serializer but got {}'.format(type(test_data), type(result))
		)
		self.assertIsInstance(result['author'], int)
		self.assertIsInstance(result['description'], int)
		self.assertIsInstance(result['name'], str)

	def test_nested_serializer__case_5___dict_4___values(self):
		'''
			Input: dict (list, values)
			Expected output: dict   (list of primary keys as values for the previous list).
		'''
		# Note: Currently, there is no possible occurrence of a dict with a list with primitive values.
		pass

	def test_nested_serializer__case_5___dict_1_2_3_4_5__nested(self):
		'''
			Input: dict (list, primary keys, model instances and nested dicts in list, primitives)
			Expected output: dict   (list with primary keys as values for the previous list, plus primitives).

			#1: The input dict should have a valid structure
			#2: The output of the tested function should be like expected
			#3: Nested django models should have been created
			#4: The root level (input dict) must not exist as django model/instance after the operation
		'''
		filter_properties_count_original = FilterProperties.objects.count()

		test_author_instance = get_user_model().objects.get(pk=2)

		# needed: 1 effect as FilterProperty dict (reuse)
		#         1 effect as FilterProperty dict (new)
		#         1 effect as FilterProperty instance (reuse)
		#         1 effect as FilterProperty pk (reuse)
		effect_1, effect_2, effect_3, effect_4, normalized_effect_1, normalized_effect_2, normalized_effect_3, \
			normalized_effect_4 = make_nested_serializer_effects_test_data(test_author_instance)
		material_1, material_2, material_3, material_4, normalized_material_1, normalized_material_2, \
			normalized_material_3, normalized_material_4 = make_nested_serializer_materials_test_data(test_author_instance)
		light_1, light_2, light_3, light_4, normalized_light_1, normalized_light_2, normalized_light_3, normalized_light_4 \
			= make_nested_serializer_lights_test_data(test_author_instance)

		test_data = {
			'author': test_author_instance,
			'scenery_complexity': 1,
			'effects': [effect_1, effect_2, effect_3, effect_4],  # [dict, dict, instance, pk<int>]
			'materials': [material_1, material_2, material_3, material_4],
			'lights': [light_1, light_2, light_3, light_4]
		}

		#  #1
		self.assertIsInstance(test_data['author'], get_user_model())
		self.assertIsInstance(test_data['scenery_complexity'], int)
		self.assertIsInstance(test_data['effects'], list)
		self.assertIsInstance(test_data['effects'][0], dict)
		self.assertIsInstance(test_data['effects'][1], dict)
		self.assertIsInstance(test_data['effects'][2], FilterProperty)
		self.assertIsInstance(test_data['effects'][3], int)
		self.assertIsInstance(test_data['materials'], list)
		self.assertIsInstance(test_data['materials'][0], dict)
		self.assertIsInstance(test_data['materials'][1], dict)
		self.assertIsInstance(test_data['materials'][2], FilterProperty)
		self.assertIsInstance(test_data['materials'][3], int)
		self.assertIsInstance(test_data['lights'], list)
		self.assertIsInstance(test_data['lights'][0], dict)
		self.assertIsInstance(test_data['lights'][1], dict)
		self.assertIsInstance(test_data['lights'][2], FilterProperty)
		self.assertIsInstance(test_data['lights'][3], int)

		result = self.serializer.deserialize_nested_data_by_reuse_or_create(
			ElementModel=FilterProperties,
			ElementSerializer=FilterPropertiesSerializer,
			element=test_data,
			produce_model_instances=False
		)

		#  #2
		self.assertIsInstance(
			result, type(test_data),
			'Expected {} as result from nested serializer but got {}'.format(type(test_data), type(result))
		)
		self.assertIsInstance(result['author'], int)
		self.assertIsInstance(result['scenery_complexity'], int)
		self.assertIsInstance(result['effects'], list)
		self.assertIsInstance(result['effects'][0], int)
		self.assertIsInstance(result['effects'][1], int)
		self.assertIsInstance(result['effects'][2], int)
		self.assertIsInstance(result['effects'][3], int)
		self.assertIsInstance(result['materials'], list)
		self.assertIsInstance(result['materials'][0], int)
		self.assertIsInstance(result['materials'][1], int)
		self.assertIsInstance(result['materials'][2], int)
		self.assertIsInstance(result['materials'][3], int)
		self.assertIsInstance(result['lights'], list)
		self.assertIsInstance(result['lights'][0], int)
		self.assertIsInstance(result['lights'][1], int)
		self.assertIsInstance(result['lights'][2], int)
		self.assertIsInstance(result['lights'][3], int)


		#  #3   test if nested are created
		effect_result_1 = FilterProperty.objects.get(pk=result['effects'][0])
		self.assertIsNotNone(effect_result_1, 'Expected nested serializer to create the objects in the database')
		self.assertEqual(normalized_effect_1, effect_result_1.name)
		effect_result_2 = FilterProperty.objects.get(pk=result['effects'][1])
		self.assertIsNotNone(effect_result_2, 'Expected nested serializer to create the objects in the database')
		self.assertEqual(normalized_effect_2, effect_result_2.name)
		effect_result_3 = FilterProperty.objects.get(pk=result['effects'][2])
		self.assertIsNotNone(effect_result_3, 'Expected nested serializer to create the objects in the database')
		self.assertEqual(normalized_effect_3, effect_result_3.name)
		effect_result_4 = FilterProperty.objects.get(pk=result['effects'][3])
		self.assertIsNotNone(effect_result_4, 'Expected nested serializer to create the objects in the database')
		self.assertEqual(normalized_effect_4, effect_result_4.name)

		material_result_1 = FilterProperty.objects.get(pk=result['materials'][0])
		self.assertIsNotNone(material_result_1, 'Expected nested serializer to create the objects in the database')
		self.assertEqual(normalized_material_1, material_result_1.name)
		material_result_2 = FilterProperty.objects.get(pk=result['materials'][1])
		self.assertIsNotNone(material_result_2, 'Expected nested serializer to create the objects in the database')
		self.assertEqual(normalized_material_2, material_result_2.name)
		material_result_3 = FilterProperty.objects.get(pk=result['materials'][2])
		self.assertIsNotNone(material_result_3, 'Expected nested serializer to create the objects in the database')
		self.assertEqual(normalized_material_3, material_result_3.name)
		material_result_4 = FilterProperty.objects.get(pk=result['materials'][3])
		self.assertIsNotNone(material_result_4, 'Expected nested serializer to create the objects in the database')
		self.assertEqual(normalized_material_4, material_result_4.name)

		light_result_1 = FilterProperty.objects.get(pk=result['lights'][0])
		self.assertIsNotNone(light_result_1, 'Expected nested serializer to create the objects in the database')
		self.assertEqual(normalized_light_1, light_result_1.name)
		light_result_2 = FilterProperty.objects.get(pk=result['lights'][1])
		self.assertIsNotNone(light_result_2, 'Expected nested serializer to create the objects in the database')
		self.assertEqual(normalized_light_2, light_result_2.name)
		light_result_3 = FilterProperty.objects.get(pk=result['lights'][2])
		self.assertIsNotNone(light_result_3, 'Expected nested serializer to create the objects in the database')
		self.assertEqual(normalized_light_3, light_result_3.name)
		light_result_4 = FilterProperty.objects.get(pk=result['lights'][3])
		self.assertIsNotNone(light_result_4, 'Expected nested serializer to create the objects in the database')
		self.assertEqual(normalized_light_4, light_result_4.name)

		#  #4   test if parent element is NOT created.
		filter_properties_count_after_test = FilterProperties.objects.count()
		self.assertEqual(
			filter_properties_count_original, filter_properties_count_after_test,
			'Expected nested serializer not to create a new FilterProperties instance, but {} != {}'.format(
				filter_properties_count_original, filter_properties_count_after_test
			)
		)

	def test_reuse_unique_should_create_new_instead_of_exception(self):
		# When some fields with a one-to-one field have the same content like the user-provided request has,
		# the reuse-filter will find the model instance but a .save operation will throw a uniq-constraint error from the
		# db.  We catch this error and instead create a new instance with the same content.
		# Thus an operation where the same content for this special case is used (written) twice, should not fail, it
		# should succeed.
		test_author_instance = get_user_model().objects.get(pk=2)
		test_description_instance = TextWithHistory.objects.create(content='test_content')
		a_filter_property = FilterProperty.objects.create(
			author=test_author_instance,
			description=test_description_instance,
			name='Test One-To-One-Reuse-Create'
		)

		the_new_filter_property = {
			'author': test_author_instance,
			'description': {'content': 'test_content'},
			'name': 'The description (a TextWithHistory field) should be created properly'
		}

		result = self.serializer.deserialize_nested_data_by_reuse_or_create(
			ElementModel=FilterProperty,
			ElementSerializer=FilterPropertySerializer,
			element=the_new_filter_property,
			produce_model_instances=False
		)

		self.assertNotEqual(
			a_filter_property.description.pk, result['description'],
			'Expected description of test-object 2 to be a duplicate with its own pk.'
		)

	def test_optional_arguments(self):
		verify_create_serializer_succeeds_if_optional_args_missing(self)
