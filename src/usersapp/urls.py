from .views import main, login_user, create_user_profile, logout_user, ResetPasswordView
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path


app_name = 'usersapp'

urlpatterns = [
    path('', main, name='main'),
    path('login/', login_user, name='login_user'),
    path('signup/', create_user_profile, name='create_user_profile'),
    path('logout/', logout_user, name='logout_user'),
    path('reset-password/', ResetPasswordView.as_view(), name='password_reset'),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name='usersapp/password_reset_done.html'),
         name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='usersapp/password_reset_confirm.html',
                                          success_url='/users/reset-password/complete/'),
         name='password_reset_confirm'),
    path('reset-password/complete/',
         PasswordResetCompleteView.as_view(template_name='usersapp/password_reset_complete.html'),
         name='password_reset_complete'),

]