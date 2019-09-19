from .models import Scenery, SceneryImage, SceneryFile
from .serializers import ScenerySerializer, SceneryImageSerializer, SceneryFileSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from django.core.files.uploadhandler import InMemoryUploadedFile
from accounts.permissions import IsOwnerOrAdminOrStaffOrReadOnly, IsOwnerOrReadOnly
from odpr_shared_models.views import NestedRetrieveUpdateDestroyAPIView, NestedCreateAPIView
from rest_framework.parsers import FileUploadParser, ParseError, MultiPartParser, FormParser
from PIL import Image
from filer import settings as filer_settings
from filer.utils.loader import load_model
from django.forms.models import modelform_factory
from django.http.multipartparser import parse_header
from django.utils import timezone
from filer.models import FolderRoot, Folder
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from rest_framework import status
import io
import json

class NewFolderForm(forms.ModelForm):
	class Meta(object):
		model = Folder
		fields = ('name',)

class UploadException(Exception):
	pass

def get_scenery_by_id(pk):
	return Scenery.objects.get(pk=pk)

def get_scenery_serializer_permission_type(self):
	if self.request.user.is_authenticated and self.request.user.is_admin:
		return ScenerySerializer.ADMIN
	elif self.request.user.is_authenticated and self.request.user.is_staff:
		return ScenerySerializer.STAFF
	elif self.request.user.is_authenticated and \
		'kwargs' in self.request.parser_context and \
		'id' in self.request.parser_context['kwargs'] and \
		get_scenery_by_id(self.request.parser_context['kwargs']['id']).author.pk == self.request.user.id:
		return ScenerySerializer.AUTHOR
	elif self.request.user.is_authenticated:
		return ScenerySerializer.VIEWER
	else:
		return ScenerySerializer.GUEST


class SceneryCreateView(NestedCreateAPIView):
	queryset = Scenery.objects.all()
	serializer_class = ScenerySerializer
	permission_classes = (permissions.IsAuthenticated,)

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)

	def get_serializer(self, *args, **kwargs):
		serializer_class = self.get_serializer_class()
		kwargs['context'] = self.get_serializer_context()
		return serializer_class(permission_type=get_scenery_serializer_permission_type(self), *args, **kwargs)


class SceneryListView(generics.ListAPIView):
	queryset = Scenery.objects.filter(privacy_setting=0).order_by('-id')
	serializer_class = ScenerySerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
												IsOwnerOrReadOnly,)

	def get_serializer(self, *args, **kwargs):
		serializer_class = self.get_serializer_class()
		kwargs['context'] = self.get_serializer_context()
		return serializer_class(permission_type=get_scenery_serializer_permission_type(self), *args, **kwargs)


class SceneryDetailView(NestedRetrieveUpdateDestroyAPIView):
	queryset = Scenery.objects.all()
	serializer_class = ScenerySerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
												IsOwnerOrAdminOrStaffOrReadOnly,)
	lookup_field = 'id'

	def get_serializer(self, *args, **kwargs):
		serializer_class = self.get_serializer_class()
		kwargs['context'] = self.get_serializer_context()
		return serializer_class(permission_type=get_scenery_serializer_permission_type(self), *args, **kwargs)

	def retrieve(self, request, *args, **kwargs):
		response = super(SceneryDetailView, self).retrieve(self, request, *args, **kwargs)
		if hasattr(response, 'data') and 'id' in response.data:
			scenery = Scenery.objects.get(pk=response.data['id'])
			scenery.visit_count = F('visit_count') + 1
			scenery.save()
		return response


class ImageUploadParser(FileUploadParser):
	media_type = 'image/*'

class SceneryImageListView(generics.ListAPIView):
	queryset = SceneryImage.objects.all()
	serializer_class = SceneryImageSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
												IsOwnerOrReadOnly,)

	def list(self, request, *args, **kwargs):
		self.queryset = SceneryImage.objects.filter(scenery=request.data['scenery'])
		super(SceneryImageListView, self).list(request, *args, **kwargs)


