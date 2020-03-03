from django import forms
from odpr_shared_models.models import Tag
from accounts.form_helpers import general_model_multiple_choice_field
from .models import Request, RequestTagRelationship


class RequestChangeForm(forms.ModelForm):
	"""
	Only used for the manytomany field tags. Needed to create the association model when creating a relationship.
	"""

	tags = general_model_multiple_choice_field(model=Tag, verbose_name='Tags')

	class Meta:
		model = Request
		fields = (
			'date_created',
			'author',
			'title',
			'description',
			'filter_properties',
			'visit_count',
			'privacy_setting',
			'is_closed',
			'tags'
		)

	def __init__(self, *args, **kwargs):
		super(RequestChangeForm, self).__init__(*args, **kwargs)

		if self.instance and self.instance.pk:
			self.fields['tags'] = general_model_multiple_choice_field(Tag, 'Tags', self.instance.pk)

	def save(self, commit=True):
		request = super().save(commit=False)
		request.save()
		self.update_tags_relationships()
		request.save()
		return request

	def update_tags_relationships(self):
		final_tags = self.cleaned_data['tags'].all()
		if 'tags' in self.initial:
			initial_tags = self.initial['tags']
		else:
			initial_tags = []
		for tag in final_tags:
			if tag not in initial_tags:
				RequestTagRelationship.objects.create(request=self.instance, tag=tag)
		for tag in initial_tags:
			if tag not in final_tags:
				RequestTagRelationship.objects.filter(request=self.instance, tag=tag).delete()
