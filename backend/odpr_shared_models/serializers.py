from rest_framework import serializers
from .models import TextWithHistory, FilterProperties, Tag, FilterProperty, ReputationRule, BadgeRule, Badge, \
	BadgeOwnership, Report, Comment, CommentRelationship, ProfileImage, Notification
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings
from rest_framework.relations import PrimaryKeyRelatedField
from odpr_shared_models.serializer_util import \
	NestedModelSerializer
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils.translation import ugettext_lazy as _
from filer.models.filemodels import File
from filer.models.imagemodels import Image

class TextWithHistorySerializer(NestedModelSerializer):
	readonly_get_fields = read_write_get_fields = post_fields = put_fields = patch_fields = ('id', 'content')

	class Meta:
		model = TextWithHistory
		# fields and read_only_fields are set in NestedModelSerializer!


class FilterPropertySerializer(NestedModelSerializer):
	description = TextWithHistorySerializer()
	readonly_get_fields = read_write_get_fields = post_fields = put_fields = patch_fields = (
		'id', 'author', 'description', 'name'
	)

	class Meta:
		model = FilterProperty
		# fields and read_only_fields are set in NestedModelSerializer!


class FilterPropertiesSerializer(NestedModelSerializer):
	effects = FilterPropertySerializer(many=True)
	materials = FilterPropertySerializer(many=True)
	lights = FilterPropertySerializer(many=True)
	readonly_get_fields = read_write_get_fields = post_fields = put_fields = patch_fields = (
		'id', 'scenery_complexity', 'effects', 'materials', 'lights'
	)

	class Meta:
		model = FilterProperties
		# fields and read_only_fields are set in NestedModelSerializer!

	def create(self, validated_data):
		validated_data.update(self.deserialize_nested_data_by_reuse_or_create(
			ElementModel=FilterProperties,
			ElementSerializer=FilterPropertiesSerializer,
			element=validated_data
		))
		return super(FilterPropertiesSerializer, self).create(validated_data)

	def save(self, **kwargs):
		if self.serializer_type is NestedModelSerializer.PUT or self.serializer_type is NestedModelSerializer.PATCH:
			self.validated_data.update(self.deserialize_nested_update(
				ElementModel=FilterProperties,
				ElementSerializer=FilterPropertiesSerializer,
				element=self.validated_data,
				**kwargs
			))
			return self.overwritten_save_for_nested_update(**kwargs)
		else:
			return super(FilterPropertiesSerializer, self).save(**kwargs)


class TagSerializer(NestedModelSerializer):
	readonly_get_fields = read_write_get_fields = post_fields = put_fields = patch_fields = ('id', 'author', 'tag')

	class Meta:
		model = Tag
		# fields and read_only_fields are set in NestedModelSerializer!


class ReputationRuleSerializer(NestedModelSerializer):  # TODO: write tests
	readonly_get_fields = read_write_get_fields = post_fields = put_fields = patch_fields = ('id', 'key', 'condition')

	class Meta:
		model = ReputationRule
		# fields and read_only_fields are set in NestedModelSerializer!


class BadgeSerializer(NestedModelSerializer):  # TODO: write tests
	readonly_get_fields = read_write_get_fields = post_fields = put_fields = patch_fields = (
		'id', 'type', 'title', 'description'
	)

	class Meta:
		model = Badge
		# fields and read_only_fields are set in NestedModelSerializer!

class BadgeRuleSerializer(NestedModelSerializer):  # TODO: write tests
	badges = BadgeSerializer(many=True)
	readonly_get_fields = read_write_get_fields = post_fields = put_fields = patch_fields = (
		'id', 'key', 'condition', 'badges', 'signal_direction', 'get_owned_by_count'
	)
	readonly_put_fields = readonly_patch_fields = ('get_owned_by_count',)
	readonly_post_fields = ('id',) + readonly_put_fields

	class Meta:
		model = BadgeRule
		# fields and read_only_fields are set in NestedModelSerializer!

	def create(self, validated_data):
		validated_data.update(self.deserialize_nested_data_by_reuse_or_create(
			ElementModel=BadgeRule,
			ElementSerializer=BadgeRuleSerializer,
			element=validated_data
		))
		return super(BadgeRuleSerializer, self).create(validated_data)

	def save(self, **kwargs):
		if self.serializer_type is NestedModelSerializer.PUT or self.serializer_type is NestedModelSerializer.PATCH:
			self.validated_data.update(self.deserialize_nested_update(
				ElementModel=BadgeRule,
				ElementSerializer=BadgeRuleSerializer,
				element=self.validated_data,
				**kwargs
			))
			return self.overwritten_save_for_nested_update(**kwargs)
		else:
			return super(BadgeRuleSerializer, self).save(**kwargs)

