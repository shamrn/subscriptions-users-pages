from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import UserLoginForm

urlpatterns = [
    path('', views.account, name='account'),
    path('login/', auth_views.LoginView.as_view(authentication_form=UserLoginForm), name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),

    path('signup/', views.SignUp.as_view(), name='signup'),
    path('signup/<email>/<uuid>/',views.confirm_user,name='confirm_user'),

    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/complete',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

    path('password_change/', views.PortChangePassword.as_view(), name='password_change'),

    path('subscribe/<type_sub>/',views.get_subscribe,name='subscribe'),

]

