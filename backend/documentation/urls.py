from django.urls import path
from . import views

app_name = 'documentation'
urlpatterns = [
	path('', views.DocumentListView.as_view(), name='document-list'),
	path('<int:id>/', views.DocumentDetailView.as_view(), name='document-detail'),
	path('create/', views.DocumentCreateView.as_view(), name='document-create'),
	path('<int:id>/update/', views.DocumentDetailView.as_view(), name='document-update'),
]
