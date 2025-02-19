from django.urls import path
from users.views import *

urlpatterns = [
    path('sign-up/', sign_up, name="sign-up"),
    path('sign-in/', sign_in, name="sign-in"),
    path('sign-out/', sign_out, name="sign-out"),
    path('activate/<int:user_id>/<str:token>/', activate_user),
    path('admin/dashboard/', admin_dashboard, name="admin-dashboard"),
    path('admin/<int:user_id>/assign-role/', assign_role, name="assign-role"),
    path('admin/create-group', create_group, name="create-group"),
    path('admin/group-list', group_list, name="group-list"),
    path('delete-group/<int:group_id>/', delete_group, name='delete-group'),
    path('delete-user/<int:user_id>/', delete_user, name='delete-user'),
]