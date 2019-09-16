from django.contrib import admin
from .models import Document, DocumentationTag, DocumentationImage, DocumentationFile
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.
class DocumentAdmin(admin.ModelAdmin):
	model = Document
	readonly_fields = ('id', 'visit_count')
	list_display = [
		'id',
		'date_created',
		'author_link',
		'title',
		'description',
		'visit_count',
		'privacy_setting'
	]
	search_fields = (
	'id', 'date_created', 'author_link', 'title', 'visit_count', 'download_count', 'author__id', 'author__username',
	'author__email')
	list_filter = ('privacy_setting',)

	def author_link(self, obj):
		return format_html('<a href="{}">{}</a>', reverse(
			'admin:accounts_user_change', args=[obj.author.id]), obj.author.email)
	author_link.short_description = "Author"


class DocumentTagAdmin(admin.ModelAdmin):
	model = DocumentationTag
	readonly_fields = ('id',)
	list_display = ['id', 'date_created', 'user_link', 'tag']
	search_fields = ('id', 'date_created', 'author__email', 'author__username', 'tag')

	def user_link(self, obj):
		return format_html('<a href="{}">{}</a>', reverse(
			'admin:accounts_user_change', args=[obj.author.id]), obj.author.email)
	user_link.short_description = "Author"


class DocumenationImageAdmin(admin.ModelAdmin):
	model = DocumentationImage
	readonly_fields = ('id',)
	list_display = ['id', 'date_created', 'author_link', 'document_link']
	search_fields = ('id', 'date_created', 'author__email', 'author__username', 'document__title', 'document__id')

	def author_link(self, obj):
		return format_html('<a href="{}">{}</a>', reverse(
			'admin:accounts_user_change', args=[obj.author.id]), obj.author.email)
	author_link.short_description = "Author"

	def document_link(self, obj):
		return format_html('<a href="{}">{}</a>', reverse(
			'admin:documentation_document_change', args=[obj.document.id]), obj.document.title)
	document_link.short_description = "Scenery"

class DocumenationFileAdmin(admin.ModelAdmin):
	model = DocumentationFile
	readonly_fields = ('id',)
	list_display = ['id', 'date_created', 'user_link', 'documentation_link']
	search_fields = ('id', 'date_created', 'author__email', 'author__username', 'document__id', 'document__title')

	def user_link(self, obj):
		return format_html('<a href="{}">{}</a>', reverse(
			'admin:accounts_user_change', args=[obj.author.id]), obj.author.email)
	user_link.short_description = "Author"

	def documentation_link(self, obj):
		return format_html('<a href="{}">{}</a>', reverse(
			'admin:documentation_document_change', args=[obj.document.id]), obj.document.title)
	documentation_link.short_description = "Document"


admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentationTag, DocumentTagAdmin)
admin.site.register(DocumentationImage, DocumenationImageAdmin)
admin.site.register(DocumentationFile, DocumenationFileAdmin)
