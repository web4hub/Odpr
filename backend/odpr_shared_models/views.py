from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from .mixins import NestedRetrieveModelMixin, NestedUpdateModelMixin, NestedCreateModelMixin
from rest_framework.mixins import DestroyModelMixin
from .models import Report, Log
from .serializers import ReportSerializer
from rest_framework import permissions
from accounts.permissions import IsOwnerOrAdminOrStaffOrReadOnly
import json

class IPLogger(GenericAPIView):
	def dispatch(self, request, *args, **kwargs):
		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
		if x_forwarded_for:
			ip = x_forwarded_for.split(',')[0]
		else:
			ip = request.META.get('REMOTE_ADDR')
		body = ''
		if request.method != 'GET':
			try:
				body = json.dumps(request.body.decode('utf-8'))
			except UnicodeDecodeError:
				body = 'Probably files.'
		Log.objects.create(ip=ip, request_body=body, request_method=request.method)
		return super(IPLogger, self).dispatch(request, *args, **kwargs)

class NestedRetrieveUpdateDestroyAPIView(
	DestroyModelMixin,
	NestedRetrieveModelMixin,
	NestedUpdateModelMixin,
	IPLogger
):
	"""
	Concrete view for retrieving, updating or deleting a model instance.
	"""

	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def patch(self, request, *args, **kwargs):
		return self.partial_update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)


class NestedCreateAPIView(NestedCreateModelMixin,
													IPLogger):
	"""
	Concrete view for creating a model instance.
	"""
	def post(self, request, *args, **kwargs):
			return self.create(request, *args, **kwargs)


class ReportCreateView(NestedCreateModelMixin, CreateAPIView):
	queryset = Report.objects.all()
	serializer_class = ReportSerializer
	permission_classes = (permissions.IsAuthenticated, )

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)


class ReportListView(ListAPIView):
	queryset = Report.objects.all()
	serializer_class = ReportSerializer
	permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdminOrStaffOrReadOnly)


class ReportDetailsView(RetrieveUpdateDestroyAPIView):
	queryset = Report.objects.all()
	serializer_class = ReportSerializer
	permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdminOrStaffOrReadOnly)
	lookup_field = 'id'
