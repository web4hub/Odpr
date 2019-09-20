from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from rest_framework.utils import model_meta
from rest_framework import serializers
from collections import OrderedDict
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError
from rest_framework.fields import get_error_detail, set_value
from rest_framework.fields import SkipField, empty
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import traceback
import copy


class IllegalArgumentError(ValueError):
	pass


class NestedModelSerializer(serializers.ModelSerializer):
	"""
		There are readonly fields predefined for GET, POST, PUT, PATCH, DELETE.
		They have the default value 'id'.
		Override them in Subclass to add or change readonly fields depending on the
		request action.
		The request type (serializer_type) is defined through an constructor argument.
		This argument is optional and per default NestedCreateModelSerializer.GET
		Child Serializers are expected to be _declared_fields and will be of the same
		serializer_type as their parent serializer.
		There is also the option to set the serializer_type via override as a field in the
		class instead of a constructor parameter. The constructor parameter will override the
		declared/overwritten field.
	"""
	GET, POST, PUT, PATCH = range(0, 4)
	SerializerType = (
		(GET, 'Get'),
		(POST, 'Post'),
		(PUT, 'Put'),
		(PATCH, 'Patch')
	)

	list_serializer = False  # defined by serializer arg many=True
	serializer_type = GET
	read_write_get_fields = ('id',)
	post_fields = ('id', )
	put_fields = ('id', )
	patch_fields = ('id', )
	readonly_get_fields = ('id', )
	readonly_post_fields = ('id', )
	readonly_put_fields = ()
	readonly_patch_fields = ()

	def __init__(self, instance=None, data=empty, **kwargs):
		kwargs.pop('serializer_type', None)
		self.update_children_serializer_types()
		super(NestedModelSerializer, self).__init__(instance, data, **kwargs)

	@classmethod
	def __new__(cls, *args, **kwargs):
		serializer_type = kwargs.pop('serializer_type', None)
		cls.set_serializer_type(serializer_type)
		#if cls.serializer_type is NestedModelSerializer.GET:
		#	kwargs['read_only'] = True
		return super(NestedModelSerializer, cls).__new__(*args, **kwargs)

	@classmethod
	def set_list_type(cls, list_type=True):
		if list_type is not None:
			cls.list_serializer = list_type

	@property
	def data(self):
		ret = super(NestedModelSerializer, self).data
		for key, value in ret.items():
			if value is None:
				ret.update({key: {}})
		return ret

	@classmethod
	def get_readonly_fields_by_serializer_type(cls):
		if cls.serializer_type == NestedModelSerializer.GET:
			return cls.get_readonly_get_fields()
		elif cls.serializer_type == NestedModelSerializer.POST:
			return cls.get_readonly_post_fields()
		elif cls.serializer_type == NestedModelSerializer.PUT:
			return cls.get_readonly_put_fields()
		elif cls.serializer_type == NestedModelSerializer.PATCH:
			return cls.get_readonly_patch_fields()
		raise IndexError('Invalid serializer type provided. Can only be one of 0, 1, 2, 3')

	@classmethod
	def get_fields_by_serializer_type(cls):
		if cls.serializer_type == NestedModelSerializer.GET:
			return cls.get_get_fields()
		elif cls.serializer_type == NestedModelSerializer.POST:
			return cls.get_post_fields()
		elif cls.serializer_type == NestedModelSerializer.PUT:
			return cls.get_put_fields()
		elif cls.serializer_type == NestedModelSerializer.PATCH:
			return cls.get_patch_fields()
		raise IndexError('Invalid serializer type provided. Can only be one of 0, 1, 2, 3')

	@classmethod
	def set_serializer_type(cls, serializer_type):
		if serializer_type is not None:
			cls.serializer_type = serializer_type
		cls.update_fields()
		cls.update_readonly_fields()
		# cls.update_id_readonly_flag()

	def update_id_readonly_flag(self):
		if self.serializer_type == NestedModelSerializer.PUT or self.serializer_type == NestedModelSerializer.PATCH:
			if hasattr(self.fields, 'fields'):
				self.fields.fields['id'] = serializers.IntegerField(read_only=False)
				self.fields.fields['id'].field_name = self.fields.fields['id'].source = 'id'
				self.fields.fields['id'].source_attrs = ['id', ]
				if '_writable_fields' in self.__dict__:
					del self.__dict__['_writable_fields']  # invalidate cached property _writable_fields, so next call will update it.

	def update_file_date_readonly_flag(self):
		if hasattr(self.fields, 'fields'):
			if 'uploaded_at' in self.fields.fields:
				self.fields.fields['uploaded_at'] = serializers.DateTimeField(default=timezone.now)
			if 'modified_at' in self.fields.fields:
				self.fields.fields['modified_at'] = serializers.DateTimeField(default=timezone.now)

	@classmethod
	def update_children_serializer_types(cls):
		if cls.serializer_type is not None:
			for key in cls._declared_fields:
				if isinstance(cls._declared_fields[key], NestedModelSerializer):
					cls._declared_fields[key].set_serializer_type(cls.serializer_type)
					cls._declared_fields[key].update_children_serializer_types()
				elif hasattr(cls._declared_fields[key], 'child') and isinstance(cls._declared_fields[key].child, NestedModelSerializer):
					if cls.serializer_type is not NestedModelSerializer.GET:
						cls._declared_fields[key].read_only = False
						cls._declared_fields[key].child.read_only = False
					cls._declared_fields[key].child.set_serializer_type(cls.serializer_type)
					cls._declared_fields[key].child.update_children_serializer_types()

	@classmethod
	def get_readonly_get_fields(cls):
		return cls.readonly_get_fields

	@classmethod
	def get_readonly_post_fields(cls):
		return cls.readonly_post_fields

	@classmethod
	def get_readonly_put_fields(cls):
		return cls.readonly_put_fields

	@classmethod
	def get_readonly_patch_fields(cls):
		return cls.readonly_patch_fields

	@classmethod
	def update_readonly_fields(cls):
		if hasattr(cls, 'Meta'):
			cls.Meta.read_only_fields = cls.get_readonly_fields_by_serializer_type()

	@classmethod
	def get_get_fields(cls):
		return cls.read_write_get_fields

	@classmethod
	def get_post_fields(cls):
		return cls.post_fields

	@classmethod
	def get_put_fields(cls):
		return cls.put_fields

	@classmethod
	def get_patch_fields(cls):
		return cls.patch_fields

	@classmethod
	def update_fields(cls):
		if hasattr(cls, 'Meta'):
			cls.Meta.fields = cls.get_fields_by_serializer_type()

	def create(self, validated_data):
		"""
			We have a bit of extra checking around this in order to provide
			descriptive messages when something goes wrong, but this method is
			essentially just:

					return ExampleModel.objects.create(**validated_data)

			If there are many to many fields present on the instance then they
			cannot be set until the model is instantiated, in which case the
			implementation is like so:

					example_relationship = validated_data.pop('example_relationship')
					instance = ExampleModel.objects.create(**validated_data)
					instance.example_relationship = example_relationship
					return instance

			The default implementation also does not handle nested relationships.
			If you want to support writable nested relationships you'll need
			to write an explicit `.create()` method.
			"""
		# raise_errors_on_nested_writes('create', self, validated_data)

		ModelClass = self.Meta.model

		# Remove many-to-many relationships from validated_data.
		# They are not valid arguments to the default `.create()` method,
		# as they require that the instance has already been saved.
		info = model_meta.get_field_info(ModelClass)
		many_to_many = {}
		for field_name, relation_info in info.relations.items():
			if relation_info.to_many and (field_name in validated_data):
				many_to_many[field_name] = validated_data.pop(field_name)

		try:
			instance = ModelClass.objects.create(**validated_data)
		except TypeError:
			tb = traceback.format_exc()
			msg = (
				'Got a `TypeError` when calling `%s.objects.create()`. '
				'This may be because you have a writable field on the '
				'serializer class that is not a valid argument to '
				'`%s.objects.create()`. You may need to make the field '
				'read-only, or override the %s.create() method to handle '
				'this correctly.\nOriginal exception was:\n %s' %
				(
					ModelClass.__name__,
					ModelClass.__name__,
					self.__class__.__name__,
					tb
				)
			)
			raise TypeError(msg)

		# Save many-to-many relationships after the instance is created.
		if many_to_many:
			for field_name, value in many_to_many.items():
				field = getattr(instance, field_name)
				field.set(value)

		return instance

	def to_internal_value(self, data):
		"""
			Dict of native values <- Dict of primitive datatypes.
			"""
		#if self.serializer_type is not NestedModelSerializer.POST:
		#	return super(NestedModelSerializer, self).to_internal_value(data)
		# Changed: Do not check mapping. Now we can use both strings and integers.
		self.error_messages = {
			'does_not_exist': _('Something went wrong during nested deserialization: Object "{pk_value}" should have an '
													'instance but could not be found'),
			'incorrect_type': _('Something went wrong during nested deserialization: Object has incorrect type: "{data_type}"'),
		}

		self.update_id_readonly_flag()
		#self.update_file_date_readonly_flag()

		ret = OrderedDict()
		errors = OrderedDict()
		fields = self._writable_fields

		remembered_serializer_type = self.serializer_type  # Needed to restore the serializer type which is modified during
		newly_created_object = self.create_new_element_if_update_or_patch_and_id_missing(  # ... this operation
			data=data, ElementModel=self.__class__.Meta.model, ElementSerializer=self.__class__
		)
		self.set_serializer_type(remembered_serializer_type)  # restore serializer type.
		if isinstance(newly_created_object, models.Model):
			return newly_created_object  # return pk of newly created object instead of further validation
		#  else: object had id for update/patch, or serializer is not for update/patch, proceed with normal validation...

		for field in fields:
			validate_method = getattr(self, 'validate_' + field.field_name, None)
			try:
				primitive_value = field.get_value(data)
				try:
					validated_value = field.run_validation(primitive_value)
					if validate_method is not None:
						validated_value = validate_method(validated_value)
				except ValidationError as exc:
					errors[field.field_name] = exc.detail
				except DjangoValidationError as exc:
					errors[field.field_name] = get_error_detail(exc)
				except SkipField:
					pass
				except TypeError:
					set_value(ret, field.source_attrs, primitive_value)
				else:
					set_value(ret, field.source_attrs, validated_value)
			except AttributeError:
				try:
					return self.Meta.model.objects.get(pk=data)
				except ObjectDoesNotExist:
					self.fail('does_not_exist', pk_value=data)
				except (TypeError, ValueError):
					if isinstance(data, models.Model):
						self.instance = data
						return data
					self.fail('incorrect_type', data_type=type(data).__name__)

		if errors:
			raise ValidationError(errors)

		if 'id' in ret:  # set instance for the update requests.
			self.instance = self.Meta.model.objects.get(pk=ret['id'])
		return ret

	def update(self, instance, validated_data):
		# removed errors on nested update.
		info = model_meta.get_field_info(instance)

		validated_data.pop('id', None)
		# Simply set each attribute on the instance, and then save it.
		# Note that unlike `.create()` we don't need to treat many-to-many
		# relationships as being a special case. During updates we already
		# have an instance pk for the relationships to be associated with.
		for attr, value in validated_data.items():
			if attr in info.relations and info.relations[attr].to_many:
				field = getattr(instance, attr)
				field.set(value)
			else:
				setattr(instance, attr, value)
		instance.save()

		return instance

	def run_validation(self, data=empty):
		"""
			We override the default `run_validation`, because the validation
			performed by validators and the `.validate()` method should
			be coerced into an error dictionary with a 'non_fields_error' key.
			"""
		# if self.serializer_type is not NestedModelSerializer.POST:
		#	return super(NestedModelSerializer, self).run_validation(data)
		(is_empty_value, data) = self.validate_empty_values(data)
		if is_empty_value:
			return data

		value = self.to_internal_value(data)
		try:
			try:
				self.run_validators(value)
			except (ValueError, TypeError):
				pass
			else:
				pass
			value = self.validate(value)
			assert value is not None, '.validate() should return the validated data'
		except (ValidationError, DjangoValidationError) as exc:
			raise ValidationError('ValidationError in serializer_util:run_validation occurred.')

		return value

	def overwritten_save_for_nested_update(self, **kwargs):
		assert not hasattr(self, 'save_object'), (
			'Serializer `%s.%s` has old-style version 2 `.save_object()` '
			'that is no longer compatible with REST framework 3. '
			'Use the new-style `.create()` and `.update()` methods instead.' %
			(self.__class__.__module__, self.__class__.__name__)
		)

		assert hasattr(self, '_errors'), (
			'You must call `.is_valid()` before calling `.save()`.'
		)

		assert not self.errors, (
			'You cannot call `.save()` on a serializer with invalid data.'
		)

		# Guard against incorrect use of `serializer.save(commit=False)`
		assert 'commit' not in kwargs, (
			"'commit' is not a valid keyword argument to the 'save()' method. "
			"If you need to access data before committing to the database then "
			"inspect 'serializer.validated_data' instead. "
			"You can also pass additional keyword arguments to 'save()' if you "
			"need to set extra attributes on the saved model instance. "
			"For example: 'serializer.save(owner=request.user)'.'"
		)

		# removed check for _data field for nested updater.

		validated_data = dict(
			list(self.validated_data.items()) +
			list(kwargs.items())
		)

		validated_data.pop('id', None)

		if self.instance is not None:
			self.instance = self.update(self.instance, validated_data)
			assert self.instance is not None, (
				'`update()` did not return an object instance.'
			)
		else:
			raise AssertionError('Something went wrong during nested update. The instance is None but should be a valid '
													 'instance.')
		return self.instance

	def create_new_element_if_update_or_patch_and_id_missing(self, data, ElementModel, ElementSerializer):
		if isinstance(data, dict) \
			and (self.serializer_type is NestedModelSerializer.PUT or self.serializer_type is NestedModelSerializer.PATCH) \
			and 'id' not in data:
				result = self.deserialize_nested_data_by_reuse_or_create(
					element=data, ElementModel=ElementModel, ElementSerializer=ElementSerializer, save_root_as_instance=True
				)
				return result
		return None

	def get_reuse_filter_by_serializer_type(self, serializer):
		"""
		:return: a LIST of filterfunctions mapped to the given serializer or an empty list.
		"""
		from .reuse_filter_map import serializer_reuse_filter_map
		# if nothing found return None
		for key in serializer_reuse_filter_map:
			if isinstance(serializer, type(key)):  # #8  (see doc of serialize_nested_data_by_reuse_or_create for reference)
				return serializer_reuse_filter_map[key]  # returns a LIST!
		return []
		# if many functions for one key: ALWAYS define a list in the map!

	@staticmethod
	def get_final_element_serializer(element, ElementSerializer, serializer_type=POST):
		try:
			return ElementSerializer(data=element, serializer_type=serializer_type)
		except TypeError:
			try:
				return ElementSerializer.__class__(data=element, serializer_type=serializer_type)
			except TypeError:
				return None

	@staticmethod
	def save_new_element(final_element_serializer, **kwargs):
		if final_element_serializer is not None:
			final_element_serializer.is_valid(raise_exception=True)
			return final_element_serializer.save(**kwargs)
		return None

	@staticmethod
	def get_child_model_class(key, parent, ParentModel):
		child = parent[key]
		if isinstance(child, dict) or isinstance(child, list):
			try:
				child_field_in_model = getattr(ParentModel, key)
				return child_field_in_model.field.related_model
			except AttributeError:
				pass
		return None

	@staticmethod
	def get_child_serializer_class(ChildModel):
		from .model_create_serializer_map import model_create_serializer_map
		if ChildModel is not None:
			return model_create_serializer_map[ChildModel.__name__]
		return None

	@staticmethod
	def validate_args(ElementModel, ElementSerializer):
		if ElementSerializer is None:
			raise IllegalArgumentError('ElementSerializer must not be None if element is a dict! This error can also mean,'
																 ' that your provided serialized data is not correctly formatted (e.g. wrong or '
																 'invalid nested elements, too many or too less elements, invalid types of nested'
																 ' elements etc.')
		if ElementModel is None:
			raise IllegalArgumentError('ElementModel must not be None if element is a dict! This error can also mean,'
																 ' that your provided serialized data is not correctly formatted (e.g. wrong or '
																 'invalid nested elements, too many or too less elements, invalid types of nested'
																 ' elements etc.')

	def deserialize_nested_data_by_reuse_or_create(
		self,
		element,
		ElementModel=None,
		ElementSerializer=None,
		produce_model_instances=True,
		save_root_as_instance=False
	):
		""" Cases:
		#1	element = int     e.g. element = 4,
																					element is an IntegerField's value. just return it. can never be a pk as
																					such a reference can only occur in a dict.
					expected output: same value same type
		#2	element = str			e.g. element = 'blla bla bla'
																					element is an CharField's or TextField's value. just return it.
					expected output: same value same type
		#3	element = Model   e.g. element = FilterProperty containing data. A real python instance of the Model-Class!
																					This happens because django-rest-framework will already deserialize incoming
																					data at the very beginning and will try to wrap such data into their
																					corresponding python instances. Then what we have here is what we actually want
																					to have later already. But we don't need it now, so we just return element.pk,
																					as the pk, the reference to this element's instance is actually needed.
					expected output: primary key of instance
		#4  element = list    e.g. element = [3, 4, 7, 11]  a list of primary keys, or [3, {'key': [3, 5]}, 8] a list with
																					nested objects AND primary keys mixed. A list can only contain nested objects,
																					this means that this function shall never return primitives as they are. also,
																					a list cannot contain primitives: It is not possible for a foreign key or a
																					many-to-many field to directly be a IntegerField or so. It can also not
																					contain a list, because a foreign key or many-to-many can only be represented
																					by a PK, a model instance or a dict. the nested dict however, can again
																					contain everything from #1 to #5.

																					The element_model and element_serializer passed to a list should be the model
																					and serializer of the individual object in the list.
																					e.g. effects = models.ManyToManyField(to=FilterProperty,...) then the
																					element_model is "FilterProperty".
													element = [<any_of_#1_#3_#5>, <any_of_#1_#3_#5>, ...]
					expected output:    again a list, only containing primary keys
						element = dict    This one is more complicated:
		#5		                element = {'key': <any_of_#1_#2_#3_#4_#5>}
																					#1 to #3    mean primitive values, easy.
																					#4          a list as value, can contain again #1 to #5
																					#5 as value means, there is some foreign, non-primitive field in the serializer/
																					model, and the value for this field is represented as another dict in order to
																					be able to either:
																						1. reuse
																						2. create
																					the new/already-existing instance. The field named 'key' can only be another
																					serializer within the current element_serializer.
					expected output:    again a dict: reusing an existing if possible and allowed, then with its PK as value instead
															of the other stuff, OR create a new one also with PK as value. primitive values stay
															primitive and are not replaced by PKs.
		#6		special case 1:									1. The dict has many keys. Solution: Just iterate over those keys and do the
																						same operation on all of them.
		#7		special case 2:									2. A value in the dict is a list of something. Just iterate over those elements
																						and do the same for all of them.
		#8		special case 3:									3. There is a serializer in the current element_serializer and the given data is
																						a dict. The data contained in the dict matches an instance which already
																						exists in the database. Normally, we would reuse this instance. But there are
																						many cases where a reuse cannot be applied, for example if the instance is
																						related to a One-To-One field somewhere else. Then we have to create a new
																						instance instead.
				Note for dicts:				Parent level of recursion always gets back a dict from this function. Inside (nested) dicts
															will always be resolved to primary keys in place of the input-dicts. A dict with no nested
															values will NOT create a new object. A dict with nested values will create only the nested
															objects. The parent dict will be created outside this function.

				:param ElementModel: The model of the provided element as Class
				:param ElementSerializer: The create-serializer of the provided element as Class
				:param element: The element to deserialize. Nested dicts and related fields will be created or reused.
				:param produce_model_instances: True, if returned object should contain model instances instead of PK values for
																				relation fields. False if pk values (int) should be used instead.
																				This parameter cannot be false when save_root_as_instance is true.
				:param save_root_as_instance: True, if the returned element should be an instance, False if the returned element
																			should be a dict, to be saved outside. This parameter cannot be true when
																			produce_model_instances is false.
				:return: Always the same type of the input element. A dict will return a dict, a list will return a list etc.
		"""
		def deserialize_dict(ElementModel, ElementSerializer, element):
			nonlocal self

			def init_flags(reuse_filter_functions):
				create_new = multiple_objects_returned = type_or_value_error_occurred = False
				if reuse_filter_functions is None or len(reuse_filter_functions) == 0:
					create_new = True
				return create_new, multiple_objects_returned, type_or_value_error_occurred

			def run_lookup_in_database_and_update_flags(element, ElementModel, reuse_filter_functions):
				def validate_object_reusability(element, ElementModel):
					from .models import TextWithHistory
					'''  if relation is one-to-one: raise ObjectDoesNotExist manually here, re-use is not possible. '''
					# info = model_meta.get_field_info(element_model)
					# for field_name, relation_info in info.relations.items():
					# 	if relation_info.to_one and (field_name in element):
					# TODO: debug this and find out how to find out whether a field is one-to-one.
					if ElementModel is TextWithHistory:
						raise ObjectDoesNotExist()  # for now we always create a new instance.

				nonlocal create_new, multiple_objects_returned, type_or_value_error_occurred
				found_element = None
				for filter_function in reuse_filter_functions:
					try:
						validate_object_reusability(element=element, ElementModel=ElementModel)
						found_element = ElementModel.objects.get(**filter_function(element))
					except ObjectDoesNotExist:
						create_new = True
					except MultipleObjectsReturned:
						multiple_objects_returned = True
					except (TypeError, ValueError):
						type_or_value_error_occurred = True
				return found_element

			def recurse_create_or_reuse_nested_elements(element, ElementSerializer):
				some_dict = {}
				# of every manually declared field inside the current active serializer
				for key, value in element.items():  # #6 try to match one key inside the current active element
					if key in ElementSerializer._declared_fields:
						nested_serializer = ElementSerializer._declared_fields[key]
						# by their names only if the field inside the current serializer is another serializer.
						if isinstance(nested_serializer, serializers.ListSerializer):
							nested_serializer = nested_serializer.child
						if isinstance(nested_serializer, serializers.Serializer):
							some_dict[key] = deserialize_nested_data_by_reuse_or_create__recursion(
								ElementModel=nested_serializer.Meta.model,
								ElementSerializer=nested_serializer,
								element=value
							)
					elif type(value) is int or type(value) is str or isinstance(value, models.Model):
						some_dict[key] = deserialize_nested_data_by_reuse_or_create__recursion(element=value)
				return some_dict

			def reuse_or_create_new(element, ElementModel, ElementSerializer, reuse_filter_functions):
				nonlocal self, create_new, multiple_objects_returned, type_or_value_error_occurred
				final_element = None
				if not create_new:
					final_element = run_lookup_in_database_and_update_flags(
						element=element,
						ElementModel=ElementModel,
						reuse_filter_functions=reuse_filter_functions
					)

				if create_new:
					# update content in element with possible new pk values instead of the original text values.
					element.update(recurse_create_or_reuse_nested_elements(element=element, ElementSerializer=ElementSerializer))
					final_element_serializer = self.get_final_element_serializer(
						element=element, ElementSerializer=ElementSerializer
					)
					final_element = self.save_new_element(final_element_serializer)
				return final_element

			def report_failure():
				nonlocal multiple_objects_returned, type_or_value_error_occurred
				if multiple_objects_returned:
					raise ValueError('Create Serializer encountered ambigious invalid value in nested related object.')
				if type_or_value_error_occurred:
					raise ValueError('Create Serializer encountered invalid value in nested related object.')
				raise ValueError('Create Serializer was not able to deserialize received dict element.')

			##################    Start of   deserialize_dict   #################
			self.validate_args(ElementModel=ElementModel, ElementSerializer=ElementSerializer)
			reuse_filter_functions = self.get_reuse_filter_by_serializer_type(ElementSerializer)
			create_new, multiple_objects_returned, type_or_value_error_occurred = init_flags(reuse_filter_functions)

			final_element = reuse_or_create_new(
				element=element,
				ElementModel=ElementModel,
				ElementSerializer=ElementSerializer,
				reuse_filter_functions=reuse_filter_functions
			)

			if final_element is not None:
				return final_element.pk
			else:
				report_failure()

		def deserialize_list(ElementModel, ElementSerializer, data):
			''' Passed model and serializer must be for the individual elements of the list, not for the parent of the list. '''
			validated_elements = []
			for element in data:
				validated_elements.append(
					deserialize_nested_data_by_reuse_or_create__recursion(
						ElementModel=ElementModel,
						ElementSerializer=ElementSerializer,
						element=element
					)
				)
			return validated_elements

		def deserialize_primitive(element):
			return element

		def deserialize_model_instance(element):
			return element.pk

		def pk_to_model_instances(element, ElementModel):
			result = copy.deepcopy(element)
			for key, value in element.items():
				if type(value) is int:
					ChildModel = None
					try:
						ChildModel = getattr(ElementModel, key).field.related_model
					except (KeyboardInterrupt, SystemExit):
						raise
					except:
						pass
					if ChildModel is not None:
						result[key] = ChildModel.objects.get(pk=value)  # raises exception which is ok.
			return result

		def deserialize_nested_data_by_reuse_or_create__recursion(
			element,
			ElementModel=None,
			ElementSerializer=None
		):
			if isinstance(element, dict):  # #5 to #8
				return deserialize_dict(ElementModel=ElementModel, ElementSerializer=ElementSerializer, element=element)
			elif isinstance(element, list):  # #4
				return deserialize_list(ElementModel=ElementModel, ElementSerializer=ElementSerializer, data=element)
			elif type(element) is int or type(element) is str:
				return deserialize_primitive(element)  # #1 and #2
			elif isinstance(element, models.Model):
				return deserialize_model_instance(element)  # #3
			raise TypeError('Create Serializer was not able to deserialize received type of element.')

		############################################  Start of serialize_nested_data_by_reuse_or_create ######################
		if not produce_model_instances and save_root_as_instance:
			raise IllegalArgumentError('produce_model_instances and save_root_as_instance cannot be true at the same time.')
		if isinstance(element, dict):
			final_element = {}
			for key in element:
				ChildModel = self.get_child_model_class(key, element, ElementModel)
				ChildSerializer = self.get_child_serializer_class(ChildModel)
				final_element[key] = deserialize_nested_data_by_reuse_or_create__recursion(
					ElementModel=ChildModel,
					ElementSerializer=ChildSerializer,
					element=element[key]
				)
			if produce_model_instances:
				final_element.update(pk_to_model_instances(final_element, ElementModel))
			if save_root_as_instance:
				final_element_serializer = self.get_final_element_serializer(
					element=final_element, ElementSerializer=ElementSerializer
				)  # TODO: provide serializer type from outside instead by self.serializer_type and resolve recursion.
				final_element = self.save_new_element(final_element_serializer)
			return final_element
		else:
			return deserialize_nested_data_by_reuse_or_create__recursion(
				element=element,
				ElementModel=ElementModel,
				ElementSerializer=ElementSerializer
			)

	def deserialize_nested_update(self, element, ElementModel, ElementSerializer, **kwargs):
		def resolve_nested(element, ElementModel, ElementSerializer, **kwargs):
			nonlocal self, RootSerializer
			self.validate_args(ElementModel, ElementSerializer)
			if 'id' not in element:
				raise KeyError('The provided data must have an id in order to be able to update it.')
			if isinstance(element, dict):
				final_dict = copy.deepcopy(element)
				for key, value in element.items():
					if isinstance(element[key], dict):
						ChildModel = self.get_child_model_class(key=key, parent=element, ParentModel=ElementModel)
						ChildSerializer = self.get_child_serializer_class(ChildModel)
						final_dict[key] = resolve_nested(
							element=element[key], ElementModel=ChildModel, ElementSerializer=ChildSerializer
						)
				if RootSerializer is not ElementSerializer:
					update_serializer = self.get_final_element_serializer(
						element=final_dict, ElementSerializer=ElementSerializer, serializer_type=NestedModelSerializer.PUT
					)  # TODO: provide serializer type from outside instead by self.serializer_type and resolve recursion.
					final_element = self.save_new_element(update_serializer, **kwargs)
					return final_element
				else:
					return final_dict
			raise TypeError('Deserialize nested update function only accepts dict as input.')

		RootSerializer = ElementSerializer
		return resolve_nested(element, ElementModel, ElementSerializer, **kwargs)
