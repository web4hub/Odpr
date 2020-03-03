from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from sceneries.models import SceneryRelationship
from scenery_requests.models import RequestRelationship
from odpr_shared_models.models import CommentRelationship
from scenery_requests.models import AnswerRelationship


def general_model_multiple_choice_field(model, verbose_name, exclude_pk=-1):
	queryset = model.objects.all()
	if exclude_pk != -1:
		queryset = queryset.exclude(pk=exclude_pk)
	return forms.ModelMultipleChoiceField(
		queryset=queryset,
		required=False,
		widget=FilteredSelectMultiple(
			verbose_name=verbose_name,
			is_stacked=False
		)
	)


def general_model_multiple_choice_field_filter_type(model, verbose_name, filter_by_type):
	queryset = model.objects.all()
	if filter:
		queryset = queryset.filter(type=filter_by_type)
	return forms.ModelMultipleChoiceField(
		queryset=queryset,
		required=False,
		widget=FilteredSelectMultiple(
			verbose_name=verbose_name,
			is_stacked=False
		)
	)


def general_queryset_multiple_choice_field_filter_type(queryset, verbose_name, filter_by_type):
	if filter:
		queryset = queryset.filter(type=filter_by_type)
	return forms.ModelMultipleChoiceField(
		queryset=queryset,
		required=False,
		widget=FilteredSelectMultiple(
			verbose_name=verbose_name,
			is_stacked=False
		)
	)


def update_answer_vote_relations(self, target_attribute, opposite_attribute, vote_type, opposite_type):
	def create_filter_function(inner_self, target):
		return {'user': inner_self.instance, 'answer': target, 'type': vote_type}

	def create_opposite_filter_function(inner_self, target):
		return {'user': inner_self.instance, 'answer': target, 'type': opposite_type}

	def create_delete_filter_function(inner_self, target):
		return {'user': inner_self.instance, 'answer': target, 'type': vote_type}

	update_votes_relations(
		self=self,
		relation_model=AnswerRelationship,
		source_model_reference_field=target_attribute,
		source_model_opposite_reference_field=opposite_attribute,
		create_filter=create_filter_function,
		create_opposite_filter=create_opposite_filter_function,
		create_delete_filter=create_delete_filter_function
	)


def update_comment_vote_relations(self, target_attribute, opposite_attribute, vote_type, opposite_type):
	def create_filter_function(inner_self, target):
		return {'user': inner_self.instance, 'comment': target, 'type': vote_type}

	def create_opposite_filter_function(inner_self, target):
		return {'user': inner_self.instance, 'comment': target, 'type': opposite_type}

	def create_delete_filter_function(inner_self, target):
		return {'user': inner_self.instance, 'comment': target, 'type': vote_type}

	update_votes_relations(
		self=self,
		relation_model=CommentRelationship,
		source_model_reference_field=target_attribute,
		source_model_opposite_reference_field=opposite_attribute,
		create_filter=create_filter_function,
		create_opposite_filter=create_opposite_filter_function,
		create_delete_filter=create_delete_filter_function
	)


def update_request_vote_relations(self, target_attribute, opposite_attribute, vote_type, opposite_type):
	def create_filter_function(inner_self, target):
		return {'user': inner_self.instance, 'request': target, 'type': vote_type}

	def create_opposite_filter_function(inner_self, target):
		return {'user': inner_self.instance, 'request': target, 'type': opposite_type}

	def create_delete_filter_function(inner_self, target):
		return {'user': inner_self.instance, 'request': target, 'type': vote_type}

	update_votes_relations(
		self=self,
		relation_model=RequestRelationship,
		source_model_reference_field=target_attribute,
		source_model_opposite_reference_field=opposite_attribute,
		create_filter=create_filter_function,
		create_opposite_filter=create_opposite_filter_function,
		create_delete_filter=create_delete_filter_function
	)


def update_scenery_vote_relations(self, target_attribute, opposite_attribute, vote_type, opposite_type):
	def create_filter_function(inner_self, target):
		return {'user': inner_self.instance, 'scenery': target, 'type': vote_type}

	def create_opposite_filter_function(inner_self, target):
		return {'user': inner_self.instance, 'scenery': target, 'type': opposite_type}

	def create_delete_filter_function(inner_self, target):
		return {'user': inner_self.instance, 'scenery': target, 'type': vote_type}

	update_votes_relations(
		self=self,
		relation_model=SceneryRelationship,
		source_model_reference_field=target_attribute,
		source_model_opposite_reference_field=opposite_attribute,
		create_filter=create_filter_function,
		create_opposite_filter=create_opposite_filter_function,
		create_delete_filter=create_delete_filter_function
	)

