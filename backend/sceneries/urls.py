from django.urls import path
from . import views

app_name = 'sceneries'
urlpatterns = [
	path('', views.SceneryListView.as_view(), name='scenery-list'),
	path('<int:id>/', views.SceneryDetailView.as_view(), name='scenery-detail'),
	path('create/', views.SceneryCreateView.as_view(), name='scenery-create'),
	path('<int:id>/update/', views.SceneryDetailView.as_view(), name='scenery-update'),
	path('<int:id>/images/', views.SceneryImageListView.as_view(), name='scenery-images'),
	path('<int:id>/files/', views.SceneryFileListView.as_view(), name='scenery-files'),
	path('images/', views.SceneryImageDetailView.as_view(), name='scenery-image-detail'),
	path('files/', views.SceneryFileDetailView.as_view(), name='scenery-file-detail'),
	#path('<int:id>/files/', views.SceneryFileListView.as_view(), name='scenery-files'),
]
