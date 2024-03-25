from django.core.exceptions import PermissionDenied


def admin_required(view):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin:
            raise PermissionDenied()
        return view(request, *args, **kwargs)

    return wrapper
