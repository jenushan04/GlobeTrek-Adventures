"""
Custom decorators for role-based access control.
Use @role_required('admin') or @role_required('staff', 'admin') above any view.
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied


def role_required(*allowed_roles):
    """
    Decorator that restricts view access to users with one of the given roles.

    Usage:
        @role_required('admin')
        def admin_only_view(request): ...

        @role_required('staff', 'admin')
        def staff_or_admin_view(request): ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, 'Please log in to access that page.')
                return redirect('accounts:login')

            if not hasattr(request.user, 'profile'):
                raise PermissionDenied('No profile attached to this user.')

            if request.user.profile.role not in allowed_roles:
                messages.error(
                    request,
                    f'Access denied — this area is restricted to '
                    f'{", ".join(allowed_roles)} users.',
                )
                raise PermissionDenied(
                    f'Required roles: {allowed_roles}, '
                    f'current role: {request.user.profile.role}'
                )

            return view_func(request, *args, **kwargs)

        return _wrapped
    return decorator
