from rest_framework import authentication, exceptions
from .models import Token

class CustomTokenAuthentication(authentication.BaseAuthentication):
    keyword = 'Token' 
    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request)
        if not auth_header:
            return None 
        
        try:
            auth_str = auth_header.decode('utf-8')
        except UnicodeError:
            raise exceptions.AuthenticationFailed("Invalid token header")

        parts = auth_str.split()
        if len(parts) != 2 or parts[0] != self.keyword:
            return None

        token_str = parts[1]
        try:
            token_obj = Token.objects.get(token=token_str)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed("Token is invalid")

        user = token_obj.user
        if not user:
            raise exceptions.AuthenticationFailed("No user associated with this token")
        return (user, token_obj)
