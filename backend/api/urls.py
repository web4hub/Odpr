from django.urls import path, include

app_name = 'api'
urlpatterns = [
  path('auth/', include('accounts.urls')),
  path('sceneries/', include('sceneries.urls', namespace='sceneries')),
  path('requests/', include('scenery_requests.urls', namespace='requests')),
  path('documentation/', include('documentation.urls', namespace='documentation')),
  path('', include('odpr_shared_models.urls'))
]
