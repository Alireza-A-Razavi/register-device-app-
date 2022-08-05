from wordpress_xmlrpc import (Client, InvalidCredentialsError,
                              ServerConnectionError,)
from wordpress_xmlrpc.methods.users import GetUserInfo

# address = 'https://algotik.ir/xmlrpc.php'
# user = 'alireza'
# password = 'aRrgtj%R2BIXx$MZzDmrX@Wy'

def try_password(address, user, password):
    try:
        wp = Client(address, user, password)
        ts = wp.call(GetUserInfo())
        print(ts.first_name, ts.last_name)
        return "200", True
    except InvalidCredentialsError:
        return "401", False
    except ServerConnectionError:
        return "500", False
    except Exception as E:
        print("Out of bound Error")
        print(E)
        return "-", False
