import time
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

user = input('Username: ')
email = input('E-Mail: ')
password = input('Password: ')

temp = user + '|' + email + '|' + password + '|' + str(time.time())
pubkey = f.encrypt(bytes(temp, 'utf-8'))


print('Private Key: ' + key.decode('utf-8'))
print('Public Key: ' + pubkey.decode('utf-8'))
print('Expires In 10 Mins')