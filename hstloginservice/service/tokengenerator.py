

import jwt
import datetime
from hstloginservice.hstloginserviceconfig import JWT_BASICTOKEN_EXPTIME, JWT_REFRESHTOKEN_EXPTIME, JWT_KEYWORD, JWT_KEYWORD_REFRESH

def get_token(username, userrole, userprevlogin, useremail):
    payload_token = {
    'user': username,
    'role': userrole,
    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=int(JWT_BASICTOKEN_EXPTIME))
    }
    payload_refreshtoken = {
    'user': username,
    'role': userrole,
    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=int(JWT_REFRESHTOKEN_EXPTIME))
    }
    return ({"username":username, "userrole":userrole,'userprevlogin' : userprevlogin, "useremail":useremail, "accessToken":str(jwt.encode(payload_token, JWT_KEYWORD, algorithm='HS256').decode('utf-8')), "refreshToken": str(jwt.encode(payload_refreshtoken, JWT_KEYWORD_REFRESH, algorithm='HS256').decode('utf-8'))})

def get_token_refresh(username, userrole):
    payload_token = {
    'user': username,
    'role': userrole,
    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=int(JWT_BASICTOKEN_EXPTIME))
    }
    payload_refreshtoken = {
    'user': username,
    'role': userrole,
    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=int(JWT_REFRESHTOKEN_EXPTIME))
    }
    return ({"username":username,"accessToken":str(jwt.encode(payload_token, JWT_KEYWORD, algorithm='HS256').decode('utf-8')),"refreshToken": str(jwt.encode(payload_refreshtoken, JWT_KEYWORD_REFRESH, algorithm='HS256').decode('utf-8'))})


def get_refresh_token(refreshtoken):
    decodetoken = jwt.decode(refreshtoken, JWT_KEYWORD_REFRESH, algorithms=['HS256'])
    return get_token_refresh(decodetoken.get('user'), decodetoken.get('role'))
