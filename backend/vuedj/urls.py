from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from api import views as api_views

app_name = 'main'
urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/v1/', include('api.urls')),
	path('accounts/', include('allauth.urls')),
	path('', api_views.index, name='home')
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += staticfiles_urlpatterns()

urlpatterns += [
	path('<path:path>', api_views.index, name='home')
]
