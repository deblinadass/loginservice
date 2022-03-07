from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_200_OK
)

from .ldapsearch import get_LDAP_user
from hstloginservice.service.tokengenerator import get_token, get_refresh_token
from hstloginservice.model.hstloginmodel import Login, Userrole, UserRoleAuthorisation
from django.http import JsonResponse
from hstloginservice.exceptionhandler.mstexceptionhandler import mst_custom_validation
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST
from hstloginservice.hstloginserviceconfig import JWT_KEYWORD
import jwt
from django.utils import timezone
from hstloginservice.serializer.hstloginserializer import UserRoleAuthorisationSerializer, UserRoleURLAuthorisationSerializer

pagesectioncache = dict()

@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username").lower()
    password = request.data.get("password")

    if username is None or password is None:
        print('UserName/Password not present in request')
        raise mst_custom_validation('Invalid Request', status_code = HTTP_400_BAD_REQUEST)
    try:
        user = Login.objects.getmstusergroup(username)
    except Exception:
        print('HTTP_403_FORBIDDEN-User does not exists in MST')
        raise mst_custom_validation('Authentication Failed', status_code = HTTP_403_FORBIDDEN)

    ldapResult = get_LDAP_user(user.useremail, password)
    if ldapResult is None:
        print('LDAP Authentication Failed')
        raise mst_custom_validation('Authentication Failed', status_code = HTTP_403_FORBIDDEN)
    
    if user.usergroup:
        lastlogintimestamp = user.userlastlogin
        Login.objects.updatelastlogintimestamp(ldapResult)
        return JsonResponse(get_token(username, user.usergroup, lastlogintimestamp, user.useremail ),  status=HTTP_200_OK)
    
    print('HTTP_403_FORBIDDEN-User does not exists in MST')
    raise mst_custom_validation('Authentication Failed', status_code = HTTP_403_FORBIDDEN)

@api_view(["POST"])
@permission_classes((AllowAny,))
def refresh(request):
    refreshtoken = request.data.get("mstseckey")
    if refreshtoken is None:
        raise mst_custom_validation('Invalid Token', status_code = HTTP_403_FORBIDDEN)
    try:
        return JsonResponse(get_refresh_token(refreshtoken), status=HTTP_200_OK)
    except Exception:
        raise mst_custom_validation('Invalid Token', status_code = HTTP_403_FORBIDDEN)

@api_view(["GET"])
@permission_classes((AllowAny,))
def checkUserRole(request, useraction):
    #usergroup ='01000010'
    usergroup = getUserGroup(request)
    roles = Userrole.objects.getuserrole(usergroup)
    for role in roles :
        if useraction == role.operations :
            return JsonResponse({"access":True}, status=HTTP_200_OK)
    return JsonResponse({"access":False}, status=HTTP_200_OK)

def getUserGroup(request):
        token = request.META.get('HTTP_AUTHORIZATION')
        #print(token)
        tokenarr = token.split()
        token = tokenarr[1]
        #print(token)
        try:
            decodedtoken = jwt.decode(token, JWT_KEYWORD, algorithms=['HS256'])
            usergroup = decodedtoken.get('role')
            return usergroup
        except jwt.ExpiredSignature:
            raise exceptions.AuthenticationFailed('Token Expired')
        except jwt.InvalidSignatureError:
            raise exceptions.AuthenticationFailed('Invalid Signature')

@api_view(["GET"])       
def getPageSectionAuthorisation(request, page):
    userrole = getUserGroup(request)
    #userrole = '01000010'
    if  str(page) + str(userrole) in pagesectioncache:
        serializer = pagesectioncache[str(page) + str(userrole)]
    else:
        customertab_list = UserRoleAuthorisation.objects.gettabsectiondetails(page, userrole)
        serializer = UserRoleAuthorisationSerializer(customertab_list, many=True)
        pagesectioncache[str(page) + str(userrole)] = serializer
    return JsonResponse(serializer.data, safe=False)
    
@api_view(["GET"])       
def getUserURLAuthorisation(request, userrole):
    url_list = UserRoleAuthorisation.objects.getUserRoleUrlsdetail(userrole)
    serializer = UserRoleURLAuthorisationSerializer(url_list, many=True)
    return JsonResponse(serializer.data, safe=False)