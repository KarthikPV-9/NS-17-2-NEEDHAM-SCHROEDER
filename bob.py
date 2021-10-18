#implementation of alice client

#importing socket,hashing,base64,cryptographic libraries
import socket            
import hashlib
import os
import random
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet


#key deriving function
backend = default_backend()
salt= b"'fjgodifaoesidhaoekmwe"
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=50,
    backend=backend
)

bobkey="bob"
bobkey = bytes(bobkey, 'utf-8')
# SK = bytes(SK, 'utf-8')

bobkey = base64.urlsafe_b64encode(kdf.derive(bobkey))
# key = base64.urlsafe_b64encode(kdf.derive(key))


# Creating a socket
s = socket.socket()        
print ("Socket successfully created")
#port assigning
port = 5000        
#binding port to the socket
s.bind(('', port))        
# socket set to listen
s.listen(3)    


print ("waiting")           
print("BOB SECRET KEY:",bobkey)
# Accepting the connection from client.
c, addr = s.accept()    
# print ('Connection accepted from', addr )

#receive encrypted messegefromalice from the client program
rec=c.recv(1024).decode()

messegefromalice = Fernet(bobkey).decrypt(rec.encode())
messegefromalice=messegefromalice.decode()
messegefromalice=messegefromalice.split(",")
sender=messegefromalice[0]
sessionkey=messegefromalice[1]

print("---------------------------------------")
print("SENDER:",sender)
print("SESSION KEY:",sessionkey)


salt= b"'fjgodifaoesidhaoekmwe"
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=50,
    backend=backend
)

sessionkey = bytes(sessionkey, 'utf-8')
# SK = bytes(SK, 'utf-8')

sessionkey = base64.urlsafe_b64encode(kdf.derive(sessionkey))


nonce=random.randint(1,999999)
storednonce=nonce
nonce=str(nonce)

print("NONCE_SENT TO ALICE:",nonce)
nonce=Fernet(sessionkey).encrypt(nonce.encode())
nonce=nonce.decode('UTF-8')
c.send(str(nonce).encode())  
rec=c.recv(1024).decode()
rec = Fernet(sessionkey).decrypt(rec.encode())
rec=rec.decode()
print("NONCE_RECEIVED FROM ALICE:",rec)
# print(storednonce)
if int(rec) == storednonce-1:
    print("nonce matching connection established")

print("---------------------------------------")
s.close() 
