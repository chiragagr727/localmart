import json
from typing import Optional
import requests
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from jwt import PyJWKClient
import jwt
from django.contrib.auth import get_user_model

User = get_user_model()


class KeycloakJWTAuthentication(BaseAuthentication):
    """
    DRF authentication using Keycloak-issued JWTs (Bearer tokens).
    Validates signature via JWKS and maps user by email/username. Creates a local user record if needed.
    """

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return None
        token = auth_header.split(' ')[1]

        try:
            claims = self._decode_token(token)
        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Invalid token: {str(e)}')

        # Optional: audience/issuer checks
        issuer = claims.get('iss')
        if not issuer or settings.KEYCLOAK_REALM not in issuer:
            raise exceptions.AuthenticationFailed('Invalid token issuer')

        email = claims.get('email')
        preferred_username = claims.get('preferred_username') or claims.get('sub')
        if not (email or preferred_username):
            raise exceptions.AuthenticationFailed('Token missing user identifiers')

        user = self._get_or_create_user(email=email, username=preferred_username, claims=claims)
        return (user, None)

    def _jwks_client(self) -> PyJWKClient:
        jwks_url = f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/certs"
        return PyJWKClient(jwks_url)

    def _decode_token(self, token: str) -> dict:
        jwk_client = self._jwks_client()
        signing_key = jwk_client.get_signing_key_from_jwt(token)
        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            options={"verify_aud": False},
        )
        return claims

    def _get_or_create_user(self, email: Optional[str], username: str, claims: dict) -> User:
        try:
            if email:
                user = User.objects.filter(email=email).first()
                if user:
                    return user
            user = User.objects.filter(username=username).first()
            if user:
                return user
        except User.DoesNotExist:
            user = None

        # Create a local user if not exists
        first_name = claims.get('given_name', '')
        last_name = claims.get('family_name', '')
        user = User.objects.create_user(
            username=username,
            email=email or '',
            first_name=first_name,
            last_name=last_name,
            password=User.objects.make_random_password(),
            role='customer',  # default; frontend can elevate via admin/vendor flows
            status='active',
        )
        return user
