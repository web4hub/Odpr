from django.contrib import admin
from .models import Request, RequestRelationship, Answer, AnswerRelationship, RequestImage, RequestFile, RequestTagRelationship
from django.urls import reverse
from django.utils.html import format_html
from .forms import RequestChangeForm


class RequestAdmin(admin.ModelAdmin):
	model = Request
	form = RequestChangeForm
	readonly_fields = ('id', 'visit_count')
	list_display = [
		'id',
		'date_created',
		'author_link',
		'title',
		'visit_count',
		'get_final_vote_number',
		'get_upvote_count',
		'get_downvote_count',
		'get_starred_count',
		'get_reported_count',
		'privacy_setting',
		'is_closed'
	]
	search_fields = (
		'id', 'date_created', 'author_link', 'title', 'visit_count', 'author__id', 'author__username',
		'author__email'
	)
	list_filter = ('privacy_setting', 'is_closed', 'tags')

	def author_link(self, obj):
		return format_html('<a href="{}">{}</a>', reverse(
			'admin:accounts_user_change', args=[obj.author.id]), obj.author.email)
	author_link.short_description = "Author"


class RequestRelationshipAdmin(admin.ModelAdmin):
	model = RequestRelationship
	readonly_fields = ('id',)
	list_display = ['id', 'date_created', 'user', 'request', 'type']
	search_fields = ('id', 'date_created', 'user__email', 'user__username', 'user__id', 'request__id', 'request__title', 'type')
	list_filter = ('type',)


class RequestTagRelationshipAdmin(admin.ModelAdmin):
	model = RequestTagRelationship
	readonly_fields = ('id',)
	list_display = ['id', 'date_created', 'tag', 'request']
	search_fields = ('id', 'date_created', 'tag__tag', 'tag__author__id', 'tag__author__email', 'tag__author__username',
									 'request__id', 'request__title')


class AnswerAdmin(admin.ModelAdmin):
	model = Answer
	readonly_fields = ('id',)
	list_display = ['id', 'content', 'user_link', 'referenced_link', 'marked_as_accepted']
	search_fields = ('id', 'author__email', 'author__username', 'content')
	list_filter = ('marked_as_accepted', )

	def user_link(self, obj):
		return format_html('<a href="{}">{}</a>', reverse(
			'admin:accounts_user_change', args=[obj.author.id]), obj.author.email)
	user_link.short_description = "Author"

	def referenced_link(self, obj):
		return format_html('<a href="{}">{}</a>', reverse('admin:scenery_requests_request_change', args=[obj.parent_id.id]),
												 obj.parent_id)
	referenced_link.short_description = "Reference"


class AnswerRelationshipAdmin(admin.ModelAdmin):
	model = AnswerRelationship
	readonly_fields = ('id',)
	list_display = ['id', 'date_created', 'user', 'answer', 'type']
	search_fields = ('id', 'date_created', 'user__email', 'user__username', 'user__id', 'answer__id', 'type')
	list_filter = ('type',)


class RequestFileAdmin(admin.ModelAdmin):
	model = RequestFile
	readonly_fields = ('id',)
	list_display = ['id', 'date_created', 'user_link', 'request_link']
	search_fields = ('id', 'date_created', 'author__email', 'author__username', 'request__id', 'request__title')

	def user_link(self, obj):
		return format_html('<a href="{}">{}</a>', reverse(
			'admin:accounts_user_change', args=[obj.author.id]), obj.author.email)
	user_link.short_description = "Author"

	def request_link(self, obj):
		return format_html('<a href="{}">{}</a>', reverse(
			'admin:scenery_requests_request_change', args=[obj.request.id]), obj.request.title)
	request_link.short_description = "Request"


class RequestImageAdmin(admin.ModelAdmin):
	model = RequestImage
	readonly_fields = ('id',)
	list_display = ['id', 'date_created', 'author_link', 'request_link']
	search_fields = ('id', 'date_created', 'author__email', 'author__username', 'request__title', 'request__id')

	def author_link(self, obj):
		return format_html('<a href="{}">{}</a>', reverse(
			'admin:accounts_user_change', args=[obj.author.id]), obj.author.email)
	author_link.short_description = "Author"

	def request_link(self, obj):
		return format_html('<a href="{}">{}</a>', reverse(
			'admin:scenery_requests_request_change', args=[obj.request.id]), obj.request.title)
	request_link.short_description = "Request"


admin.site.register(Request, RequestAdmin)
admin.site.register(RequestRelationship, RequestRelationshipAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(AnswerRelationship, AnswerRelationshipAdmin)
admin.site.register(RequestImage, RequestImageAdmin)
admin.site.register(RequestFile, RequestFileAdmin)
admin.site.register(RequestTagRelationship, RequestTagRelationshipAdmin)
