from .models import Request
from .serializers import RequestSerializer
from rest_framework import generics
from rest_framework import permissions
from accounts.permissions import IsOwnerOrAdminOrStaffOrReadOnly, IsOwnerOrReadOnly
from odpr_shared_models.views import NestedRetrieveUpdateDestroyAPIView, NestedCreateAPIView

def get_request_by_id(pk):
	return Request.objects.get(pk=pk)

def get_request_serializer_permission_type(self):
	if self.request.user.is_authenticated and self.request.user.is_admin:
		return RequestSerializer.ADMIN
	elif self.request.user.is_authenticated and self.request.user.is_staff:
		return RequestSerializer.STAFF
	elif self.request.user.is_authenticated and \
		'kwargs' in self.request.parser_context and \
		'id' in self.request.parser_context['kwargs'] and \
		get_request_by_id(self.request.parser_context['kwargs']['id']).author.pk == self.request.user.id:
		return RequestSerializer.AUTHOR
	elif self.request.user.is_authenticated:
		return RequestSerializer.VIEWER
	else:
		return RequestSerializer.GUEST


class RequestCreateView(NestedCreateAPIView):
	queryset = Request.objects.all()
	serializer_class = RequestSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)

	def get_serializer(self, *args, **kwargs):
		serializer_class = self.get_serializer_class()
		kwargs['context'] = self.get_serializer_context()
		return serializer_class(permission_type=get_request_serializer_permission_type(self), *args, **kwargs)


class RequestListView(generics.ListAPIView):
	queryset = Request.objects.all()
	serializer_class = RequestSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
												IsOwnerOrReadOnly,)

	def get_serializer(self, *args, **kwargs):
		serializer_class = self.get_serializer_class()
		kwargs['context'] = self.get_serializer_context()
		return serializer_class(permission_type=get_request_serializer_permission_type(self), *args, **kwargs)


class RequestDetailView(NestedRetrieveUpdateDestroyAPIView):
	queryset = Request.objects.all()
	serializer_class = RequestSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
												IsOwnerOrAdminOrStaffOrReadOnly,)
	lookup_field = 'id'

	def get_serializer(self, *args, **kwargs):
		serializer_class = self.get_serializer_class()
		kwargs['context'] = self.get_serializer_context()
		return serializer_class(permission_type=get_request_serializer_permission_type(self), *args, **kwargs)
