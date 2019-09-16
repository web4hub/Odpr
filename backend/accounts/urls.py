from django.urls import path, include
from . import views as acc_views

app_name = 'accounts'
urlpatterns = [
	path('', acc_views.UserListView.as_view(), name='user-list'),
	path('login/', acc_views.UserLoginView.as_view(), name='login'),
	path('user-data/', acc_views.UserDataView.as_view(), name='user-data'),
	path('logout/', acc_views.UserLogoutView.as_view(), name='logout'),
	path('register/', acc_views.CustomRegisterView.as_view(), name='register'),
	# path('reset-password/', acc_views.PasswordResetView.as_view(),  name='reset-password'),
	# path('reset-password/', acc_views.CustomPasswordResetView.as_view(), name='reset-password'),
	# path('reset-password-confirm/', acc_views.CustomPasswordResetConfirmView.as_view(), name='reset-password-confirm'),
	path('reset-password/verify-token/', acc_views.CustomPasswordTokenVerificationView.as_view(), name='password_reset_verify_token'),
	path('reset-password/', include('django_rest_passwordreset.urls', namespace='password_reset')),
	path('<int:id>/', acc_views.UserDetailView.as_view(), name='user-detail'),
	# path('', include('allauth.urls')),
]
