from django.urls import path
from users.views import *
from django.contrib.auth.views import LogoutView, PasswordChangeDoneView

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name="sign-up"),
    path('sign-in/', sign_in, name="sign-in"),
    path('sign-out/', CustomSignOutView.as_view(), name="sign-out"),
    path('activate/<int:user_id>/<str:token>/', ActivateUserView.as_view()),
    path('admin/dashboard/', admin_dashboard, name="admin-dashboard"),
    path('admin/<int:user_id>/assign-role/', assign_role, name="assign-role"),
    path('admin/create-group', create_group, name="create-group"),
    path('admin/group-list', group_list, name="group-list"),
    path('delete-group/<int:group_id>/', delete_group, name='delete-group'),
    path('delete-user/<int:user_id>/', delete_user, name='delete-user'),
    
    #All Profile Related URl's:
    path('profile/', ProfileView.as_view(), name="user-profile"),
    path('passwd-change/', ChangePassword.as_view(template_name = 'accounts/password_change.html'), name="passwd-change"),
    path('passwd-change-done/', PasswordChangeDoneView.as_view(template_name = 'accounts/password_change_done.html'), name="password_change_done"),
    path('passwd-reset/', CustomPasswordResetView.as_view(), name="password_reset"),
    path('passwd-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('edit-profile/', EditProfileView.as_view(), name='edit-profile'),
]