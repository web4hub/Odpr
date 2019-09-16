from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django.db import models
from .models import User
from odpr_shared_models.models import Badge, BadgeOwnership, Comment, CommentRelationship
from scenery_requests.models import Answer, AnswerRelationship
from .form_helpers import general_model_multiple_choice_field,\
	general_model_multiple_choice_field_filter_type,\
	general_queryset_multiple_choice_field_filter_type, \
	update_scenery_vote_relations, \
	update_relationships, \
	update_request_vote_relations, \
	update_comment_vote_relations, \
	update_answer_vote_relations
from django.db.models.signals import post_save
from django.dispatch import receiver
from sceneries.models import Scenery, SceneryRelationship
from scenery_requests.models import Request, RequestRelationship


class UserCreationForm(forms.ModelForm):
	"""A form for creating new users. Includes all the required
	fields, plus a repeated password."""
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = get_user_model()
		fields = ('email', 'username')

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super().save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user


class UserChangeForm(forms.ModelForm):
	"""A form for updating users. Includes all the fields on
	the user, but replaces the password field with admin's
	password hash display field.

	Provides lots of additional functions for admin-site changes on manytomany fields
	(to create and delete association models)
	"""
	password = ReadOnlyPasswordHashField()
	following = general_model_multiple_choice_field(model=get_user_model(), verbose_name='Following')
	followers = general_model_multiple_choice_field(model=get_user_model(), verbose_name='Followers')
	# friends = models.CharField(max_length=30, default='Not implemented')
	# friends = forms.CharField(max_length=30, empty_value='Not implemented')
	blocked = general_model_multiple_choice_field(model=get_user_model(), verbose_name='Blocked')
	blocked_by = general_model_multiple_choice_field(model=get_user_model(), verbose_name='Blocked by')
	bronze_badges = general_model_multiple_choice_field(model=Badge, verbose_name='Bronze Badges')
	silver_badges = general_model_multiple_choice_field(model=Badge, verbose_name='Silver Badges')
	gold_badges = general_model_multiple_choice_field(model=Badge, verbose_name='Gold Badges')
	upvoted_sceneries = general_model_multiple_choice_field(model=Scenery, verbose_name='Upvoted Sceneries')
	downvoted_sceneries = general_model_multiple_choice_field(model=Scenery, verbose_name='Downvoted Sceneries')
	starred_sceneries = general_model_multiple_choice_field(model=Scenery, verbose_name='Starred Sceneries')
	visited_sceneries = general_model_multiple_choice_field(model=Scenery, verbose_name='Viewed Sceneries')
	downloaded_sceneries = general_model_multiple_choice_field(model=Scenery, verbose_name='Downloaded Sceneries')
	upvoted_requests = general_model_multiple_choice_field(model=Request, verbose_name='Upvoted Requests')
	downvoted_requests = general_model_multiple_choice_field(model=Request, verbose_name='Downvoted Requests')
	starred_requests = general_model_multiple_choice_field(model=Request, verbose_name='Starred Requests')
	visited_requests = general_model_multiple_choice_field(model=Request, verbose_name='Viewed Requests')
	upvoted_comments = general_model_multiple_choice_field(model=Comment, verbose_name='Upvoted Comments')
	downvoted_comments = general_model_multiple_choice_field(model=Comment, verbose_name='Downvoted Comments')
	upvoted_answers = general_model_multiple_choice_field(model=Answer, verbose_name='Upvoted Answers')
	downvoted_answers = general_model_multiple_choice_field(model=Answer, verbose_name='Downvoted Answers')

	class Meta:
		model = get_user_model()
		fields = (
			'email',
			'password',
			'username',
			'is_active',
			'is_admin',
			'following',
			'followers',
			# 'friends',
			'blocked',
			'blocked_by',
			'bronze_badges',
			'silver_badges',
			'gold_badges',
			'upvoted_sceneries',
			'downvoted_sceneries',
			'starred_sceneries',
			'visited_sceneries',
			'downloaded_sceneries',
			'upvoted_requests',
			'downvoted_requests',
			'starred_requests',
			'visited_requests',
			'upvoted_comments',
			'downvoted_comments',
			'upvoted_answers',
			'downvoted_answers'
		)
		#'badges')

	def __init__(self, *args, **kwargs):
		super(UserChangeForm, self).__init__(*args, **kwargs)

		if self.instance and self.instance.pk:
			self.fields['following'] = general_model_multiple_choice_field(get_user_model(), 'Following', self.instance.pk)
			self.fields['followers'] = general_model_multiple_choice_field(get_user_model(), 'Followers', self.instance.pk)
			self.fields['followers'].initial = self.instance.followers.all()
			# self.fields['friends'].initial = 'Not implemented'
			self.fields['blocked'] = general_model_multiple_choice_field(get_user_model(), 'Blocked', self.instance.pk)
			self.fields['blocked_by'] = general_model_multiple_choice_field(get_user_model(), 'Blocked by', self.instance.pk)
			self.fields['bronze_badges'] = general_model_multiple_choice_field_filter_type(Badge,
																																				 'Bronze Badges',
																																				 filter_by_type=Badge.BRONZE)
			self.fields['silver_badges'] = general_model_multiple_choice_field_filter_type(Badge,
																																				 'Silver Badges',
																																				 filter_by_type=Badge.SILVER)
			self.fields['gold_badges'] = general_model_multiple_choice_field_filter_type(Badge,
																																			 'Gold Badges',
																																			 filter_by_type=Badge.GOLD)
			self.fields['upvoted_sceneries'] = general_model_multiple_choice_field(Scenery, 'Upvoted Sceneries',
																																						 self.instance.pk)
			self.fields['upvoted_sceneries'].initial = self.instance.upvoted_sceneries.all()
			# self.fields['upvoted_sceneries'].initial = self.instance.upvoted_sceneries.all()
			self.fields['downvoted_sceneries'] = general_model_multiple_choice_field(Scenery, 'Downvoted Sceneries',
																																							 self.instance.pk)
			self.fields['starred_sceneries'] = general_model_multiple_choice_field(Scenery, 'Starred Sceneries',
																																						 self.instance.pk)
			self.fields['visited_sceneries'] = general_model_multiple_choice_field(Scenery, 'Viewed Sceneries',
																																						 self.instance.pk)
			self.fields['downloaded_sceneries'] = general_model_multiple_choice_field(Scenery, 'Downloaded Sceneries',
																																								self.instance.pk)
			self.fields['upvoted_requests'] = general_model_multiple_choice_field(Request, 'Upvoted Requests',
																																						 self.instance.pk)
			self.fields['downvoted_requests'] = general_model_multiple_choice_field(Request, 'Downvoted Requests',
																																							 self.instance.pk)
			self.fields['starred_requests'] = general_model_multiple_choice_field(Request, 'Starred Requests',
																																						 self.instance.pk)
			self.fields['visited_requests'] = general_model_multiple_choice_field(Request, 'Viewed Requests',
																																						 self.instance.pk)
			self.fields['upvoted_comments'] = general_model_multiple_choice_field(Comment, 'Upvoted Comments',
																																						self.instance.pk)
			self.fields['downvoted_comments'] = general_model_multiple_choice_field(Comment, 'Downvoted Comments',
																																							self.instance.pk)
			self.fields['upvoted_answers'] = general_model_multiple_choice_field(Answer, 'Upvoted Answers',
																																						self.instance.pk)
			self.fields['downvoted_answers'] = general_model_multiple_choice_field(Answer, 'Downvoted Answers',
																																							self.instance.pk)

	def clean_password(self):
		# Regardless of what the user provides, return the initial value.
		# This is done here, rather than on the field, because the
		# field does not have access to the initial value
		return self.initial["password"]

	def save(self, commit=True):
		user = super().save(commit=False)
		#if commit:
		user.save()
		# self.create_badge_ownerships()
		self.update_badges_relationships()
		self.update_scenery_relations()
		self.update_request_relations()
		self.update_comment_relations()
		self.update_answer_relations()
		user.save()
		return user

	def update_badges_relationships(self):
		self.update_badge_relationships(badge_type='bronze_badges')
		self.update_badge_relationships(badge_type='silver_badges')
		self.update_badge_relationships(badge_type='gold_badges')

	def update_badge_relationships(self, badge_type):
		update_relationships(
			self=self,
			relation_model=BadgeOwnership,
			source_model_reference_field=badge_type,
			create_filter=lambda inner_self, target: {'owner': inner_self.instance, 'badge': target},
			delete_filter=lambda inner_self, target: {'owner': inner_self.instance, 'badge': target}
		)

	def update_comment_relations(self):
		self.update_comment_downvote_relations()
		self.update_comment_upvote_relations()

	def update_answer_relations(self):
		self.update_answer_upvote_relations()
		self.update_answer_downvote_relations()

	def update_request_relations(self):
		self.update_request_upvote_relations()
		self.update_request_downvote_relations()
		self.update_request_star_relations()
		self.update_request_visited_relations()

	def update_scenery_relations(self):
		self.update_scenery_upvote_relations()
		self.update_scenery_downvote_relations()
		self.update_scenery_star_relations()
		self.update_scenery_visited_relations()
		self.update_scenery_downloaded_relations()

	def update_scenery_downloaded_relations(self):
		update_relationships(
			self=self,
			relation_model=SceneryRelationship,
			source_model_reference_field='downloaded_sceneries',
			create_filter=lambda inner_self, target: {
				'user': inner_self.instance,
				'scenery': target,
				'type': SceneryRelationship.SCENERY_DOWNLOAD
			},
			delete_filter=lambda inner_self, target: {
				'user': inner_self.instance,
				'scenery': target,
				'type': SceneryRelationship.SCENERY_DOWNLOAD
			},
		)

	def update_scenery_visited_relations(self):
		update_relationships(
			self=self,
			relation_model=SceneryRelationship,
			source_model_reference_field='visited_sceneries',
			create_filter=lambda inner_self, target: {
				'user': inner_self.instance,
				'scenery': target,
				'type': SceneryRelationship.SCENERY_VISIT
			},
			delete_filter=lambda inner_self, target: {
				'user': inner_self.instance,
				'scenery': target,
				'type': SceneryRelationship.SCENERY_VISIT
			},
		)

	def update_scenery_star_relations(self):
		update_relationships(
			self=self,
			relation_model=SceneryRelationship,
			source_model_reference_field='starred_sceneries',
			create_filter=lambda inner_self, target: {
				'user': inner_self.instance,
				'scenery': target,
				'type': SceneryRelationship.SCENERY_STAR
			},
			delete_filter=lambda inner_self, target: {
				'user': inner_self.instance,
				'scenery': target,
				'type': SceneryRelationship.SCENERY_STAR
			},
		)

	def update_scenery_downvote_relations(self):
		update_scenery_vote_relations(
			self=self,
			target_attribute='downvoted_sceneries',
			opposite_attribute='upvoted_sceneries',
			vote_type=SceneryRelationship.SCENERY_DOWNVOTE,
			opposite_type=SceneryRelationship.SCENERY_UPVOTE
		)

	def update_scenery_upvote_relations(self):
		update_scenery_vote_relations(
			self=self,
			target_attribute='upvoted_sceneries',
			opposite_attribute='downvoted_sceneries',
			vote_type=SceneryRelationship.SCENERY_UPVOTE,
			opposite_type=SceneryRelationship.SCENERY_DOWNVOTE
		)

	def update_request_visited_relations(self):
		update_relationships(
			self=self,
			relation_model=RequestRelationship,
			source_model_reference_field='visited_requests',
			create_filter=lambda inner_self, target: {
				'user': inner_self.instance,
				'request': target,
				'type': RequestRelationship.REQUEST_VISIT
			},
			delete_filter=lambda inner_self, target: {
				'user': inner_self.instance,
				'request': target,
				'type': RequestRelationship.REQUEST_VISIT
			},
		)

	def update_request_star_relations(self):
		update_relationships(
			self=self,
			relation_model=RequestRelationship,
			source_model_reference_field='starred_requests',
			create_filter=lambda inner_self, target: {
				'user': inner_self.instance,
				'request': target,
				'type': RequestRelationship.REQUEST_STAR
			},
			delete_filter=lambda inner_self, target: {
				'user': inner_self.instance,
				'request': target,
				'type': RequestRelationship.REQUEST_STAR
			},
		)

	def update_request_downvote_relations(self):
		update_request_vote_relations(
			self=self,
			target_attribute='downvoted_requests',
			opposite_attribute='upvoted_requests',
			vote_type=RequestRelationship.REQUEST_DOWNVOTE,
			opposite_type=RequestRelationship.REQUEST_UPVOTE
		)

	def update_request_upvote_relations(self):
		update_request_vote_relations(
			self=self,
			target_attribute='upvoted_requests',
			opposite_attribute='downvoted_requests',
			vote_type=RequestRelationship.REQUEST_UPVOTE,
			opposite_type=RequestRelationship.REQUEST_DOWNVOTE
		)

	def update_comment_downvote_relations(self):
		update_comment_vote_relations(
			self=self,
			target_attribute='downvoted_comments',
			opposite_attribute='upvoted_comments',
			vote_type=CommentRelationship.COMMENT_DOWNVOTE,
			opposite_type=CommentRelationship.COMMENT_UPVOTE
		)

	def update_comment_upvote_relations(self):
		update_comment_vote_relations(
			self=self,
			target_attribute='upvoted_comments',
			opposite_attribute='downvoted_comments',
			vote_type=CommentRelationship.COMMENT_UPVOTE,
			opposite_type=CommentRelationship.COMMENT_DOWNVOTE
		)

	def update_answer_downvote_relations(self):
		update_answer_vote_relations(
			self=self,
			target_attribute='downvoted_answers',
			opposite_attribute='upvoted_answers',
			vote_type=AnswerRelationship.ANSWER_DOWNVOTE,
			opposite_type=AnswerRelationship.ANSWER_UPVOTE
		)

	def update_answer_upvote_relations(self):
		update_answer_vote_relations(
			self=self,
			target_attribute='upvoted_answers',
			opposite_attribute='downvoted_answers',
			vote_type=AnswerRelationship.ANSWER_UPVOTE,
			opposite_type=AnswerRelationship.ANSWER_DOWNVOTE
		)


class UserLoginForm(forms.ModelForm):
	username_or_email = forms.CharField(label='Username or E-Mail', widget=forms.TextInput)
	password = forms.CharField(label='Password', widget=forms.PasswordInput)