'''
	relation_model = e.g. BadgeOwnership, SceneryRelationship, etc. 
	source_model_reference_field = the field in the source Model (e.g. an attribute in the User Model), which is the other
																	foreign key of the ManyToMany Relation. (e.g. 'bronze_badges', 'silver_badges', 'gold_badges',
																	'upvoted_sceneries', 'downvoted_sceneries', ...
	create_filter(self, target) = a function returning a dictionary consisting of key-value pairs to determine the filters for the default
									create and delete functions. e.g. returning {user=self.instance, scenery=target, type=relation_type}
	create_opposite_filter(self, target) to create a filter for the opposite votes
									e.g. {	user=self.instance,
													scenery=target,
													type=opposite_type	}
	create_delete_filter(self, target): e.g. 	return {
																'user': self.instance,
																'scenery': target
															}
'''
def update_votes_relations(
	self,
	relation_model,
	source_model_reference_field,
	source_model_opposite_reference_field,
	create_filter,
	create_opposite_filter,
	create_delete_filter=None
):
	# find opposite vote and delete if exists
	def create_function(inner_self, target):
		relation_model.objects.create(**create_filter(inner_self=inner_self, target=target))
		opposite_intermediate = relation_model.objects.filter(**create_opposite_filter(inner_self=inner_self, target=target))
		if len(opposite_intermediate) == 1:
			opposite_intermediate.delete()
		getattr(inner_self.instance, source_model_opposite_reference_field).remove(target) # FIXME: TODO: this won't be saved?! don't know why, it works, but the next reload and this change is not remembered...

	update_relationships(
		self=self,
		relation_model=relation_model,
		source_model_reference_field=source_model_reference_field,
		create_function=create_function,
		delete_filter=create_delete_filter
	)

'''
	relation_model = e.g. BadgeOwnership, SceneryRelationship, etc.
	source_model_reference_field = the field in the source Model (e.g. an attribute in the User Model), which is the other
																	foreign key of the ManyToMany Relation. (e.g. 'bronze_badges', 'silver_badges', 'gold_badges',
																	'upvoted_sceneries', 'downvoted_sceneries', ...
	filter = a function returning a dictionary consisting of key-value pairs to determine the filters for the default
						create and delete functions.
						(e.g. def create_filter(target))
	functions = functions to provide custom create and/or delete methods.
	If a function is given, the corresponding filter is not needed and vice versa.		
'''
def update_relationships(
	self,
	relation_model,
	source_model_reference_field,
	create_filter=None,
	delete_filter=None,
	create_function=None,
	delete_function=None
):
	if create_filter is None and create_function is None:
		raise ValueError(_('Either one of create_filter or create_function needs to be set!'))
	if delete_filter is None and delete_function is None:
		raise ValueError(_('Either one of delete_filter or delete_function needs to be set!'))

	if source_model_reference_field in self.changed_data:
		final_relations = self.cleaned_data[source_model_reference_field].all()
		if source_model_reference_field in self.initial:
			initial_relations = self.initial[source_model_reference_field]
		else:
			initial_relations = []

		for target in final_relations:
			if target not in initial_relations:
				if create_function is None and create_filter is not None:
					relation_model.objects.create(**create_filter(inner_self=self, target=target))
					# relation_model.objects.create(user=self.instance, scenery=target, type=relation_type)
				elif create_function is not None:
					create_function(inner_self=self, target=target)

		# Neutralize
		if delete_function is not None or delete_filter is not None:
			for target in initial_relations:
				if target not in final_relations:
					if delete_function is None and delete_filter is not None:
						deleted_by_admin = relation_model.objects.filter(**delete_filter(inner_self=self, target=target))
						# deleted_by_admin = relation_model.objects.filter(user=self.instance, scenery=target)
						if len(deleted_by_admin) == 1:
							deleted_by_admin.delete()
					elif delete_function is not None:
						delete_function(inner_self=self, target=target)

