from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class Admin(BaseUserAdmin):
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
	]
	list_filter = ('is_admin', )
	fieldsets = (
		(None, {'fields': ('id', 'email', 'username', 'password')}),
		('Permissions', {'fields': ('is_admin', 'is_superuser', 'is_staff')}),
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

	def get_queryset(self, request):
		queryset = super(Admin, self).get_queryset(request)
		#  queryset = queryset.annotate(models.Count('followers'))  TODO add things to be annotated
		return queryset


admin.site.register(get_user_model(), Admin)
