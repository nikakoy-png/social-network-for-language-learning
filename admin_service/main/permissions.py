from rest_framework import permissions
from rest_framework_simplejwt.tokens import AccessToken

from main.models import Admin


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            print(54645654654)
            authorization_header = request.headers.get('Authorization')
            print(request)
            if not authorization_header:
                return False  # No Authorization header present

            token = authorization_header.split()[1]
            access_token = AccessToken(token)
            admin_id = access_token.payload.get('user_id')

            # Check if admin exists
            admin = Admin.objects.get(pk=admin_id)
            return True
        except (Admin.DoesNotExist, KeyError, IndexError):
            return False  # User is not admin or token is invalid
        except Exception as e:
            # Log or handle other exceptions as needed
            return False