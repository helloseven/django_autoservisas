from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, FormMixin, UpdateView

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


class UserRegisterView(SuccessMessageMixin, CreateView):
    template_name = 'user_profile/register.html'
    success_url = reverse_lazy('login')
    form_class = UserRegisterForm
    success_message = _('Your profile was created successfully')


class UserProfileView(LoginRequiredMixin, DetailView, FormMixin):
    model = User
    template_name = 'user_profile/profile.html'
    form_class = UserUpdateForm
    
    def get_success_url(self):
        return reverse_lazy('user_profile:profile', kwargs={'pk' : self.object.id})

    def get_context_data(self, *args, **kwargs):
        context= super(UserProfileView, self).get_context_data(**kwargs)
        context['form'] = UserUpdateForm(instance=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, _('Profile updated successfuly.'))
            return redirect(reverse_lazy('user_profile:profile'))
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form' : u_form,
        'p_form' : p_form,
    }
    return render (request, 'user_profile/profile.html', context=context)
