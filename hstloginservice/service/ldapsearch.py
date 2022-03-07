
from hstloginservice.hstloginserviceconfig import LDAP_SERVER, LDAP_AUTH_USER, LDAP_AUTH_PASSWORD, LDAP_SEARCH_BASE, LDAP_SEARCH_ENTRY
from ldap3 import Server, Connection, ALL, utils


# Check user authentication in the LDAP and return his information
def get_LDAP_user(useremail, password):
    server = Server(LDAP_SERVER, get_info=ALL)
    '''Keeping commented in case required later
    #connection = Connection(server, LDAP_AUTH_USER, LDAP_AUTH_PASSWORD, auto_bind=True)
    #success  = connection.search(LDAP_SEARCH_BASE, search_filter="(&(sAMAccountName=%s))"%(utils.conv.escape_filter_chars(username)), attributes=['*'])
    #if not success or len(connection.entries) != 1:
    #    return None
    #Connection(server, connection.entries[0][LDAP_SEARCH_ENTRY].value, password, auto_bind=True)'''
    Connection(server, useremail, password, auto_bind=True)
    return useremail        