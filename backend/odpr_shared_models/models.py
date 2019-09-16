from annoying.fields import AutoOneToOneField
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils import timezone
from simple_history.models import HistoricalRecords

from vuedj.settings import AUTH_USER_MODEL
from .choices import Actions

'''
	Used for bio, scenery_description, ...
'''
class TextWithHistory(models.Model):
	history = HistoricalRecords()
	content = models.TextField(max_length=2000, blank=True, verbose_name='TextWithHistory', default='')

	class Meta:
		app_label = 'odpr_shared_models'
		verbose_name_plural = 'Texts with History'

	def __str__(self):
		return self.content


'''
	Used for comments, ...
'''
class TextWithHistoryAuthor(models.Model):
	SCENERY_DESCRIPTION = 0
	REQUEST_DESCRIPTION = 1
	COMMENT = 2
	ANSWER = 3

	ContentTypes = (
		(SCENERY_DESCRIPTION, 'Scenery Description'),
		(REQUEST_DESCRIPTION, 'Request Description'),
		(COMMENT, 'Comment'),
		(ANSWER, 'Answer')
	)

	history = HistoricalRecords()
	author = models.ForeignKey(to=AUTH_USER_MODEL, related_name='textual_posts', on_delete=models.SET_NULL, null=True)
	content = models.TextField(max_length=20000, blank=True, verbose_name='TextWithHistory', default='')
	type = models.IntegerField(choices=ContentTypes)

	# num of upvotes and downvotes

	class Meta:
		app_label = 'odpr_shared_models'
		verbose_name_plural = 'Texts with History and Details'

	def __str__(self):
		return self.content


class Badge(models.Model):
	BRONZE = 0
	SILVER = 1
	GOLD = 2

	BadgeTypes = (
		(BRONZE, 'Bronze'),
		(SILVER, 'Silver'),
		(GOLD, 'Gold')
	)

	type = models.IntegerField(choices=BadgeTypes)
	title = models.CharField(blank=False, max_length=100)
	description = models.CharField(blank=False, max_length=1500)

	class Meta:
		app_label = 'odpr_shared_models'

	def __str__(self):
		return self.title

	def get_owned_by_count(self):
		if self.type == Badge.BRONZE:
			return get_user_model().objects.filter(bronze_badges=self.pk).count()
		if self.type == Badge.SILVER:
			return get_user_model().objects.filter(silver_badges=self.pk).count()
		if self.type == Badge.GOLD:
			return get_user_model().objects.filter(gold_badges=self.pk).count()
		return 0
	get_owned_by_count.short_description = 'Owned by'
	# get_owned_by_count.admin_order_field = 'owned_by__count'


class BadgeOwnership(models.Model):
	owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
	badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
	date_received = models.DateTimeField(default=timezone.now)
	viewed = models.BooleanField(default=False, help_text='Whether the user who received this badge has viewed/seen the badge')


# TODO: BadgeMappingTable: a map of constraints which connects the badges to conditionals:
# Some badges occur when the first post is done, some occur when a reputation greater than nnn is achieved, some happen ...
# How to efficiently map this ?


class Report(models.Model):
	USER, SCENERY, REQUEST, COMMENT, ANSWER, DOCUMENTATION = range(0, 6)

	ReportTypes = (
		(USER, 'User'),
		(SCENERY, 'Scenery'),
		(REQUEST, 'Request'),
		(COMMENT, 'Comment'),
		(ANSWER, 'Answer'),
		(DOCUMENTATION, 'Documentation')
	)

	author = models.ForeignKey(to=AUTH_USER_MODEL, related_name='reports', on_delete=models.SET_NULL, null=True)

	type = models.IntegerField(choices=ReportTypes)
	title = models.CharField(blank=False, max_length=100)
	description = models.CharField(blank=True, max_length=1500)
	# reference = models.URLField(blank=False)

	# get the correct referenced content by report.type + referenced ID  (for example the user id, the comment id,
	# which are all unique)
	reference = models.IntegerField(blank=False, help_text='ID to scenery, request, user or comment')
	resolved = models.BooleanField(default=False, help_text='Whether the report has been reviewed and some action (or not)'
																													' was made')

	class Meta:
		app_label = 'odpr_shared_models'

	def __str__(self):
		return self.title

	def get_link_to_referenced_object(self):
		if self.type == Report.USER:
			return reverse('api:accounts:user-detail', args=[self.reference])
		elif self.type == Report.SCENERY:
			return reverse('api:sceneries:scenery-detail', args=[self.reference])
		elif self.type == Report.REQUEST:
			return reverse('api:requests:request-detail', args=[self.reference])
		elif self.type == Report.ANSWER:
			return reverse('api:answers:answer-detail', args=[self.reference])
		elif self.type == Report.DOCUMENTATION:
			return reverse('api:documentation:document-detail', args=[self.reference])
		elif self.type == Report.COMMENT:
			# TODO: first get type of parent (scenery or request), then load the parent with its id, then second parameter in url should be comment id.
			return reverse('api:comments:comment-detail', args=[self.reference]) # TODO adapt for comments


