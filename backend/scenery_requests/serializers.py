from .models import Request, RequestTagRelationship, RequestFile, RequestImage, RequestRelationship, Answer, \
	AnswerRelationship
from .permissions import ADMIN_REQUEST_DETAIL_DATA_ACCESS_FULL, \
	STAFF_REQUEST_DETAIL_DATA_ACCESS_FULL, \
	AUTHENTICATED_SELF_REQUEST_DETAIL_DATA_ACCESS_FULL, \
	AUTHENTICATED_OTHER_REQUEST_DETAIL_DATA_ACCESS_FULL, \
	UNAUTHENTICATED_REQUEST_DETAIL_DATA_ACCESS_FULL, \
	ADMIN_REQUEST_DETAIL_READ_ONLY_DATA_ACCESS, AUTHENTICATED_OTHER_REQUEST_DETAIL_READ_ONLY_DATA_ACCESS, \
	AUTHENTICATED_SELF_REQUEST_DETAIL_READ_ONLY_DATA_ACCESS, STAFF_REQUEST_DETAIL_READ_ONLY_DATA_ACCESS, \
	UNAUTHENTICATED_REQUEST_DETAIL_READ_ONLY_DATA_ACCESS, ADMIN_REQUEST_LIST_DATA_ACCESS_FULL, \
	ADMIN_REQUEST_LIST_READ_ONLY_DATA_ACCESS, STAFF_REQUEST_LIST_DATA_ACCESS_FULL, \
	STAFF_REQUEST_LIST_READ_ONLY_DATA_ACCESS, AUTHENTICATED_REQUEST_LIST_DATA_ACCESS_FULL, \
	AUTHENTICATED_REQUEST_LIST_READ_ONLY_DATA_ACCESS, UNAUTHENTICATED_REQUEST_LIST_DATA_ACCESS_FULL, \
	UNAUTHENTICATED_REQUEST_LIST_READ_ONLY_DATA_ACCESS
from odpr_shared_models.serializers import TextWithHistorySerializer, FilterPropertiesSerializer, \
	TagSerializer
from odpr_shared_models.serializer_util import NestedModelSerializer
from rest_framework.fields import empty

class RequestSerializer(NestedModelSerializer):
	ADMIN, STAFF, AUTHOR, VIEWER, GUEST = range(0, 5)
	permission_type = GUEST  # defined by request.user (type and authentication=True/False)

	description = TextWithHistorySerializer()
	filter_properties = FilterPropertiesSerializer()
	tags = TagSerializer(many=True)

	class Meta:
		model = Request
		# Fields and readonly fields are defined by the overwritten methods below!

	def create(self, validated_data):
		validated_data.update(self.deserialize_nested_data_by_reuse_or_create(
			ElementModel=Request,
			ElementSerializer=RequestSerializer,
			element=validated_data
		))
		return super(RequestSerializer, self).create(validated_data)

	def save(self, **kwargs):
		if self.serializer_type is NestedModelSerializer.PUT or self.serializer_type is NestedModelSerializer.PATCH:
			self.validated_data.update(self.deserialize_nested_update(
				ElementModel=Request,
				ElementSerializer=RequestSerializer,
				element=self.validated_data,
				**kwargs
			))
			return self.overwritten_save_for_nested_update(**kwargs)
		else:
			return super(RequestSerializer, self).save(**kwargs)

	def __init__(self, instance=None, data=empty, **kwargs):
		kwargs.pop('permission_type', None)
		super(RequestSerializer, self).__init__(instance, data, **kwargs)

	@classmethod
	def __new__(cls, *args, **kwargs):
		serializer_type = kwargs.pop('serializer_type', None)
		cls.set_serializer_type(serializer_type)
		permission_type = kwargs.pop('permission_type', None)
		list_serializer = kwargs.get('many', None)
		cls.set_list_type(list_serializer)
		cls.set_permission_type(permission_type)
		return super(NestedModelSerializer, cls).__new__(*args, **kwargs)

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
			if cls.permission_type is RequestSerializer.GUEST:
				return UNAUTHENTICATED_REQUEST_LIST_READ_ONLY_DATA_ACCESS
			elif cls.permission_type is RequestSerializer.VIEWER or cls.permission_type is RequestSerializer.AUTHOR:
				return AUTHENTICATED_REQUEST_LIST_READ_ONLY_DATA_ACCESS
			elif cls.permission_type is RequestSerializer.STAFF:
				return STAFF_REQUEST_LIST_READ_ONLY_DATA_ACCESS
			elif cls.permission_type is RequestSerializer.ADMIN:
				return ADMIN_REQUEST_LIST_READ_ONLY_DATA_ACCESS
		else:
			if cls.permission_type is RequestSerializer.GUEST:
				return UNAUTHENTICATED_REQUEST_DETAIL_READ_ONLY_DATA_ACCESS
			elif cls.permission_type is RequestSerializer.VIEWER:
				return AUTHENTICATED_OTHER_REQUEST_DETAIL_READ_ONLY_DATA_ACCESS
			elif cls.permission_type is RequestSerializer.AUTHOR:
				return AUTHENTICATED_SELF_REQUEST_DETAIL_READ_ONLY_DATA_ACCESS
			elif cls.permission_type is RequestSerializer.STAFF:
				return STAFF_REQUEST_DETAIL_READ_ONLY_DATA_ACCESS
			elif cls.permission_type is RequestSerializer.ADMIN:
				return ADMIN_REQUEST_DETAIL_READ_ONLY_DATA_ACCESS
		raise IndexError('Invalid permission type: Can only be one of 0, 1, 2, 3!')

	@classmethod
	def get_get_fields(cls):
		if cls.list_serializer:
			if cls.permission_type is RequestSerializer.GUEST:
				return UNAUTHENTICATED_REQUEST_LIST_DATA_ACCESS_FULL
			elif cls.permission_type is RequestSerializer.VIEWER or cls.permission_type is RequestSerializer.AUTHOR:
				return AUTHENTICATED_REQUEST_LIST_DATA_ACCESS_FULL
			elif cls.permission_type is RequestSerializer.STAFF:
				return STAFF_REQUEST_LIST_DATA_ACCESS_FULL
			elif cls.permission_type is RequestSerializer.ADMIN:
				return ADMIN_REQUEST_LIST_DATA_ACCESS_FULL
		else:
			if cls.permission_type is RequestSerializer.GUEST:
				return UNAUTHENTICATED_REQUEST_DETAIL_DATA_ACCESS_FULL
			elif cls.permission_type is RequestSerializer.VIEWER:
				return AUTHENTICATED_OTHER_REQUEST_DETAIL_DATA_ACCESS_FULL
			elif cls.permission_type is RequestSerializer.AUTHOR:
				return AUTHENTICATED_SELF_REQUEST_DETAIL_DATA_ACCESS_FULL
			elif cls.permission_type is RequestSerializer.STAFF:
				return STAFF_REQUEST_DETAIL_DATA_ACCESS_FULL
			elif cls.permission_type is RequestSerializer.ADMIN:
				return ADMIN_REQUEST_DETAIL_DATA_ACCESS_FULL
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

