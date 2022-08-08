import random
import string
from wordpress_xmlrpc import (Client, InvalidCredentialsError,
                              ServerConnectionError,)
from wordpress_xmlrpc.methods.users import GetUserInfo
from rest_framework import status

from .models import User

characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")

def generate_random_password(length=12):
	random.shuffle(characters)
	
	password = []
	for i in range(length):
		password.append(random.choice(characters))

	random.shuffle(password)

	return "".join(password)

# address = 'https://algotik.ir/xmlrpc.php'
# user = 'alireza'
# password = 'aRrgtj%R2BIXx$MZzDmrX@Wy'

def try_password(address, user, password):
    try:
        wp = Client(address, user, password)
        ts = wp.call(GetUserInfo())
        print(ts.first_name, ts.last_name, ts.id)
        return 200, True, ts
    except InvalidCredentialsError:
        return 401, False, None
    except ServerConnectionError:
        return 500, False, None
    except Exception as E:
        print("Out of bound Error")
        print(E)
        return "-", False, None

def user_verify_and_creation(username, password):
    status_code, status_bool, user_data = try_password(
        address="https://algotik.ir/xmlrpc.php",
        user=username,
        password=password,
    )
    user = None
    if user_data:
        user, created = User.objects.get_or_create(
            wp_user_id=user_data.id, 
            username=user_data.username,
            first_name=user_data.first_name,
            last_name=user_data.last_name,

        )
        user.set_password(password)
        user.save()
        if created:
            return {"user": user , "status_code":status.HTTP_201_CREATED}
        else:
            return {"user": user , "status_code":status.HTTP_200_OK}
    elif status_code == 401:
        return {"user": user , "status_code":status.HTTP_401_UNAUTHORIZED}
    elif status_code == 500:
        return {"user": user , "status_code":status.HTTP_500_INTERNAL_SERVER_ERROR}
    else:
        return {"user": user, "status_code": status.HTTP_403_FORBIDDEN}

