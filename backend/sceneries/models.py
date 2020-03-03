from django.db import models
from odpr_shared_models.models import TextWithHistory, FilterProperty, FilterProperties, Report, Tag
from annoying.fields import AutoOneToOneField
from vuedj.settings import AUTH_USER_MODEL
from django.utils import timezone
from filer.fields.image import FilerImageField, FilerFileField


# Create your models here.
class Scenery(models.Model):
	PUBLIC, LINK, PRIVATE = range(0, 3)

	PrivacyChoices = (
		(PUBLIC, 'Public'),
		(LINK, 'Link'),
		(PRIVATE, 'Private'),
	)

	####### Primary key ########
	# ID is implied by django
	date_created = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(to=AUTH_USER_MODEL, related_name='sceneries', on_delete=models.SET_NULL, null=True, blank=False)

	####### Data of this Model #######
	title = models.CharField(max_length=200)
	description = AutoOneToOneField(TextWithHistory, on_delete=models.SET_NULL, null=True)

	filter_properties = AutoOneToOneField(
		to=FilterProperties,
		related_name='scenery',
		blank=False,
		on_delete=models.CASCADE,
		null=False
	)

	visit_count = models.IntegerField(verbose_name='Viewed', default=0)
	download_count = models.IntegerField(verbose_name='Downloads', default=0)

	privacy_setting = models.IntegerField(choices=PrivacyChoices, default=PUBLIC)

	is_closed = models.BooleanField(default=False)

	tags = models.ManyToManyField(Tag, related_name='tagged_sceneries', blank=True)
	# preview_images computed through ImageWrapper.scenery_previews
	# files computed.

	def __str__(self):
		""" toString """
		return self.title

	class Meta:
		ordering = ('title',)
		verbose_name_plural = 'Sceneries'
		app_label = 'sceneries'

	def get_upvote_count(self):
		return self.scenery_upvoters.count()
	get_upvote_count.short_description = 'Upvoted'

	def get_downvote_count(self):
		return self.scenery_downvoters.count()
	get_downvote_count.short_description = 'Downvoted'

	def get_starred_count(self):
		return self.scenery_starrers.count()
	get_starred_count.short_description = 'Stars'

	def get_reported_count(self):
		return Report.objects.filter(type=Report.SCENERY, reference=self.pk).count()
	get_reported_count.short_description = 'Reported by'

	def get_final_vote_number(self):
		return self.get_upvote_count() + self.get_downvote_count()
	get_final_vote_number.short_description = 'Vote Rate'

	def get_images(self):
		finalImageList = []
		for image in self.preview_images.all():
			finalImageList.append({
				'id': image.id,
				'url': image.image.canonical_url,
				'size': image.image.file.size,
				'width': image.image.width,
				'height': image.image.height,
				'name': image.image.original_filename,
				'sha1': image.image.sha1,
				'date': image.image.uploaded_at
			})
		return finalImageList

	def get_files(self):
		finalFileList = []
		for file in self.scenery_files.all():
			finalFileList.append({
				'id': file.id,
				'url': file.file.canonical_url,
				'size': file.file.size,
				'name': file.file.original_filename,
				'sha1': file.file.sha1,
				'date': file.file.uploaded_at
			})
		return finalFileList

	# TODO: add get_comment_count


class SceneryRelationship(models.Model):
	SCENERY_UPVOTE, SCENERY_DOWNVOTE, SCENERY_STAR, SCENERY_VISIT, SCENERY_DOWNLOAD = range(0, 5)

	RelationshipType = (
		(SCENERY_UPVOTE, 'Scenery Upvote'),
		(SCENERY_DOWNVOTE, 'Scenery Downvote'),
		(SCENERY_STAR, 'Starred Scenery'),
		(SCENERY_VISIT, 'Visited Scenery'),
		(SCENERY_DOWNLOAD, 'Scenery Download'),
	)

	user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
	scenery = models.ForeignKey(Scenery, on_delete=models.SET_NULL, null=True)
	date_created = models.DateTimeField(default=timezone.now)
	type = models.IntegerField(choices=RelationshipType)


class SceneryTagRelationship(models.Model):
	tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
	scenery = models.ForeignKey(Scenery, on_delete=models.SET_NULL, null=True)
	date_created = models.DateTimeField(default=timezone.now)

	class Meta:
		app_label = 'sceneries'

	def __str__(self):
		return 'Scenery: ' + self.scenery.title + ' - Tag: ' + self.tag.tag


class SceneryImage(models.Model):
	author = models.ForeignKey(
		to=AUTH_USER_MODEL,
		related_name='uploaded_scenery_images',
		on_delete=models.SET_NULL,
		null=True
	)

	date_created = models.DateTimeField(default=timezone.now)

	image = FilerImageField(null=True, blank=True, related_name='scenery_preview_images', on_delete=models.SET_NULL)

	class Meta:
		app_label = 'sceneries'
		verbose_name_plural = 'Scenery Preview Images'

	scenery = models.ForeignKey(to=Scenery, null=False, blank=False, related_name='preview_images', on_delete=models.CASCADE)

	def __str__(self):
		return self.image.url


class SceneryFile(models.Model):
	author = models.ForeignKey(
		to=AUTH_USER_MODEL,
		related_name='uploaded_scenery_files',
		on_delete=models.SET_NULL,
		null=True
	)

	date_created = models.DateTimeField(default=timezone.now)

	file = FilerFileField(null=True, blank=True, related_name='scenery_files', on_delete=models.SET_NULL)

	class Meta:
		app_label = 'sceneries'
		verbose_name_plural = 'Scenery Files'

	scenery = models.ForeignKey(to=Scenery, null=False, blank=False, related_name='scenery_files', on_delete=models.CASCADE)
