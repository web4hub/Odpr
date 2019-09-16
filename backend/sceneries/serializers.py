from .models import Scenery, SceneryRelationship, SceneryTagRelationship, SceneryFile, SceneryImage
from .permissions import ADMIN_SCENERY_DETAIL_DATA_ACCESS_FULL, \
	STAFF_SCENERY_DETAIL_DATA_ACCESS_FULL, \
	AUTHENTICATED_SELF_SCENERY_DETAIL_DATA_ACCESS_FULL, \
	AUTHENTICATED_OTHER_SCENERY_DETAIL_DATA_ACCESS_FULL, \
	UNAUTHENTICATED_SCENERY_DETAIL_DATA_ACCESS_FULL, \
	ADMIN_SCENERY_DETAIL_READ_ONLY_DATA_ACCESS, AUTHENTICATED_OTHER_SCENERY_DETAIL_READ_ONLY_DATA_ACCESS, \
	AUTHENTICATED_SELF_SCENERY_DETAIL_READ_ONLY_DATA_ACCESS, STAFF_SCENERY_DETAIL_READ_ONLY_DATA_ACCESS, \
	UNAUTHENTICATED_SCENERY_DETAIL_READ_ONLY_DATA_ACCESS, ADMIN_SCENERY_LIST_DATA_ACCESS_FULL, \
	ADMIN_SCENERY_LIST_READ_ONLY_DATA_ACCESS, STAFF_SCENERY_LIST_DATA_ACCESS_FULL, \
	STAFF_SCENERY_LIST_READ_ONLY_DATA_ACCESS, AUTHENTICATED_SCENERY_LIST_DATA_ACCESS_FULL, \
	AUTHENTICATED_SCENERY_LIST_READ_ONLY_DATA_ACCESS, UNAUTHENTICATED_SCENERY_LIST_DATA_ACCESS_FULL, \
	UNAUTHENTICATED_SCENERY_LIST_READ_ONLY_DATA_ACCESS
from odpr_shared_models.serializers import TextWithHistorySerializer, FilterPropertiesSerializer, \
	TagSerializer, ImageSerializer, FileSerializer
from odpr_shared_models.serializer_util import NestedModelSerializer
from rest_framework.fields import empty

class ScenerySerializer(NestedModelSerializer):
	ADMIN, STAFF, AUTHOR, VIEWER, GUEST = range(0, 5)
	permission_type = GUEST  # defined by request.user (type and authentication=True/False)

	description = TextWithHistorySerializer()
	filter_properties = FilterPropertiesSerializer()
	tags = TagSerializer(many=True)

	class Meta:
		model = Scenery
		# Fields and readonly fields are defined by the overwritten methods below!

	def create(self, validated_data):
		validated_data.update(self.deserialize_nested_data_by_reuse_or_create(
			ElementModel=Scenery,
			ElementSerializer=ScenerySerializer,
			element=validated_data
		))
		return super(ScenerySerializer, self).create(validated_data)

	def save(self, **kwargs):
		if self.serializer_type is NestedModelSerializer.PUT or self.serializer_type is NestedModelSerializer.PATCH:
			self.validated_data.update(self.deserialize_nested_update(
				ElementModel=Scenery,
				ElementSerializer=ScenerySerializer,
				element=self.validated_data,
				**kwargs
			))
			return self.overwritten_save_for_nested_update(**kwargs)
		else:
			return super(ScenerySerializer, self).save(**kwargs)

	def __init__(self, instance=None, data=empty, **kwargs):
		kwargs.pop('permission_type', None)
		super(ScenerySerializer, self).__init__(instance, data, **kwargs)

	@classmethod
	def __new__(cls, *args, **kwargs):
		serializer_type = kwargs.pop('serializer_type', None)
		cls.set_serializer_type(serializer_type)
		permission_type = kwargs.pop('permission_type', None)
		list_serializer = kwargs.get('many', None)
		cls.set_list_type(list_serializer)
		cls.set_permission_type(permission_type)
		return super(ScenerySerializer, cls).__new__(*args, **kwargs)

	@classmethod
	def set_permission_type(cls, permission_type):
		if permission_type is not None:
			if type(permission_type) is not int:
				raise TypeError('permission_type must be int.')
			if permission_type < 0 or permission_type >= 5:
				raise ValueError('permission_type can only be one of 0, 1, 2, 3, 4')
			cls.permission_type = permission_type
		cls.update_fields()
		cls.update_readonly_fields()

	@classmethod
	def get_readonly_get_fields(cls):
		if cls.list_serializer:
			if cls.permission_type is ScenerySerializer.GUEST:
				return UNAUTHENTICATED_SCENERY_LIST_READ_ONLY_DATA_ACCESS
			elif cls.permission_type is ScenerySerializer.VIEWER or cls.permission_type is ScenerySerializer.AUTHOR:
				return AUTHENTICATED_SCENERY_LIST_READ_ONLY_DATA_ACCESS
			elif cls.permission_type is ScenerySerializer.STAFF:
				return STAFF_SCENERY_LIST_READ_ONLY_DATA_ACCESS
			elif cls.permission_type is ScenerySerializer.ADMIN:
				return ADMIN_SCENERY_LIST_READ_ONLY_DATA_ACCESS
		else:
			if cls.permission_type is ScenerySerializer.GUEST:
				return UNAUTHENTICATED_SCENERY_DETAIL_READ_ONLY_DATA_ACCESS
			elif cls.permission_type is ScenerySerializer.VIEWER:
				return AUTHENTICATED_OTHER_SCENERY_DETAIL_READ_ONLY_DATA_ACCESS
			elif cls.permission_type is ScenerySerializer.AUTHOR:
				return AUTHENTICATED_SELF_SCENERY_DETAIL_READ_ONLY_DATA_ACCESS
			elif cls.permission_type is ScenerySerializer.STAFF:
				return STAFF_SCENERY_DETAIL_READ_ONLY_DATA_ACCESS
			elif cls.permission_type is ScenerySerializer.ADMIN:
				return ADMIN_SCENERY_DETAIL_READ_ONLY_DATA_ACCESS
		raise IndexError('Invalid permission type: Can only be one of 0, 1, 2, 3!')

	@classmethod
	def get_get_fields(cls):
		if cls.list_serializer:
			if cls.permission_type is ScenerySerializer.GUEST:
				return UNAUTHENTICATED_SCENERY_LIST_DATA_ACCESS_FULL
			elif cls.permission_type is ScenerySerializer.VIEWER or cls.permission_type is ScenerySerializer.AUTHOR:
				return AUTHENTICATED_SCENERY_LIST_DATA_ACCESS_FULL
			elif cls.permission_type is ScenerySerializer.STAFF:
				return STAFF_SCENERY_LIST_DATA_ACCESS_FULL
			elif cls.permission_type is ScenerySerializer.ADMIN:
				return ADMIN_SCENERY_LIST_DATA_ACCESS_FULL
		else:
			if cls.permission_type is ScenerySerializer.GUEST:
				return UNAUTHENTICATED_SCENERY_DETAIL_DATA_ACCESS_FULL
			elif cls.permission_type is ScenerySerializer.VIEWER:
				return AUTHENTICATED_OTHER_SCENERY_DETAIL_DATA_ACCESS_FULL
			elif cls.permission_type is ScenerySerializer.AUTHOR:
				return AUTHENTICATED_SELF_SCENERY_DETAIL_DATA_ACCESS_FULL
			elif cls.permission_type is ScenerySerializer.STAFF:
				return STAFF_SCENERY_DETAIL_DATA_ACCESS_FULL
			elif cls.permission_type is ScenerySerializer.ADMIN:
				return ADMIN_SCENERY_DETAIL_DATA_ACCESS_FULL
		raise IndexError('Invalid permission type: Can only be one of 0, 1, 2, 3!')

	@classmethod
	def get_post_fields(cls):
		return 'id', 'author', 'title', 'description', 'filter_properties', 'privacy_setting', 'tags'

	@classmethod
	def get_put_fields(cls):
		return cls.get_post_fields()

	@classmethod
	def get_patch_fields(cls):
		return cls.get_post_fields()

