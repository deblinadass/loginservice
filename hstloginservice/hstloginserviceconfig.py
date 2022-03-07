
import os

#Defining LDAP Constants
LDAP_SERVER = 'ldap://ldap.kpnnl.local:389'
LDAP_SEARCH_BASE = 'DC=kpnnl,DC=local'
LDAP_AUTH_USER = 'cn=srv_ldap_mbp,OU=Service Accounts,OU=Accounts,OU=Workspace,DC=kpnnl,DC=local'
LDAP_AUTH_PASSWORD = os.environ["LDAP_AUTH_PASSWORD"]
LDAP_SEARCH_ENTRY = 'mail'

#Defining JWT Constants
JWT_BASICTOKEN_EXPTIME = os.environ["JWT_BASICTOKEN_EXPTIME"]
JWT_REFRESHTOKEN_EXPTIME = os.environ["JWT_REFRESHTOKEN_EXPTIME"]
JWT_KEYWORD = os.environ["JWT_KEYWORD"]
JWT_KEYWORD_REFRESH = os.environ["JWT_KEYWORD_REFRESH"]
JWT_KEYWORD_PREFIX = os.environ["JWT_KEYWORD_PREFIX"]