def get_or_create_root_folder():
	try:
		return Folder.objects.get(name='filer_root')
	except ObjectDoesNotExist:
		root_folder_form = NewFolderForm({'name': 'filer_root'})
		if root_folder_form.is_valid():
			new_folder = root_folder_form.save(commit=True)
			return new_folder
		else:
			raise AttributeError('Could not create root folder')

def get_or_create_user_folder(user):
	try:
		return Folder.objects.get(name='user_{}'.format(user.id))
	except ObjectDoesNotExist:
		root_folder = get_or_create_root_folder()
		new_folder_form = NewFolderForm({'name': 'user_{}'.format(user.id)})
		if new_folder_form.is_valid():
			new_folder = new_folder_form.save(commit=False)
			if root_folder.contains_folder(new_folder.name):
				raise ValueError('Folder with this name already exists.')
			else:
				new_folder.parent = root_folder
				new_folder.owner = user
				new_folder.save()


class SceneryImageDetailView(NestedRetrieveUpdateDestroyAPIView):
	queryset = SceneryImage.objects.all()
	serializer_class = SceneryImageSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
												IsOwnerOrAdminOrStaffOrReadOnly,)
	# parser_classes = (ImageUploadParser,)
	parser_classes = (MultiPartParser, FormParser, FileUploadParser)
	lookup_field = 'id'

	def put(self, request, *args, **kwargs):
		try:
			# temp = request.data
			# Note: currently, django tests with multipart/form-data do not fill the request.FILES field, but requests by
			# the Vue frontend with axios DO. That's weird, and I do not know the reason for this, but it works and I'll
			# leave it for now.
			if len(request.FILES) != 2 or 'file' not in request.FILES or 'scenery' not in request.FILES:
				raise UploadException('Bad file request. Need to contain file and scenery ID.')

			scenery_id_json_bytes = request.FILES['scenery'].read()
			scenery_id_json = json.loads(scenery_id_json_bytes.decode('utf-8'))
			scenery_id = int(scenery_id_json['scenery'])

			upload = request.FILES['file']
			filename = upload.name

			folder = get_or_create_user_folder(request.user)

			for filer_class in filer_settings.FILER_FILE_MODELS:
				FileSubClass = load_model(filer_class)
				# TODO: What if there are more than one that qualify?
				if FileSubClass.matches_file_type(filename, upload, request):
					FileForm = modelform_factory(
						model=FileSubClass,
						fields=('original_filename', 'owner', 'file')
					)
					break
			uploadform = FileForm({'original_filename': filename,
														 'owner': request.user.pk},
														{'file': upload})
			if uploadform.is_valid():
				file_obj = uploadform.save(commit=False)
				# Enforce the FILER_IS_PUBLIC_DEFAULT
				file_obj.is_public = filer_settings.FILER_IS_PUBLIC_DEFAULT
				file_obj.folder = folder
				file_obj.save()

				# Try to generate thumbnails.
				if not file_obj.icons:
					# There is no point to continue, as we can't generate
					# thumbnails for this file. Usual reasons: bad format or
					# filename.
					file_obj.delete()
					# This would be logged in BaseImage._generate_thumbnails()
					# if FILER_ENABLE_LOGGING is on.
					return Response(
						data={'error': 'failed to generate icons for file'},
						status=status.HTTP_500_INTERNAL_SERVER_ERROR,
					)

				# Save file object to SceneryFile/SceneryImage
				request.data.clear()
				request.data['image'] = file_obj
				request.data['scenery'] = scenery_id
				response = super(SceneryImageDetailView, self).put(request, *args, **kwargs)
				scenery_image_instance = SceneryImage.objects.get(pk=response.data['id'])
				scenery_image_instance.author = request.user
				scenery_image_instance.save()

				thumbnail = None
				# Backwards compatibility: try to get specific icon size (32px)
				# first. Then try medium icon size (they are already sorted),
				# fallback to the first (smallest) configured icon.
				for size in (['32'] +
										 filer_settings.FILER_ADMIN_ICON_SIZES[1::-1]):
					try:
						thumbnail = file_obj.icons[size]
						break
					except KeyError:
						continue

				data = {
					'thumbnail': thumbnail,
					'alt_text': '',
					'label': str(file_obj),
					'file_id': file_obj.pk,
				}
				# prepare preview thumbnail
				if type(file_obj) == Image:
					thumbnail_180_options = {
						'size': (180, 180),
						'crop': True,
						'upscale': True,
					}
					thumbnail_180 = file_obj.file.get_thumbnail(
						thumbnail_180_options)
					data['thumbnail_180'] = thumbnail_180.url
					data['original_image'] = file_obj.url
				return Response(data=data, status=status.HTTP_201_CREATED)  # TODO: add something to data?

			else:
				form_errors = '; '.join(['%s: %s' % (
					field,
					', '.join(errors)) for field, errors in list(
					uploadform.errors.items())
																 ])
				raise UploadException(
					"AJAX request not valid: form invalid '%s'" % (
						form_errors,))

		except UploadException as e:
			return Response(data={'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

		# # multipart/form-data
		#
		# #del request._full_data
		# data = request.data
		#
		# if 'image' not in data or 'scenery' not in data:
		# 	raise ParseError('Empty or invalid content')
		#
		# f = bytes(data['image'], 'utf-8')
		# if f is None:
		# 	raise ParseError('Empty content')
		#
		# file = io.BytesIO(f)
		#
		# django_valid_file = InMemoryUploadedFile(
		# 	file=file, field_name='temp', name='temp', content_type=request.content_type, size=len(f), charset='utf-8'
		# )
		# # try:
		# # 	img = Image.open(io.BytesIO(f))
		# # 	img.verify()
		# # except IOError:
		# # 	raise ParseError('Unsupported image type')
		# # TODO: would have been nice to support this image verification, but there are differencies in the header of my
		# # TODO: test mock and the one this library is comparing to.
		# request._full_data = {
		# 	'image': {
		# 		'file_ptr': {
		# 			# 'file': io.BytesIO(f),
		# 			'file': django_valid_file
		# 			#'uploaded_at': timezone.now(),
		# 			#'modified_at': timezone.now()
		# 		}
		# 		#'uploaded_at': timezone.now(),
		# 		#'modified_at': timezone.now()
		# 	},
		# 	'scenery': int(data['scenery'])
		# }
		#
		# response = super(SceneryImageDetailView, self).put(request, *args, **kwargs)
		# scenery_image_wrapper = SceneryImage.objects.get(pk=response.data['id'])
		# scenery_image_serializer = self.serializer_class(instance=scenery_image_wrapper, data=f)
		# scenery_image_serializer.is_valid(raise_exception=True)
		# file_instance = scenery_image_serializer.save()
		# # TODO: look if the wrapper has its file...
		# # SceneryImage.objects.get(pk=1).image.save()
		# # SceneryImage.image.save(f.name, f, save=True)
		# response.data.update({'image': file_instance.image})
		# return response

	# If it is called without a filename URL keyword argument, then the client must set the filename
	# in the Content-Disposition HTTP header. For example Content-Disposition: attachment; filename=upload.jpg.
	# .media_type: */*

	# def put(self, request, *args, **kwargs):


# TODO: test whether permissions work properly: only author, staff and admin can edit files?
class SceneryFileListView(generics.ListAPIView):
	queryset = SceneryFile.objects.all()
	serializer_class = SceneryFileSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
												IsOwnerOrReadOnly,)

	def list(self, request, *args, **kwargs):
		self.queryset = SceneryFile.objects.filter(scenery=request.data['scenery'])
		super(SceneryFileListView, self).list(request, *args, **kwargs)


class SceneryFileDetailView(NestedRetrieveUpdateDestroyAPIView):
	queryset = SceneryFile.objects.all()
	serializer_class = SceneryFileSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
												IsOwnerOrAdminOrStaffOrReadOnly,)
	# parser_classes = (ImageUploadParser,)
	parser_classes = (MultiPartParser, FormParser, FileUploadParser)
	lookup_field = 'id'

	def retrieve(self, request, *args, **kwargs):
		response = super(SceneryFileDetailView, self).retrieve(self, request, *args, **kwargs)
		if hasattr(response, 'data') and 'scenery' in response.data:
			scenery = Scenery.objects.get(pk=response.data['scenery'])
			scenery.download_count = F('download_count') + 1
			scenery.save()
		return response

	def put(self, request, *args, **kwargs):
		try:
			if len(request.FILES) != 2 or 'file' not in request.FILES or 'scenery' not in request.FILES:
				raise UploadException('Bad file request. Need to contain file and scenery ID.')

			scenery_id_json_bytes = request.FILES['scenery'].read()
			scenery_id_json = json.loads(scenery_id_json_bytes.decode('utf-8'))
			scenery_id = int(scenery_id_json['scenery'])

			upload = request.FILES['file']
			filename = upload.name

			folder = get_or_create_user_folder(request.user)

			for filer_class in filer_settings.FILER_FILE_MODELS:
				FileSubClass = load_model(filer_class)
				# TODO: What if there are more than one that qualify?
				if FileSubClass.matches_file_type(filename, upload, request):
					FileForm = modelform_factory(
						model=FileSubClass,
						fields=('original_filename', 'owner', 'file')
					)
					break
			uploadform = FileForm({'original_filename': filename,
														 'owner': request.user.pk},
														{'file': upload})
			if uploadform.is_valid():
				file_obj = uploadform.save(commit=False)
				# Enforce the FILER_IS_PUBLIC_DEFAULT
				file_obj.is_public = filer_settings.FILER_IS_PUBLIC_DEFAULT
				file_obj.folder = folder
				file_obj.save()

				# Try to generate thumbnails.
				if not file_obj.icons:
					# There is no point to continue, as we can't generate
					# thumbnails for this file. Usual reasons: bad format or
					# filename.
					file_obj.delete()
					# This would be logged in BaseImage._generate_thumbnails()
					# if FILER_ENABLE_LOGGING is on.
					return Response(
						data={'error': 'failed to generate icons for file'},
						status=status.HTTP_500_INTERNAL_SERVER_ERROR,
					)

				# Save file object to SceneryFile/SceneryImage
				request.data.clear()
				request.data['file'] = file_obj
				request.data['scenery'] = scenery_id
				response = super(SceneryFileDetailView, self).put(request, *args, **kwargs)
				scenery_file_instance = SceneryFile.objects.get(pk=response.data['id'])
				scenery_file_instance.author = request.user
				scenery_file_instance.save()

				thumbnail = None
				# Backwards compatibility: try to get specific icon size (32px)
				# first. Then try medium icon size (they are already sorted),
				# fallback to the first (smallest) configured icon.
				for size in (['32'] +
										 filer_settings.FILER_ADMIN_ICON_SIZES[1::-1]):
					try:
						thumbnail = file_obj.icons[size]
						break
					except KeyError:
						continue

				data = {
					'thumbnail': thumbnail,
					'alt_text': '',
					'label': str(file_obj),
					'file_id': file_obj.pk,
				}
				# prepare preview thumbnail
				if type(file_obj) == Image:
					thumbnail_180_options = {
						'size': (180, 180),
						'crop': True,
						'upscale': True,
					}
					thumbnail_180 = file_obj.file.get_thumbnail(
						thumbnail_180_options)
					data['thumbnail_180'] = thumbnail_180.url
					data['original_image'] = file_obj.url
				return Response(data=data, status=status.HTTP_201_CREATED)  # TODO: add something to data?

			else:
				form_errors = '; '.join(['%s: %s' % (
					field,
					', '.join(errors)) for field, errors in list(
					uploadform.errors.items())
																 ])
				raise UploadException(
					"AJAX request not valid: form invalid '%s'" % (
						form_errors,))

		except UploadException as e:
			return Response(data={'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
