from django.urls import path
from . import views

app_name = 'scenery_requests'
urlpatterns = [
	path('', views.RequestListView.as_view(), name='request-list'),
	path('<int:id>/', views.RequestDetailView.as_view(), name='request-detail'),
	path('create/', views.RequestCreateView.as_view(), name='request-create'),
	path('<int:id>/update/', views.RequestDetailView.as_view(), name='request-update'),
]