class RequestRelationshipSerializer(NestedModelSerializer):  # TODO: write tests
	""" Here are request votes stored/created/updated. A vote is the 'type' """
	request = RequestSerializer()
	readonly_get_fields = read_write_get_fields = post_fields = put_fields = patch_fields = (
		'id', 'user', 'request', 'date_created', 'type'
	)
	readonly_put_fields = readonly_patch_fields = (
		'user', 'request', 'date_created'
	)
	readonly_post_fields = ('id',) + readonly_put_fields

	class Meta:
		model = RequestRelationship
		# fields and read_only_fields are set in NestedModelSerializer!

class RequestTagRelationshipSerializer(NestedModelSerializer):  # TODO: write tests
	tag = TagSerializer()
	request = RequestSerializer()
	readonly_get_fields = read_write_get_fields = post_fields = put_fields = patch_fields = (
		'id', 'tag', 'request', 'date_created'
	)
	readonly_put_fields = readonly_patch_fields = (
		'tag', 'request', 'date_created'
	)
	readonly_post_fields = ('id',) + readonly_put_fields

	class Meta:
		model = RequestTagRelationship
		# fields and read_only_fields are set in NestedModelSerializer!

class AnswerSerializer(NestedModelSerializer):  # TODO: write tests
	content = TextWithHistorySerializer()
	readonly_get_fields = read_write_get_fields = post_fields = put_fields = patch_fields = (
		'id', 'author', 'content', 'parent_id', 'marked_as_accepted', 'get_link_to_referenced_parent',
		'get_upvote_count', 'get_downvote_count', 'get_reported_count', 'get_final_vote_number'
	)
	readonly_put_fields = readonly_patch_fields = (
		'author', 'parent_id', 'get_link_to_referenced_parent',
		'get_upvote_count', 'get_downvote_count', 'get_reported_count', 'get_final_vote_number'
	)
	readonly_post_fields = ('id',) + readonly_put_fields

	class Meta:
		model = Answer
		# fields and read_only_fields are set in NestedModelSerializer!

class AnswerRelationshipSerializer(NestedModelSerializer):  # TODO: write tests
	""" Here are request votes stored/created/updated. A vote is the 'type' """
	answer = AnswerSerializer()
	readonly_get_fields = read_write_get_fields = post_fields = put_fields = patch_fields = (
		'id', 'user', 'answer', 'date_created', 'type'
	)
	readonly_put_fields = readonly_patch_fields = (
		'user', 'answer', 'date_created'
	)
	readonly_post_fields = ('id',) + readonly_put_fields

	class Meta:
		model = AnswerRelationship
		# fields and read_only_fields are set in NestedModelSerializer!

class RequestImageSerializer(NestedModelSerializer):  # TODO: write tests
	request = RequestSerializer()
	readonly_get_fields = read_write_get_fields = post_fields = put_fields = patch_fields = (
		'id', 'author', 'image', 'date_created', 'request'
	)
	readonly_put_fields = readonly_patch_fields = (
		'request', 'date_created'
	)
	readonly_post_fields = ('id',) + readonly_put_fields

	class Meta:
		model = RequestImage
		# fields and read_only_fields are set in NestedModelSerializer!

class RequestFileSerializer(NestedModelSerializer):  # TODO: write tests
	request = RequestSerializer()
	readonly_get_fields = read_write_get_fields = post_fields = put_fields = patch_fields = (
		'id', 'author', 'file', 'date_created', 'request'
	)
	readonly_put_fields = readonly_patch_fields = (
		'request', 'date_created'
	)
	readonly_post_fields = ('id',) + readonly_put_fields

	class Meta:
		model = RequestFile
		# fields and read_only_fields are set in NestedModelSerializer!
