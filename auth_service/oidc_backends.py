from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from django.contrib.auth.models import User

class ShopflowOIDCBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        """
        Called when a new user logs in via OIDC and no corresponding Django user exists.
        Map useful claims to Django User fields.
        """
        username = claims.get("preferred_username") or claims.get("sub")
        user = User.objects.create_user(username=username)
        user.email = claims.get("email", "")
        user.first_name = claims.get("given_name", "") or ""
        user.last_name = claims.get("family_name", "") or ""
        user.save()
        return user

    def filter_users_by_claims(self, claims):
        """
        Try to find existing users by email first (common case).
        """
        email = claims.get("email")
        if not email:
            return User.objects.none()
        return User.objects.filter(email__iexact=email)