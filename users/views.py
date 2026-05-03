from django.views import generic
from django.contrib.auth import (
    get_user_model,
    login,
    update_session_auth_hash,
    logout,
)
from .forms import RegisterForm, LoginForm, ProfileEditForm, PasswordChangeForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


User = get_user_model()  # noqa: N806


class UserList(generic.ListView):
    model = User
    template_name = 'users/participants.html'
    context_object_name = 'participants'

    def get_queryset(self):
        queryset = User.objects.all().order_by('pk')
        return queryset


class UserDetail(generic.DetailView):
    model = User
    template_name = 'users/user-details.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'user'


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('projects:project_list')
    model = User

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class LoginView(generic.FormView):
    form_class = LoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('projects:project_list')

    def form_valid(self, form):
        login(self.request, form.user_cache)
        return super().form_valid(form)


class ProfileEditView(LoginRequiredMixin, generic.UpdateView):
    form_class = ProfileEditForm
    template_name = 'users/edit_profile.html'
    model = User

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'users:profile',
            kwargs={'user_id': self.request.user.pk}
        )


class PasswordChangeView(LoginRequiredMixin, generic.FormView):
    form_class = PasswordChangeForm
    template_name = 'users/change_password.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        new_password = form.cleaned_data.get('new_password1')
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'users:profile',
            kwargs={'user_id': self.request.user.pk}
        )


class MyLogoutView(generic.View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('projects:project_list'))

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('projects:project_list'))