class SceneryRelationshipSerializer(NestedModelSerializer):  # TODO: write tests
	""" Here are scenery votes stored/created/updated. A vote is the 'type' """
	scenery = ScenerySerializer()
	readonly_get_fields = read_write_get_fields = post_fields = put_fields = patch_fields = (
		'id', 'user', 'scenery', 'date_created', 'type'
	)
	readonly_put_fields = readonly_patch_fields = (
		'user', 'scenery', 'date_created'
	)
	readonly_post_fields = ('id',) + readonly_put_fields

	class Meta:
		model = SceneryRelationship
		# fields and read_only_fields are set in NestedModelSerializer!

class SceneryTagRelationshipSerializer(NestedModelSerializer):  # TODO: write tests
	tag = TagSerializer()
	scenery = ScenerySerializer()
	readonly_get_fields = read_write_get_fields = post_fields = put_fields = patch_fields = (
		'id', 'tag', 'scenery', 'date_created'
	)
	readonly_put_fields = readonly_patch_fields = (
		'tag', 'scenery', 'date_created'
	)
	readonly_post_fields = ('id',) + readonly_put_fields

	class Meta:
		model = SceneryTagRelationship
		# fields and read_only_fields are set in NestedModelSerializer!

class SceneryImageSerializer(NestedModelSerializer):  # TODO: write tests
	scenery = ScenerySerializer()
	image = ImageSerializer()
	readonly_get_fields = read_write_get_fields = post_fields = put_fields = patch_fields = (
		'id', 'author', 'image', 'date_created', 'scenery'
	)
	readonly_put_fields = readonly_patch_fields = (
		'scenery', 'date_created'
	)
	readonly_post_fields = ('id',) + readonly_put_fields

	class Meta:
		model = SceneryImage
		# fields and read_only_fields are set in NestedModelSerializer!

class SceneryFileSerializer(NestedModelSerializer):  # TODO: write tests
	scenery = ScenerySerializer()
	file = FileSerializer()
	readonly_get_fields = read_write_get_fields = post_fields = put_fields = patch_fields = (
		'id', 'author', 'file', 'date_created', 'scenery'
	)
	readonly_put_fields = readonly_patch_fields = (
		'scenery', 'date_created'
	)
	readonly_post_fields = ('id',) + readonly_put_fields

	class Meta:
		model = SceneryFile
		# fields and read_only_fields are set in NestedModelSerializer!
