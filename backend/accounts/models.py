import re
from django.db import models
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from odpr_shared_models.models import TextWithHistory, Badge, BadgeOwnership, Report, Comment, CommentRelationship
from scenery_requests.models import Answer, AnswerRelationship
from sceneries.models import Scenery
from scenery_requests.models import Request
from annoying.fields import AutoOneToOneField


# Create your models here.

class CustomUserManager(BaseUserManager):
	use_in_migrations = True

	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)
		user.set_password(password)
		user.user_type = User.USER
		user.save(using=self._db)
		return user

	def create_staffuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.staff = True
		user.is_staff = True
		user.user_type = User.STAFF
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.staff = True
		user.admin = True
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.user_type = User.ADMIN

		user.save(using=self._db)
		return user


class User(AbstractBaseUser, PermissionsMixin):
	class Meta:
		app_label = 'accounts'
		db_table = 'user'
		# ordering=["created"]

	username = models.CharField(_('username'), max_length=75, unique=True,
															help_text=_('Required. 30 characters or fewer. Letters, numbers and '
																					'@/./+/-/_ characters'),
															validators=[
																validators.RegexValidator(re.compile('^[\w.@+-]+$'),
																													_('Enter a valid username.'), 'invalid')
															])

	email = models.EmailField(_('email address'), max_length=254, unique=True)
	is_staff = models.BooleanField(_('staff status'), default=False,
																 help_text=_('Designates whether the user can log into this admin '
																						 'site.'))
	is_active = models.BooleanField(_('active'), default=True,
																	help_text=_('Designates whether this user should be treated as '
																							'active. Unselect this instead of deleting accounts.'))
	is_admin = models.BooleanField(_('admin status'), default=False,
																 help_text='Whether this account has access to all admin settings or not.')
	date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

	objects = CustomUserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	def get_full_name(self):
		return self.username

	def get_short_name(self):
		return self.username

	def __unicode__(self):
		return self.email

	def __str__(self):
		return self.email

	ADMIN, STAFF, MOD, USER, GUEST = range(0, 5)
	UserTypes = (
		(ADMIN, 'Admin'),
		(STAFF, 'Staff'),
		(MOD, 'Moderator'),
		(USER, 'User'),
		(GUEST, 'Guest'),
	)
	user_type = models.IntegerField(choices=UserTypes, default=3)

	#################### Custom app-specific relationships (database scheme) ####################

	bio = AutoOneToOneField(TextWithHistory, on_delete=models.SET_NULL, null=True, blank=True)
	profile_image_id = models.IntegerField(default=1, verbose_name='Profile Image')
	points = models.IntegerField(default=0, verbose_name='Reputatuion', blank=False, auto_created=True,
															 help_text='Your social points which you will receive for upvoted posts and comments, and'
																				 ' lose for downvoted posts or comments.')

	bronze_badges = models.ManyToManyField(Badge, related_name='bronze_badge_owners', blank=True) #, through=BadgeOwnership, through_fields=('owner', 'badge'))
	silver_badges = models.ManyToManyField(Badge, related_name='silver_badge_owners', blank=True) #, through=BadgeOwnership)
	gold_badges = models.ManyToManyField(Badge, related_name='gold_badge_owners', blank=True) # , through=BadgeOwnership)
	following = models.ManyToManyField('self', related_name='followers', blank=True, symmetrical=False) # Reference to all users who THIS user is following
	friends = models.ManyToManyField('self', blank=True, symmetrical=True) # TODO too complicated to implement now: friends would need requests plus acceptance or denial. Just leaving this here for the db scheme.
	blocked = models.ManyToManyField('self', related_name='blocked_by', blank=True, symmetrical=False)
	# reports defined by owner/author in Report.
	# sceneries defined by owner/author in Scenery.
	# reported_anything is not a field, but a computed property
	# reported_by is also computed below.
	upvoted_sceneries = models.ManyToManyField(Scenery, related_name='scenery_upvoters', blank=True)
	downvoted_sceneries = models.ManyToManyField(Scenery, related_name='scenery_downvoters', blank=True)
	starred_sceneries = models.ManyToManyField(Scenery, related_name='scenery_starrers', blank=True)
	visited_sceneries = models.ManyToManyField(Scenery, related_name='scenery_visitors', blank=True)
	downloaded_sceneries = models.ManyToManyField(Scenery, related_name='scenery_downloaders', blank=True)

	upvoted_requests = models.ManyToManyField(Request, related_name='request_upvoters', blank=True)
	downvoted_requests = models.ManyToManyField(Request, related_name='request_downvoters', blank=True)
	starred_requests = models.ManyToManyField(Request, related_name='request_starrers', blank=True)
	visited_requests = models.ManyToManyField(Request, related_name='request_visitors', blank=True)

	# posted_comments defined by author in Comment
	# posted_answers defined by author in Answer
	upvoted_comments = models.ManyToManyField(Comment, related_name='comment_upvoters', blank=True)
	downvoted_comments = models.ManyToManyField(Comment, related_name='comment_downvoters', blank=True)

	upvoted_answers = models.ManyToManyField(Answer, related_name='answer_upvoters', blank=True)
	downvoted_answers = models.ManyToManyField(Answer, related_name='answer_downvoters', blank=True)


	#################### Custom getter methods ##################################################

	def get_created_answers_count(self):
		return self.get_created_answers().count()
	get_created_answers_count.short_description = 'Posted Answers'

	def get_created_answers(self):
		return Answer.objects.filter(author=self.pk)

	def get_created_comments_count(self):
		return self.get_created_comments().count()
	get_created_comments_count.short_description = 'Comments made'

	def get_created_comments(self):
		return Comment.objects.filter(author=self.pk)

	def get_created_sceneries_count(self):
		return self.get_created_sceneries().count()
	get_created_sceneries_count.short_description = 'Created Sceneries'

	def get_created_sceneries(self):
		return Scenery.objects.filter(author=self.pk)

	def get_created_requests_count(self):
		return self.get_created_requests().count()
	get_created_requests_count.short_description = 'Created Requests'

	def get_created_requests(self):
		return Request.objects.filter(author=self.pk)

	def get_created_reports_count(self):
		return self.get_created_reports().count()
	get_created_reports_count.short_description = 'Created Reports'

	def get_created_reports(self):
		return Report.objects.filter(author=self.pk)

	def get_upvoted_answers_count(self):
		return self.upvoted_answers.count()
	get_upvoted_answers_count.short_description = 'Upvoted Answers'
	get_upvoted_answers_count.admin_order_field = 'upvoted_answers__count'

	def get_downvoted_answers_count(self):
		return self.downvoted_answers.count()
	get_downvoted_answers_count.short_description = 'Downvoted Answers'
	get_downvoted_answers_count.admin_order_field = 'downvoted_answers__count'

	def get_upvoted_comments_count(self):
		return self.upvoted_comments.count()
	get_upvoted_comments_count.short_description = 'Upvoted Comments'
	get_upvoted_comments_count.admin_order_field = 'upvoted_comments__count'

	def get_downvoted_comments_count(self):
		return self.downvoted_comments.count()
	get_downvoted_comments_count.short_description = 'Downvoted Comments'
	get_downvoted_comments_count.admin_order_field = 'downvoted_comments__count'

	def get_upvoted_requests_count(self):
		return self.upvoted_requests.count()
	get_upvoted_requests_count.short_description = 'Upvoted Requests'
	get_upvoted_requests_count.admin_order_field = 'upvoted_requests__count'

	def get_downvoted_requests_count(self):
		return self.downvoted_requests.count()
	get_downvoted_requests_count.short_description = 'Downvoted Requests'
	get_downvoted_requests_count.admin_order_field = 'downvoted_requests__count'

	def get_starred_requests_count(self):
		return self.starred_requests.count()
	get_starred_requests_count.short_description = 'Starred Requests'
	get_starred_requests_count.admin_order_field = 'starred_requests__count'

	def get_visited_requests_count(self):
		return self.visited_requests.count()
	get_visited_requests_count.short_description = 'Viewed Requests'
	get_visited_requests_count.admin_order_field = 'visited_requests__count'

	def get_upvoted_sceneries_count(self):
		return self.upvoted_sceneries.count()
	get_upvoted_sceneries_count.short_description = 'Upvoted Sceneries'
	get_upvoted_sceneries_count.admin_order_field = 'upvoted_sceneries__count'

	def get_downvoted_sceneries_count(self):
		return self.downvoted_sceneries.count()
	get_downvoted_sceneries_count.short_description = 'Downvoted Sceneries'
	get_downvoted_sceneries_count.admin_order_field = 'downvoted_sceneries__count'

	def get_starred_sceneries_count(self):
		return self.starred_sceneries.count()
	get_starred_sceneries_count.short_description = 'Starred Sceneries'
	get_starred_sceneries_count.admin_order_field = 'starred_sceneries__count'

	def get_visited_sceneries_count(self):
		return self.visited_sceneries.count()
	get_visited_sceneries_count.short_description = 'Viewed Sceneries'
	get_visited_sceneries_count.admin_order_field = 'visited_sceneries__count'

	def get_downloaded_sceneries_count(self):
		return self.downloaded_sceneries.count()
	get_downloaded_sceneries_count.short_description = 'Downloaded Sceneries'
	get_downloaded_sceneries_count.admin_order_field = 'downloaded_sceneries__count'

	def get_following_count(self):
		return self.following.count()
	get_following_count.short_description = 'Following'
	get_following_count.admin_order_field = 'following__count'

	def get_followers_count(self):
		return self.followers.count()
	get_followers_count.short_description = 'Followers'
	get_followers_count.admin_order_field = 'followers__count'

	def get_friends_count(self):
		return self.friends.count()
	get_friends_count.short_description = 'Friends'
	get_friends_count.admin_order_field = 'friends__count'

	def get_blocked_count(self):
		return self.blocked.count()
	get_blocked_count.short_description = 'Blocking Users'
	get_blocked_count.admin_order_field = 'blocked__count'

	def get_blocking_count(self):
		return self.blocked_by.count()
	get_blocking_count.short_description = 'Blocked By'
	get_blocking_count.admin_order_field = 'blocked_by__count'

	def get_bronze_badge_count(self):
		return self.bronze_badges.count()
	get_bronze_badge_count.short_description = 'Bronze Badges'
	get_bronze_badge_count.admin_order_field = 'bronze_badges__count'

	def get_silver_badge_count(self):
		return self.silver_badges.count()
	get_silver_badge_count.short_description = 'Silver Badges'
	get_silver_badge_count.admin_order_field = 'silver_badges__count'

	def get_gold_badge_count(self):
		return self.gold_badges.count()
	get_gold_badge_count.short_description = 'Gold Badges'
	get_gold_badge_count.admin_order_field = 'gold_badges__count'

	def get_badge_count(self):
		return self.bronze_badges.count() + self.silver_badges.count() + self.gold_badges.count()
	get_badge_count.short_description = 'All Badges'
	get_badge_count.admin_order_field = 'badge__count'

	def get_reported_users_count(self):
		return self.reports.filter(type=Report.USER).count()
	get_reported_users_count.short_description = 'Reported Users'
	get_reported_users_count.admin_order_field = 'reported_users__count'

	def get_reported_sceneries_count(self):
		return self.reports.filter(type=Report.SCENERY).count()
	get_reported_sceneries_count.short_description = 'Reported Sceneries'
	get_reported_sceneries_count.admin_order_field = 'reported_sceneries__count'

	def get_reported_requests_count(self):
		return self.reports.filter(type=Report.REQUEST).count()
	get_reported_requests_count.short_description = 'Reported Requests'
	get_reported_requests_count.admin_order_field = 'reported_requests__count'

	def get_reported_comments_count(self):
		return self.reports.filter(type=Report.COMMENT).count()
	get_reported_comments_count.short_description = 'Reported Comments'
	get_reported_comments_count.admin_order_field = 'reported_comments__count'

	def get_reports_count(self):
		return self.reports.count()
	get_reports_count.short_description = 'Reports Made'
	get_reports_count.admin_order_field = 'reports__count'

	def get_reported_by_count(self):
		return Report.objects.filter(type=Report.USER, reference=self.pk).count()
	get_reported_by_count.short_description = 'Reportd by'
	# get_reported_by_count.admin_order_field = 'reported_by__count'
