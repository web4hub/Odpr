from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework import status
from .serializer_util import NestedModelSerializer

class NestedRetrieveModelMixin(RetrieveModelMixin):
	"""
	Retrieve a model instance.
	"""

	def retrieve(self, request, *args, **kwargs):
		instance = self.get_object()
		serializer = self.get_serializer(instance, serializer_type=NestedModelSerializer.GET)
		return Response(serializer.data)

class NestedUpdateModelMixin(UpdateModelMixin):
	"""
	Update a model instance.
	"""

	def update(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', False)
		instance = None
		try:
			instance = self.get_object()
		except AssertionError:
			pass
		serializer_type = NestedModelSerializer.PUT
		if partial:
			serializer_type = NestedModelSerializer.PATCH
		serializer = self.get_serializer(instance, data=request.data, partial=partial, serializer_type=serializer_type)
		serializer.is_valid(raise_exception=True)
		if not isinstance(serializer.validated_data, serializer.Meta.model):  # This is a special condition for files.
			self.perform_update(serializer)
		else:
			serializer.instance = serializer.validated_data

		if getattr(instance, '_prefetched_objects_cache', None):
			# If 'prefetch_related' has been applied to a queryset, we need to
			# forcibly invalidate the prefetch cache on the instance.
			instance._prefetched_objects_cache = {}

		return Response(serializer.data)

class NestedCreateModelMixin(CreateModelMixin):
	"""
	Create a model instance.
	"""

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data, serializer_type=NestedModelSerializer.POST)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
