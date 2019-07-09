from rest_framework import permissions
from django.contrib.auth import get_user_model


class IsOwnerOrReadOnly(permissions.BasePermission):
	"""
		Custom permission to only allow owners of an object to edit it.
	"""

	def has_object_permission(self, request, view, obj):
		# Read permissions are allowed to any request,
		# so we'll always allow GET, HEAD or OPTIONS requests.
		if request.method in permissions.SAFE_METHODS:
			return True

		# Write permissions are only allowed to the owner of the snippet.
		return obj.author == request.user


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		return obj.author == request.user or request.user.is_admin


class IsOwnerOrAdminOrStaffOrReadOnly(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		if hasattr(obj, 'author'):
			return obj.author == request.user or request.user.is_admin or request.user.is_staff
		elif isinstance(obj, get_user_model()):
			return obj.id == request.user.id or request.user.is_admin or request.user.is_staff
		return False


class IsUnauthenticatedOrAdminOrStaff(permissions.BasePermission):
	def has_permission(self, request, view):
		if request.method in permissions.SAFE_METHODS:
			return True
		return not request.user.is_authenticated or request.user.is_authenticated and \
					 (request.user.is_admin or request.user.is_staff)
