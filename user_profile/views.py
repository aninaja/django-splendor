from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission, Group
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from user_profile.forms import ProfileCreationForm
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
