
import jwt
from hstloginservice.hstloginserviceconfig import JWT_SECRET, JWT_TOKEN_PREFIX
from rest_framework.authentication import BaseAuthentication

class HSTBackendTokenFilter(BaseAuthentication):
        
    def authenticate(self, request):
        header = request.META.get('HTTP_AUTHORIZATION', None)
        token = self.__get_token(header)
        if token:
            try:
                jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
                return None
            except jwt.ExpiredSignature:
                raise jwt.ExpiredSignature
        else:
            raise jwt.InvalidTokenError
    
    def __get_token(self, header):
        bearer, _, token = header.partition(' ')
        if bearer != JWT_TOKEN_PREFIX:
            raise ValueError('Invalid token')

        return token