from simple_history.admin import SimpleHistoryAdmin
from django.contrib import admin
from .models import TextWithHistory, Badge, BadgeOwnership, Report, TextWithHistoryAuthor, Comment, CommentRelationship
from .models import FilterProperty, FilterProperties, Tag, BadgeRule, ReputationRule, Log
from scenery_requests.models import Answer, AnswerRelationship
from django.urls import reverse
from django.utils.html import format_html

class TextWithHistoryAdmin(SimpleHistoryAdmin):
	model = TextWithHistory
	readonly_fields = ('id',)


class TextWithHistoryAuthorAdmin(SimpleHistoryAdmin):
	model = TextWithHistoryAuthor
	readonly_fields = ('id',)
	list_display = ['id', 'author', 'content', 'type']
	search_fields = ('id', 'author', 'content', 'type')
	list_filter = ('type',)


class BadgeAdmin(admin.ModelAdmin):
	model = Badge
	readonly_fields = ('id',)
	list_display = ['id', 'title', 'description', 'type', 'get_owned_by_count']
	search_fields = ('id', 'type', 'title', 'description')
	list_filter = ('type',)

	def owned_by_reference(self):
		pass


class BadgeOwnershipAdmin(admin.ModelAdmin):
	model = BadgeOwnership
	readonly_fields = ('id', )
	list_display = ['id', 'date_received', 'badge_link', 'user_link', 'viewed']
	search_fields = ('id', 'owner__email', 'owner__username', 'badge__title', 'badge__id', 'badge__description')
	list_filter = ('viewed', 'badge__type', 'badge__id')

	def badge_link(self, obj):
		return format_html('<a href="{}">{}</a>', reverse(
			'admin:odpr_shared_models_badge_change', args=[obj.badge.id]), 'ID: ' + str(obj.badge.id) + '  Title: ' + str(obj.badge.title))
	badge_link.short_description = "Badge"

	def user_link(self, obj):
		return format_html('<a href="{}">{}</a>', reverse(
			'admin:accounts_user_change', args=[obj.owner.id]), obj.owner.email)
	user_link.short_description = "Owner"


class ReportAdmin(admin.ModelAdmin):
	model = Report
	readonly_fields = ('id',)
	list_display = ['id', 'title', 'description', 'user_link', 'referenced_link', 'type', 'resolved']
	search_fields = ('id', 'author__email', 'author__username', 'title', 'description', 'type')
	list_filter = ('type', 'resolved')

	def user_link(self, obj):
		return format_html('<a href="{}">{}</a>', reverse(
			'admin:accounts_user_change', args=[obj.author.id]), obj.author.email)
	user_link.short_description = "Author"

	def referenced_link(self, obj):
		if obj.type == Report.USER:
			return format_html('<a href="{}">{}</a>', reverse('admin:accounts_user_change', args=[obj.reference]), obj.reference)
		elif obj.type == Report.SCENERY:
			return format_html('<a href="{}">{}</a>', reverse('admin:sceneries_scenery_change', args=[obj.reference]), obj.reference)
		elif obj.type == Report.REQUEST:
			return format_html('<a href="{}">{}</a>', reverse('admin:scenery_requests_request_change', args=[obj.reference]), obj.reference)
		elif obj.type == Report.ANSWER:
			return format_html('<a href="{}">{}</a>', reverse('admin:scenery_requests_answer_change', args=[obj.reference]), obj.reference)
		elif obj.type == Report.COMMENT:
			# TODO: IN VIEWS, NOT HERE: first get type of parent (scenery or request), then load the parent with its id, then second parameter in url should be comment id.
			return format_html('<a href="{}">{}</a>', reverse('admin:odpr_shared_models_comment_change', args=[obj.reference]), obj.reference)
	referenced_link.short_description = "Reference"


