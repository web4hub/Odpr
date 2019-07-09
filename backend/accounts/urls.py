from django.urls import path, include
from . import views as acc_views

app_name = 'accounts'
urlpatterns = [
	path('register/', acc_views.CustomRegisterView.as_view(), name='register'),
	path('reset-password/verify-token/', acc_views.CustomPasswordTokenVerificationView.as_view(), name='password_reset_verify_token'),
	path('reset-password/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
