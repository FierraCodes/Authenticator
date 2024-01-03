from cryptography.fernet import Fernet
import hashlib
import time

def gettkn(pubkey, privkey):
    f = Fernet(privkey)
    tkey = f.decrypt(pubkey).decode('utf-8') + '|' + str(round(time.time() / 10) * 10)
    hashed_key = hashlib.sha256(tkey.encode('utf-8')).hexdigest()
    return hashed_key

pubkey = bytes(input('Enter Public Key: '), 'utf-8')
privkey = bytes(input('Enter Private Key: '), 'utf-8')
inputtoken = input('Enter Auth Token: ')
if inputtoken == gettkn(pubkey, privkey):
    print('Success!')
else:
    print('Failed!')