class CommentAdmin(admin.ModelAdmin):
	model = Comment
	readonly_fields = ('id',)
	list_display = ['id', 'content', 'user_link', 'referenced_link', 'type']
	search_fields = ('id', 'author__email', 'author__username', 'content', 'type')
	list_filter = ('type', )

	def user_link(self, obj):
		return format_html('<a href="{}">{}</a>', reverse(
			'admin:accounts_user_change', args=[obj.author.id]), obj.author.email)
	user_link.short_description = "Author"

	def referenced_link(self, obj):
		if obj.type == Comment.SCENERY_COMMENT:
			return format_html('<a href="{}">{}</a>', reverse('admin:sceneries_scenery_change', args=[obj.parent_id]),
												 obj.parent_id)
		elif obj.type == Comment.REQUEST_COMMENT:
			return format_html('<a href="{}">{}</a>', reverse('admin:scenery_requests_request_change', args=[obj.parent_id]),
												 obj.parent_id)
		elif obj.type == Comment.REQUEST_ANSWER_COMMENT:
			return format_html('<a href="{}">{}</a>', reverse('admin:scenery_requests_request_change', args=[obj.parent_id]),
												 obj.parent_id) # TODO link to answer instead of request.
	referenced_link.short_description = "Reference"


class CommentRelationshipAdmin(admin.ModelAdmin):
	model = CommentRelationship
	readonly_fields = ('id',)
	list_display = ['id', 'date_created', 'user', 'comment', 'type']
	search_fields = ('id', 'date_created', 'user__email', 'user__username', 'user__id', 'comment__id', 'type')
	list_filter = ('type',)


class FilterPropertyAdmin(admin.ModelAdmin):
	model = FilterProperty
	readonly_fields = ('id',)
	list_display = ['id', 'name', 'user_link', 'description']
	search_fields = ('id', 'author__email', 'author__username', 'name', 'description')

	def user_link(self, obj):
		return format_html('<a href="{}">{}</a>', reverse(
			'admin:accounts_user_change', args=[obj.author.id]), obj.author.email)
	user_link.short_description = "Author"


class FilterPropertiesAdmin(admin.ModelAdmin):
	model = FilterProperties
	readonly_fields = ('id',)
	list_display = ['id', 'get_effects_count', 'get_materials_count', 'get_lights_count', 'scenery_complexity']
	search_fields = ('id', 'get_effects_count', 'get_materials_count', 'get_lights_count', 'scenery_complexity')
	list_filter = ('scenery_complexity', )


class TagAdmin(admin.ModelAdmin):
	model = Tag
	readonly_fields = ('id',)
	list_display = ['id', 'date_created', 'user_link', 'tag']
	search_fields = ('id', 'date_created', 'author__email', 'author__username', 'tag')

	def user_link(self, obj):
		return format_html('<a href="{}">{}</a>', reverse(
			'admin:accounts_user_change', args=[obj.author.id]), obj.author.email)
	user_link.short_description = "Author"


class BadgeRuleAdmin(admin.ModelAdmin):
	model = BadgeRule
	readonly_fields = ('id',)
	list_display = ['id', 'key', 'condition', 'signal_direction']
	search_fields = ('id', 'key', 'condition', 'signal_direction')


class ReputationRuleAdmin(admin.ModelAdmin):
	model = ReputationRule
	readonly_fields = ('id',)
	list_display = ['id', 'key', 'condition']
	search_fields = ('id', 'key', 'condition')


class LogAdmin(admin.ModelAdmin):
	model = Log
	readonly_fields = ('id', 'request_method', 'ip', 'request_body', 'date')
	list_display = ('id', 'request_method', 'ip', 'request_body', 'date')
	search_fields = ('id', 'request_method', 'ip', 'request_body', 'date')
	list_filter = ('request_method',)


admin.site.register(TextWithHistory, TextWithHistoryAdmin)
admin.site.register(Badge, BadgeAdmin)
admin.site.register(BadgeOwnership, BadgeOwnershipAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(TextWithHistoryAuthor, TextWithHistoryAuthorAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentRelationship, CommentRelationshipAdmin)
admin.site.register(FilterProperty, FilterPropertyAdmin)
admin.site.register(FilterProperties, FilterPropertiesAdmin)
admin.site.register(BadgeRule, BadgeRuleAdmin)
admin.site.register(ReputationRule, ReputationRuleAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Log, LogAdmin)