class Comment(models.Model):
	SCENERY_COMMENT = 0
	REQUEST_COMMENT = 1
	REQUEST_ANSWER_COMMENT = 2

	CommentTypes = (
		(SCENERY_COMMENT, 'Scenery Comment'),
		(REQUEST_COMMENT, 'Request Comment'),
		(REQUEST_ANSWER_COMMENT, 'Request-Answer Comment')
	)

	author = models.ForeignKey(to=AUTH_USER_MODEL, related_name='comments', on_delete=models.SET_NULL, null=True)
	type = models.IntegerField(choices=CommentTypes)
	content = AutoOneToOneField(TextWithHistory, on_delete=models.SET_NULL, null=True, blank=True)
	parent_id = models.IntegerField(blank=False, help_text='ID of either the Scenery, the Request or the Answer, to which this comment belongs (depends on configured type of the comment)')

	class Meta:
		app_label = 'odpr_shared_models'
		verbose_name_plural = 'Comments'

	def __str__(self):
		return self.content.content

	def get_link_to_referenced_parent(self):
		if self.type == Comment.SCENERY_COMMENT:
			return reverse('api:sceneries:scenery-detail', args=[self.parent_id])
		elif self.type == Comment.REQUEST_COMMENT:
			return reverse('api:requests:request-detail', args=[self.parent_id])
		elif self.type == Comment.REQUEST_ANSWER_COMMENT:
			return reverse('api:requests:request-detail', args=[self.parent_id]) # TODO: link to answer


class CommentRelationship(models.Model):
	COMMENT_UPVOTE, COMMENT_DOWNVOTE = range(0, 2)

	RelationshipType = (
		(COMMENT_UPVOTE, 'Comment Upvote'),
		(COMMENT_DOWNVOTE, 'Comment Downvote'),
	)

	class Meta:
		app_label = 'odpr_shared_models'
		verbose_name_plural = 'Comment Relationships'

	user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
	comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)
	date_created = models.DateTimeField(default=timezone.now)
	type = models.IntegerField(choices=RelationshipType)


class FilterProperty(models.Model):
	author = models.ForeignKey(
		to=AUTH_USER_MODEL,
		related_name='created_filter_properties',
		on_delete=models.SET_NULL,
		null=True
	)
	description = AutoOneToOneField(TextWithHistory, on_delete=models.SET_NULL, null=True, blank=True)
	name = models.CharField(blank=False, null=False, max_length=40)

	class Meta:
		app_label = 'odpr_shared_models'
		verbose_name_plural = 'Filter Properties'

	def __str__(self):
		return self.name


# TODO: add form to admin and use the manytomany forms for the filters.
class FilterProperties(models.Model):
	MINIMALISTIC, SIMPLE, INTERMEDIATE, COMPLEX = range(0, 4)

	ComplexityType = (
		(MINIMALISTIC, 'Minimalistic'),
		(SIMPLE, 'Simple'),
		(INTERMEDIATE, 'Intermediate'),
		(COMPLEX, 'Complex')
	)

	scenery_complexity = models.IntegerField(choices=ComplexityType)
	effects = models.ManyToManyField(
		to=FilterProperty,
		related_name='effects',
		blank=False,
		help_text='One or more effects (Filter for caustics). If no effect in scene: Choose Effect \'None\''
	)
	materials = models.ManyToManyField(
		to=FilterProperty,
		related_name='materials',
		blank=False,
		help_text='One or more materials (Filter for sceneries). If no material in scene: Choose Material \'None\''
	)
	lights = models.ManyToManyField(
		to=FilterProperty,
		related_name='lights',
		blank=False,
		help_text='One or more lights (Filter for sceneries). If no lights in scene: Choose Light \'None\''
	)

	class Meta:
		app_label = 'odpr_shared_models'
		verbose_name_plural = 'Wrapped Filter Properties'

	def __str__(self):
		return FilterProperties.ComplexityType[self.scenery_complexity][1] +\
				' - Effects: ' + ', '.join(e.name for e in self.effects.all()) +\
				' - Materials: ' + ', '.join(m.name for m in self.materials.all()) +\
				' - Lights: ' + ', '.join(l.name for l in self.lights.all())

	def get_effects_count(self):
		return self.effects.count()
	get_effects_count.short_description = 'Effects'

	def get_materials_count(self):
		return self.materials.count()
	get_materials_count.short_description = 'Materials'

	def get_lights_count(self):
		return self.lights.count()
	get_lights_count.short_description = 'Lights'


