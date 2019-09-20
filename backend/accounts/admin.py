from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db import models
from django.db.models import Q
from .models import User
from .forms import UserChangeForm, UserCreationForm
from odpr_shared_models.models import Report, ProfileImage, Notification
from django.urls import reverse
from django.utils.html import format_html


class Admin(BaseUserAdmin):
	add_form = UserCreationForm
	form = UserChangeForm
	model = get_user_model()
	readonly_fields = ('id',)
	# The fields to be used in displaying the User model.
	# These override the definitions on the base UserAdmin
	# that reference specific fields on auth.User.
	list_display = [
		'email',
		'id',
		'username',
		'is_admin',
		'points',
		'get_following_count',
		'get_followers_count',
		#	'get_friends_count',
		'get_blocked_count',
		'get_blocking_count',
		'get_badge_count',
		'get_gold_badge_count',
		'get_silver_badge_count',
		'get_bronze_badge_count',
		'get_reports_count',
		'get_reported_users_count',
		'get_reported_sceneries_count',
		'get_reported_requests_count',
		'get_reported_comments_count',
		'get_reported_by_count',
		'get_upvoted_sceneries_count',
		'get_downvoted_sceneries_count',
		'get_starred_sceneries_count',
		'get_visited_sceneries_count',
		'get_created_sceneries_count',
		'get_downloaded_sceneries_count',
		'get_upvoted_requests_count',
		'get_downvoted_requests_count',
		'get_starred_requests_count',
		'get_visited_requests_count',
		'get_created_requests_count',
		'get_created_comments_count',
		'get_upvoted_comments_count',
		'get_downvoted_comments_count',
		'get_upvoted_answers_count',
		'get_downvoted_answers_count',
		'get_created_answers_count',
	]
	list_filter = ('is_admin', )
	fieldsets = (
		(None, {'fields': ('id', 'email', 'password')}),
		('Personal info', {'fields': ('username', 'points', 'bio')}),
		('Badges', {'fields': ('bronze_badges', 'silver_badges', 'gold_badges')}),
		# ('Badges', {'fields': ('badges',)}),
		('Permissions', {'fields': ('is_admin', 'is_superuser', 'is_staff')}),
		('Following / Followers', {'fields': ('following', 'followers')}),
		# ('Friends', {'fields': ('friends',)}),
		('Blocking', {'fields': ('blocked', 'blocked_by')}),
		('Sceneries', {'fields': (
			'upvoted_sceneries',
			'downvoted_sceneries',
			'starred_sceneries',
			'visited_sceneries',
			'downloaded_sceneries'
		)}),
		('Requests', {'fields': (
			'upvoted_requests',
			'downvoted_requests',
			'starred_requests',
			'visited_requests',
		)}),
		('Comments', {'fields': ('upvoted_comments', 'downvoted_comments')}),
		('Answers', {'fields': ('upvoted_answers', 'downvoted_answers')})
	)
	# add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
	# overrides get_fieldsets to use this attribute when creating a user.
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'username', 'password1', 'password2')
		}),
	)
	search_fields = ('id', 'email', 'username')
	ordering = ('id', 'email', 'username')
	# filter_horizontal = ('following', 'followers')

	def get_queryset(self, request):
		queryset = super(Admin, self).get_queryset(request)
		queryset = queryset.annotate(models.Count('followers'))
		queryset = queryset.annotate(models.Count('following'))
		# queryset = queryset.annotate(models.Count('friends')) # TODO: frozen feature.
		queryset = queryset.annotate(models.Count('blocked'))
		queryset = queryset.annotate(models.Count('blocked_by'))
		queryset = queryset.annotate(gold_badges__count=models.Count('gold_badges'))
		queryset = queryset.annotate(silver_badges__count=models.Count('silver_badges'))
		queryset = queryset.annotate(bronze_badges__count=models.Count('bronze_badges'))
		queryset = queryset.annotate(badge__count=models.Count('gold_badges')+models.Count('silver_badges')+models.Count('bronze_badges'))
		queryset = queryset.annotate(reported_users__count=models.Count('reports', filter=Q(reports__type=Report.USER)))
		queryset = queryset.annotate(reported_sceneries__count=models.Count('reports', filter=Q(reports__type=Report.SCENERY)))
		queryset = queryset.annotate(reported_requests__count=models.Count('reports', filter=Q(reports__type=Report.REQUEST)))
		queryset = queryset.annotate(reported_comments__count=models.Count('reports', filter=Q(reports__type=Report.COMMENT)))
		queryset = queryset.annotate(reports__count=models.Count('reports'))
		# queryset = queryset.annotate(reported_by__count=models.Count('report', filter=Q(type='user'))) # TODO: filter by user pk
		queryset = queryset.annotate(models.Count('upvoted_sceneries'))
		queryset = queryset.annotate(models.Count('downvoted_sceneries'))
		queryset = queryset.annotate(models.Count('starred_sceneries'))
		queryset = queryset.annotate(models.Count('visited_sceneries'))
		queryset = queryset.annotate(models.Count('downloaded_sceneries'))
		queryset = queryset.annotate(models.Count('upvoted_requests'))
		queryset = queryset.annotate(models.Count('downvoted_requests'))
		queryset = queryset.annotate(models.Count('starred_requests'))
		queryset = queryset.annotate(models.Count('visited_requests'))
		queryset = queryset.annotate(models.Count('upvoted_comments'))
		queryset = queryset.annotate(models.Count('downvoted_comments'))
		queryset = queryset.annotate(models.Count('upvoted_answers'))
		queryset = queryset.annotate(models.Count('downvoted_answers'))
		return queryset


class UserProfileImageAdmin(admin.ModelAdmin):
	model = ProfileImage
	readonly_fields = ('id',)
	list_display = ['id', 'date_created', 'author_link', 'user_link']
	search_fields = ('id', 'date_created', 'author__email', 'author__username', 'user__email', 'user__username')

	def author_link(self, obj):
		return format_html('<a href="{}">{}</a>', reverse(
			'admin:accounts_user_change', args=[obj.author.id]), obj.author.email)
	author_link.short_description = "Author"

	def user_link(self, obj):
		return format_html('<a href="{}">{}</a>', reverse(
			'admin:accounts_user_change', args=[obj.user.id]), obj.user.email)
	user_link.short_description = "User"


class NotificationAdmin(admin.ModelAdmin):
	model = Notification
	readonly_fields = ('id',)
	list_display = ['id', 'content', 'user_link']
	search_fields = ('id', 'content', 'user__email', 'user__username')

	def user_link(self, obj):
		return format_html('<a href="{}">{}</a>', reverse(
			'admin:accounts_user_change', args=[obj.user.id]), obj.user.email)
	user_link.short_description = "User"

# Now register the new UserAdmin...
admin.site.register(get_user_model(), Admin)
admin.site.register(ProfileImage, UserProfileImageAdmin)
admin.site.register(Notification, NotificationAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
