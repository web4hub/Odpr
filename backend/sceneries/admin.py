from .models import Scenery, SceneryRelationship, SceneryImage, SceneryFile, SceneryTagRelationship
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .forms import SceneryChangeForm


class SceneryAdmin(admin.ModelAdmin):
	model = Scenery
	form = SceneryChangeForm
	readonly_fields = ('id', 'visit_count', 'download_count')
	list_display = [
		'id',
		'date_created',
		'author_link',
		'title',
		'visit_count',
		'download_count',
		'get_final_vote_number',
		'get_upvote_count',
		'get_downvote_count',
		'get_starred_count',
		'get_reported_count',
		'privacy_setting'
	]
	search_fields = ('id', 'date_created', 'author_link', 'title', 'visit_count', 'download_count', 'author__id', 'author__username', 'author__email')
	list_filter = ('privacy_setting', 'is_closed', 'tags')

	def author_link(self, obj):
		return format_html('<a href="{}">{}</a>', reverse(
			'admin:accounts_user_change', args=[obj.author.id]), obj.author.email)
	author_link.short_description = "Author"


class SceneryRelationshipAdmin(admin.ModelAdmin):
	model = SceneryRelationship
	readonly_fields = ('id',)
	list_display = ['id', 'date_created', 'user', 'scenery', 'type']
	search_fields = ('id', 'date_created', 'user__email', 'user__username', 'user__id', 'scenery__id', 'scenery__title', 'type')
	list_filter = ('type',)


class SceneryTagRelationshipAdmin(admin.ModelAdmin):
	model = SceneryTagRelationship
	readonly_fields = ('id',)
	list_display = ['id', 'date_created', 'tag', 'scenery']
	search_fields = ('id', 'date_created', 'tag__tag', 'tag__author__id', 'tag__author__email', 'tag__author__username',
									 'scenery__id', 'scenery__title')


class SceneryFileAdmin(admin.ModelAdmin):
	model = SceneryFile
	readonly_fields = ('id',)
	list_display = ['id', 'date_created', 'user_link', 'scenery_link']
	search_fields = ('id', 'date_created', 'author__email', 'author__username', 'scenery__id', 'scenery__title')

	def user_link(self, obj):
		return format_html('<a href="{}">{}</a>', reverse(
			'admin:accounts_user_change', args=[obj.author.id]), obj.author.email)
	user_link.short_description = "Author"

	def scenery_link(self, obj):
		return format_html('<a href="{}">{}</a>', reverse(
			'admin:sceneries_scenery_change', args=[obj.scenery.id]), obj.scenery.title)
	scenery_link.short_description = "Scenery"


class SceneryImageAdmin(admin.ModelAdmin):
	model = SceneryImage
	readonly_fields = ('id',)
	list_display = ['id', 'date_created', 'author_link', 'scenery_link']
	search_fields = ('id', 'date_created', 'author__email', 'author__username', 'scenery__title', 'scenery__id')

	def author_link(self, obj):
		return format_html('<a href="{}">{}</a>', reverse(
			'admin:accounts_user_change', args=[obj.author.id]), obj.author.email)
	author_link.short_description = "Author"

	def scenery_link(self, obj):
		return format_html('<a href="{}">{}</a>', reverse(
			'admin:sceneries_scenery_change', args=[obj.scenery.id]), obj.scenery.title)
	scenery_link.short_description = "Scenery"


admin.site.register(Scenery, SceneryAdmin)
admin.site.register(SceneryRelationship, SceneryRelationshipAdmin)
admin.site.register(SceneryImage, SceneryImageAdmin)
admin.site.register(SceneryFile, SceneryFileAdmin)
admin.site.register(SceneryTagRelationship, SceneryTagRelationshipAdmin)