class BadgeOwnershipSerializer(NestedModelSerializer):  # TODO: write tests
	badge = BadgeSerializer()
	readonly_get_fields = read_write_get_fields = post_fields = put_fields = patch_fields = (
		'id', 'owner', 'badge', 'date_received', 'viewed'
	)
	readonly_put_fields = readonly_patch_fields = ('owner', 'badge', 'date_received')
	readonly_post_fields = ('id',) + readonly_put_fields

	class Meta:
		model = BadgeOwnership
		# fields and read_only_fields are set in NestedModelSerializer!

class ReportSerializer(NestedModelSerializer):  # TODO: write tests
	readonly_get_fields = read_write_get_fields = post_fields = put_fields = patch_fields = (
		'id', 'author', 'type', 'title', 'description', 'reference', 'get_link_to_referenced_object', 'resolved'
	)
	readonly_put_fields = readonly_patch_fields = (
		'author', 'get_link_to_referenced_object', 'resolved'
	)
	readonly_post_fields = ('id',) + readonly_put_fields

	class Meta:
		model = Report
		# fields and read_only_fields are set in NestedModelSerializer!

class CommentSerializer(NestedModelSerializer):  # TODO: write tests
	content = TextWithHistorySerializer()
	readonly_get_fields = read_write_get_fields = post_fields = put_fields = patch_fields = (
		'id', 'author', 'type', 'content', 'parent_id', 'get_link_to_referenced_parent'
	)
	readonly_put_fields = readonly_patch_fields = (
		'author', 'type', 'reference', 'get_link_to_referenced_parent'
	)
	readonly_post_fields = ('id',) + readonly_put_fields

	class Meta:
		model = Comment
		# fields and read_only_fields are set in NestedModelSerializer!

class CommentRelationshipSerializer(NestedModelSerializer):  # TODO: write tests
	""" Here are comment votes stored/created/updated. A vote is the 'type' """
	comment = CommentSerializer()
	readonly_get_fields = read_write_get_fields = post_fields = put_fields = patch_fields = (
		'id', 'user', 'comment', 'date_created', 'type'
	)
	readonly_put_fields = readonly_patch_fields = (
		'user', 'comment', 'date_created'
	)
	readonly_post_fields = ('id',) + readonly_put_fields

	class Meta:
		model = CommentRelationship
		# fields and read_only_fields are set in NestedModelSerializer!

class ProfileImageSerializer(NestedModelSerializer):  # TODO: write tests
	readonly_get_fields = read_write_get_fields = post_fields = put_fields = patch_fields = (
		'id', 'author', 'image', 'date_created'
	)
	readonly_put_fields = readonly_patch_fields = (
		'date_created',
	)
	readonly_post_fields = ('id',) + readonly_put_fields

	class Meta:
		model = ProfileImage
		# fields and read_only_fields are set in NestedModelSerializer!

class NotificationSerializer(NestedModelSerializer):  # TODO: write tests
	readonly_get_fields = read_write_get_fields = post_fields = put_fields = patch_fields = (
		'id', 'user', 'content'
	)

	class Meta:
		model = Notification
		# fields and read_only_fields are set in NestedModelSerializer!

class FileSerializer(NestedModelSerializer):
	readonly_get_fields = read_write_get_fields = post_fields = put_fields = patch_fields = (
		'id', 'file', 'sha1', 'original_filename', 'name', 'description', 'owner', 'uploaded_at', 'modified_at',
		'is_public', 'label', 'url', 'canonical_url', 'size', 'extension'
	)
	readonly_put_fields = readonly_patch_fields = (
		'sha1', 'label', 'url', 'canonical_url', 'size', 'extension'
	)
	readonly_post_fields = ('id',) + readonly_put_fields

	class Meta:
		model = File
		# fields and read_only_fields are set in NestedModelSerializer!

class ImageSerializer(NestedModelSerializer):
	file_ptr = FileSerializer()
	readonly_get_fields = read_write_get_fields = post_fields = put_fields = patch_fields = (
		'id', 'file_ptr', 'author', 'default_alt_text', 'default_caption', 'sidebar_image_ratio', 'label', 'width',
		'height', 'icons', 'thumbnails', 'uploaded_at', 'modified_at'
	)
	readonly_put_fields = readonly_patch_fields = (
		'sidebar_image_ratio', 'width', 'height', 'icons', 'thumbnails'
	)
	readonly_post_fields = ('id', ) + readonly_put_fields

	# TODO: add these serializers to the base serializer and in the views prepare the data dict with these nested values.
	class Meta:
		model = Image
		# fields and read_only_fields are set in NestedModelSerializer!