class Tag(models.Model):
	date_created = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(to=AUTH_USER_MODEL, related_name='tags', on_delete=models.SET_NULL, null=True,
														 blank=False)

	tag = models.CharField(max_length=45)

	class Meta:
		app_label = 'odpr_shared_models'

	def __str__(self):
		return self.tag


class BadgeRule(models.Model):
	# FIRST_DOCUMENTATION_UPVOTE, FIRST_DOCUMENTATION_DOWNVOTE, FIRST_DOCUMENTATION_STAR\

	# For every manytomany exists only one generic field: Use them twice, once with active, once with passive.
	# if they are conditioned with an occuring-counter, like FIRST, TENTH, HUNDRETH etc., just use one generic,
	# the condition is given by the condition field, and the badge will have the proper explanation.
	Actions = Actions

	ACTIVE, PASSIVE, BIDIRECTIONAL = range(0, 3)

	SignalDirection = (
		(ACTIVE, 'User Action will rule badge-gain of another user'),
		(PASSIVE, 'User Action will rule badge-gain of same user'),
		(BIDIRECTIONAL, 'User Action will rule badge-gain of same user AND another user'),
	)
	# key will be compared by the BadgeSignalHandler with the signal the handler got.

	key = models.IntegerField(choices=Actions, blank=False, null=False)
	condition = models.IntegerField(blank=False, null=False,
																	help_text='Amount of reputation or actions needed to grant badge')
	badges = models.ManyToManyField(Badge, related_name='rules', blank=True)
	signal_direction = models.IntegerField(
		choices=SignalDirection,
		help_text='Whether the badgeSignal will lead to a badge on this user or on the receiving user. The receiving means, '
							'the user who will suffer from the action of this user.',
		blank=False,
		null=False
	)

	class Meta:
		app_label = 'odpr_shared_models'


class ProfileImage(models.Model):
	from filer.fields.image import FilerImageField

	author = models.ForeignKey(
		to=AUTH_USER_MODEL,
		related_name='uploaded_profile_images',
		on_delete=models.SET_NULL,
		null=True
	)

	date_created = models.DateTimeField(default=timezone.now)

	image = FilerImageField(null=True, blank=True, related_name='profile_images', on_delete=models.SET_NULL)

	class Meta:
		app_label = 'odpr_shared_models'
		verbose_name_plural = 'Profile Images'

	# user = models.ForeignKey(to=AUTH_USER_MODEL, null=False, blank=False, related_name='profile_images', on_delete=models.CASCADE)


class ReputationRule(models.Model):
	# FIRST_DOCUMENTATION_UPVOTE, FIRST_DOCUMENTATION_DOWNVOTE, FIRST_DOCUMENTATION_STAR\

	# For every manytomany exists only one generic field: Use them twice, once with active, once with passive.
	# if they are conditioned with an occuring-counter, like FIRST, TENTH, HUNDRETH etc., just use one generic,
	# the condition is given by the condition field, and the badge will have the proper explanation.
	Actions = Actions

	# key will be compared by the UserActionSignalHandler with the signal the handler got.

	key = models.IntegerField(choices=Actions, blank=False, null=False)
	condition = models.IntegerField(blank=False, null=False, help_text='Amount of reputation needed to permit User Action.')

	class Meta:
		app_label = 'odpr_shared_models'


class Notification(models.Model):
	user = models.ForeignKey(to=AUTH_USER_MODEL, blank=False, null=False, on_delete=models.CASCADE, related_name='notifications')
	content = models.CharField(blank=False, null=False, max_length=2000)

	class Meta:
		app_label = 'odpr_shared_models'


class Log(models.Model):
	ip = models.GenericIPAddressField()
	request_body = models.TextField(blank=True, default='')
	request_method = models.CharField(default='GET', max_length=30)
	date = models.DateTimeField(default=timezone.now)
