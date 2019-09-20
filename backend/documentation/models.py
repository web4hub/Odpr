from django.db import models
from django.utils import timezone
from odpr_shared_models.models import TextWithHistory
from annoying.fields import AutoOneToOneField
from vuedj.settings import AUTH_USER_MODEL
from filer.fields.image import FilerImageField, FilerFileField


class DocumentationTag(models.Model):
	date_created = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(to=AUTH_USER_MODEL, related_name='documentation_tags', on_delete=models.SET_NULL, null=True,
														 blank=False)

	tag = models.CharField(max_length=45, unique=True)

	class Meta:
		app_label = 'documentation'

	def __str__(self):
		return self.tag


class Document(models.Model):
	PUBLIC, LINK, STAFF, PRIVATE = range(0, 4)

	PrivacyChoices = (
		(PUBLIC, 'Public'),
		(LINK, 'Link'),
		(STAFF, 'Staff'),
		(PRIVATE, 'Private')
	)

	date_created = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(to=AUTH_USER_MODEL, related_name='documents', on_delete=models.SET_NULL, null=True,
														 blank=False)

	####### Data of this Model #######
	title = models.CharField(max_length=200)
	description = AutoOneToOneField(TextWithHistory, on_delete=models.SET_NULL, null=True)

	visit_count = models.IntegerField(verbose_name='Viewed', default=0)
	privacy_setting = models.IntegerField(choices=PrivacyChoices, default=PUBLIC)

	tags = models.ManyToManyField(DocumentationTag, related_name='tagged_documents', blank=True)

	class Meta:
		app_label = 'documentation'

	def __str__(self):
		return self.title


class DocumentationImage(models.Model):
	author = models.ForeignKey(
		to=AUTH_USER_MODEL,
		related_name='uploaded_documentation_images',
		on_delete=models.SET_NULL,
		null=True
	)

	date_created = models.DateTimeField(default=timezone.now)

	image = FilerImageField(null=True, blank=True, related_name='documentation_images', on_delete=models.SET_NULL)

	class Meta:
		app_label = 'documentation'
		verbose_name_plural = 'Documentation Images'

	document = models.ForeignKey(to=Document, null=False, blank=False, related_name='document_images', on_delete=models.CASCADE)


class DocumentationFile(models.Model):
	author = models.ForeignKey(
		to=AUTH_USER_MODEL,
		related_name='uploaded_documentation_files',
		on_delete=models.SET_NULL,
		null=True
	)

	date_created = models.DateTimeField(default=timezone.now)

	file = FilerFileField(null=True, blank=True, related_name='documentation_files', on_delete=models.SET_NULL)

	class Meta:
		app_label = 'documentation'
		verbose_name_plural = 'Documentation Files'

	document = models.ForeignKey(to=Document, null=False, blank=False, related_name='documentation_files', on_delete=models.CASCADE)
