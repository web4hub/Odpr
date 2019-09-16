from django.db import models
from simple_history.models import HistoricalRecords
from odpr_shared_models.models import TextWithHistory, FilterProperties, Report, Tag
from annoying.fields import AutoOneToOneField
from vuedj.settings import AUTH_USER_MODEL
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from filer.fields.image import FilerImageField, FilerFileField

# Create your models here.
class Request(models.Model):

	PUBLIC, LINK, PRIVATE = range(0, 3)

	PrivacyChoices = (
		(PUBLIC, 'Public'),
		(LINK, 'Link'),
		(PRIVATE, 'Private'),
	)

	date_created = models.DateTimeField(default=timezone.now)
	####### Primary key ########
	# ID is implied by django
	author = models.ForeignKey(to=AUTH_USER_MODEL, related_name='requests', on_delete=models.SET_NULL, null=True, blank=False)

	####### Data of this Model #######
	title = models.CharField(max_length=200)
	description = AutoOneToOneField(TextWithHistory, on_delete=models.SET_NULL, null=True)

	filter_properties = AutoOneToOneField(
		to=FilterProperties,
		related_name='request',
		blank=False,
		on_delete=models.CASCADE,
		null=False
	)

	visit_count = models.IntegerField(verbose_name='Viewed', default=0)
	privacy_setting = models.IntegerField(choices=PrivacyChoices, default=PUBLIC)
	is_closed = models.BooleanField(default=False)

	tags = models.ManyToManyField(Tag, related_name='tagged_requests', blank=True)

	def __str__(self):
		""" toString """
		return self.title

	class Meta:
		ordering = ('title',)
		verbose_name_plural = 'Requests'
		app_label = 'scenery_requests'

	def get_upvote_count(self):
		return self.request_upvoters.count()
	get_upvote_count.short_description = 'Upvoted'

	def get_downvote_count(self):
		return self.request_downvoters.count()
	get_downvote_count.short_description = 'Downvoted'

	def get_starred_count(self):
		return self.request_starrers.count()
	get_starred_count.short_description = 'Stars'

	def get_reported_count(self):
		return Report.objects.filter(type=Report.REQUEST, reference=self.pk).count()
	get_reported_count.short_description = 'Reported by'

	def get_final_vote_number(self):
		return self.get_upvote_count() + self.get_downvote_count()
	get_final_vote_number.short_description = 'Vote Rate'


class RequestRelationship(models.Model):
	REQUEST_UPVOTE, REQUEST_DOWNVOTE, REQUEST_STAR, REQUEST_VISIT = range(0, 4)

	RelationshipType = (
		(REQUEST_UPVOTE, 'Request Upvote'),
		(REQUEST_DOWNVOTE, 'Request Downvote'),
		(REQUEST_STAR, 'Starred Request'),
		(REQUEST_VISIT, 'Visited Request'),
	)

	user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
	request = models.ForeignKey(Request, on_delete=models.SET_NULL, null=True)
	date_created = models.DateTimeField(default=timezone.now)
	type = models.IntegerField(choices=RelationshipType)


class RequestTagRelationship(models.Model):
	tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
	request = models.ForeignKey(Request, on_delete=models.SET_NULL, null=True)
	date_created = models.DateTimeField(default=timezone.now)

	class Meta:
		app_label = 'scenery_requests'

	def __str__(self):
		return 'Request: ' + self.request.title + ' - Tag: ' + self.tag.tag


class Answer(models.Model):
	# from scenery_requests.models import Request # by intention within class to resolve cyclic import.
	# import scenery_requests.models as request_models # by intention within class to resolve cyclic import.

	author = models.ForeignKey(to=AUTH_USER_MODEL, related_name='answers', on_delete=models.SET_NULL, null=True)
	# type = models.IntegerField(choices=CommentTypes)
	content = AutoOneToOneField(TextWithHistory, on_delete=models.SET_NULL, null=True, blank=True)
	parent_id = models.ForeignKey(
		to=Request,
		blank=False,
		on_delete=models.CASCADE,
		help_text='The Request to which this answer belongs'
	)
	marked_as_accepted = models.BooleanField(default=False)

	class Meta:
		app_label = 'scenery_requests'
		verbose_name_plural = 'Answers'

	def __str__(self):
		return self.content.content

	def get_link_to_referenced_parent(self):
			return reverse('api:scenery_requests:request-detail', args=[self.parent_id.id])

	def get_upvote_count(self):
		return self.answer_upvoters.count()
	get_upvote_count.short_description = 'Upvoted'

	def get_downvote_count(self):
		return self.answer_downvoters.count()
	get_downvote_count.short_description = 'Downvoted'

	def get_reported_count(self):
		return Report.objects.filter(type=Report.ANSWER, reference=self.pk).count()
	get_reported_count.short_description = 'Reported by'

	def get_final_vote_number(self):
		return self.get_upvote_count() + self.get_downvote_count()
	get_final_vote_number.short_description = 'Vote Rate'


class AnswerRelationship(models.Model):
	ANSWER_UPVOTE, ANSWER_DOWNVOTE = range(0, 2)

	RelationshipType = (
		(ANSWER_UPVOTE, 'Answer Upvote'),
		(ANSWER_DOWNVOTE, 'Answer Downvote')
	)

	class Meta:
		app_label = 'scenery_requests'
		verbose_name_plural = 'Answer Relationships'

	user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
	answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True)
	date_created = models.DateTimeField(default=timezone.now)
	type = models.IntegerField(choices=RelationshipType)


class RequestImage(models.Model):
	author = models.ForeignKey(
		to=AUTH_USER_MODEL,
		related_name='uploaded_request_images',
		on_delete=models.SET_NULL,
		null=True
	)

	date_created = models.DateTimeField(default=timezone.now)

	image = FilerImageField(null=True, blank=True, related_name='request_preview_images', on_delete=models.SET_NULL)

	class Meta:
		app_label = 'scenery_requests'
		verbose_name_plural = 'Request Preview Images'

	request = models.ForeignKey(to=Request, null=False, blank=False, related_name='request_preview_images', on_delete=models.CASCADE)


class RequestFile(models.Model):
	author = models.ForeignKey(
		to=AUTH_USER_MODEL,
		related_name='uploaded_request_files',
		on_delete=models.SET_NULL,
		null=True
	)

	date_created = models.DateTimeField(default=timezone.now)

	file = FilerFileField(null=True, blank=True, related_name='request_files', on_delete=models.SET_NULL)

	class Meta:
		app_label = 'scenery_requests'
		verbose_name_plural = 'Request Files'

	request = models.ForeignKey(to=Request, null=False, blank=False, related_name='request_files', on_delete=models.CASCADE)
