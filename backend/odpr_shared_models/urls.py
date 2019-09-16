from django.urls import path
from . import views

app_name = 'odpr_shared_models'
urlpatterns = [
	path('reports/', views.ReportListView.as_view(), name='report-list'),
	path('reports/create/', views.ReportCreateView.as_view(), name='report-create'),
	path('reports/<int:id>', views.ReportDetailsView.as_view(), name='report-detail'),
]
