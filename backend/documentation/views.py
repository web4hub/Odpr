from .models import Document
from .serializers import DocumentSerializer
from rest_framework import generics
from rest_framework import permissions
from accounts.permissions import IsOwnerOrAdminOrStaffOrReadOnly, IsOwnerOrReadOnly
from odpr_shared_models.views import NestedRetrieveUpdateDestroyAPIView, NestedCreateAPIView

def get_document_by_id(pk):
	return Document.objects.get(pk=pk)

def get_document_serializer_permission_type(self):
	if self.request.user.is_authenticated and self.request.user.is_admin:
		return DocumentSerializer.ADMIN
	elif self.request.user.is_authenticated and self.request.user.is_staff:
		return DocumentSerializer.STAFF
	elif self.request.user.is_authenticated and \
		'kwargs' in self.request.parser_context and \
		'id' in self.request.parser_context['kwargs'] and \
		get_document_by_id(self.request.parser_context['kwargs']['id']).author.pk == self.request.user.id:
		return DocumentSerializer.AUTHOR
	elif self.request.user.is_authenticated:
		return DocumentSerializer.VIEWER
	else:
		return DocumentSerializer.GUEST


class DocumentCreateView(NestedCreateAPIView):
	queryset = Document.objects.all()
	serializer_class = DocumentSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)

	def get_serializer(self, *args, **kwargs):
		serializer_class = self.get_serializer_class()
		kwargs['context'] = self.get_serializer_context()
		return serializer_class(permission_type=get_document_serializer_permission_type(self), *args, **kwargs)


class DocumentListView(generics.ListAPIView):
	queryset = Document.objects.all()
	serializer_class = DocumentSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
												IsOwnerOrReadOnly,)

	def get_serializer(self, *args, **kwargs):
		serializer_class = self.get_serializer_class()
		kwargs['context'] = self.get_serializer_context()
		return serializer_class(permission_type=get_document_serializer_permission_type(self), *args, **kwargs)


class DocumentDetailView(NestedRetrieveUpdateDestroyAPIView):
	queryset = Document.objects.all()
	serializer_class = DocumentSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
												IsOwnerOrAdminOrStaffOrReadOnly,)
	lookup_field = 'id'

	def get_serializer(self, *args, **kwargs):
		serializer_class = self.get_serializer_class()
		kwargs['context'] = self.get_serializer_context()
		return serializer_class(permission_type=get_document_serializer_permission_type(self), *args, **kwargs)
