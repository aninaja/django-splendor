from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission, Group
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from user_profile.forms import ProfileCreationForm, RegistrationForm
from .utils import unique_id_generator


User = get_user_model()


class ProfileListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    ordering = ['-date_created']
    permission_required = 'profiles.view_user'

    def get_context_data(self, **kwargs):
        context = super(ProfileListView, self).get_context_data(**kwargs)
        return context


@login_required
# @permission_required('profiles.add_user', raise_exception=True)
def profile_create(request):
    form = ProfileCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        uid = User.objects.get(id=user.id)
        uid.user_id = unique_id_generator(user.id)
        uid.save()
        messages.success(request, 'User created successfully.')
        return redirect('/users')

    template_name = 'user_create.html'
    context = {'form': form}
    return render(request, template_name, context)


def group_create(request):
    if request.method == 'POST':
        permissions = request.POST.getlist('permission')
        new_group, group = Group.objects.get_or_create(
            name=request.POST['group_name']
        )
        new_group.permissions.set(permissions)
        return redirect('users:group_create')
    else:
        permission = Permission.objects.all()
        template = 'group_create.html'
    context = {
        "permission": permission
    }

    return render(request, template, context)


def patient_list(request):
    patients_list = User.objects.filter(is_patient=True).order_by('-date_created')
    template_name = 'patient_list.html'
    context = {'patients_list': patients_list}
    return render(request, template_name, context)


def patient_create(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        patient = form.save()
        patient.is_patient = True
        patient.save()
        messages.success(request, 'Patient registered successfully.')
        return redirect('users:patient_create')
    template_name = 'patient_create.html'
    context = {'form': form}
    return render(request, template_name, context)


