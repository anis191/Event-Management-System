from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.forms import *
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required, user_passes_test
# from events.views import user_role

# check admin or not
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def user_role(user):
    if user.is_authenticated:
        if user.groups.filter(name='Admin').exists():
            return 'Admin'
        elif user.groups.filter(name='Organizer').exists():
            return 'Organizer'
        elif user.groups.filter(name='Participant').exists():
            return 'Participant'
    return None

def sign_up(request):
    form = CustomRegisterForm()
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('CreatePassword'))
            user.is_active = False
            user.save()
            messages.success(request, "A confirmation mail sent. Check your email")
            return redirect('sign-in')
        else:
            print("Form is not valid")
    return render(request, "registration/sign_up.html", {"form":form})

def sign_in(request):
    # Django custom sign-in/login form:
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            user_type = user_role(request.user)
            # return redirect('home')
            if user_type == 'Admin':
                return redirect('admin-dashboard')
            elif user_type == 'Organizer':
                return redirect('organizer-dashboard')
            elif user_type == 'Participant':
                return redirect('participant-dashboard')
    return render(request, "registration/sign_in.html", {'form':form})

@login_required
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        # now varify token using build in authenticate function:
        if default_token_generator.check_token(user, token):
            user.is_active = True
            participant_group, created = Group.objects.get_or_create(name='Participant')
            user.groups.add(participant_group)
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse("Invalid user id and url's")
    except:
        return HttpResponse('User Not Found!')

@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    ).all()
    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = "No Group Assign"
    return render(request, 'admin/dashboard.html', {"users" : users})

@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    user = User.objects.get(id = user_id)
    form = AssignRoleForm()
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear() #Remove Old Role
            user.groups.add(role)
            messages.success(request, f"User {user.username} has been assigned to the {role.name} role")
            return redirect('admin-dashboard')
    return render(request, 'admin/assign_role.html', {"form" : form})

@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group '{group.name}' has been Created")
            return redirect('create-group')
    return render(request, 'admin/create_group.html', {"form" : form})

@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions__content_type').all()
    return render(request, 'admin/group_list.html', {"groups": groups})

@user_passes_test(is_admin, login_url='no-permission')
def delete_group(request, group_id):
    if request.method == "POST":
        group = Group.objects.get(id = group_id)
        group.delete()
        messages.success(request, "Group deleted successfully.")
    return redirect('group-list')

@user_passes_test(is_admin, login_url='no-permission')
def delete_user(request, user_id):
    if request.method == "POST":
        user = User.objects.get(id = user_id)
        user.delete()
        messages.success(request, "User deleted successfully.")
    return redirect('admin-dashboard')