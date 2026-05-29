"""
Accounts views — registration, login, logout, profile management.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy

from .forms import RegisterForm, LoginForm, ProfileUpdateForm, UserUpdateForm


@require_http_methods(["GET", "POST"])
def register(request):
    """New customer signup page."""
    if request.user.is_authenticated:
        return redirect('dashboard:redirect')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Auto-login after successful registration
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(
                    request,
                    f'Welcome aboard, {user.first_name}! '
                    f'Your GlobeTrek account is ready.',
                )
                return redirect('dashboard:redirect')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


class CustomLoginView(LoginView):
    """Customised login view with our styled form."""
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().first_name or form.get_user().username}!')
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    """Logout — redirects to home."""
    next_page = reverse_lazy('core:home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You have been logged out. Safe travels!')
        return super().dispatch(request, *args, **kwargs)


@login_required
@require_http_methods(["GET", "POST"])
def profile(request):
    """View + edit own profile."""
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile,
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('accounts:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'accounts/profile.html', {
        'u_form': u_form,
        'p_form': p_form,
    })
