import random
import string

characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")

def generate_random_password(length=12):
	random.shuffle(characters)
	
	password = []
	for i in range(length):
		password.append(random.choice(characters))

	random.shuffle(password)

	return "".join(password)

