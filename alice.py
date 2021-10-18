#implementation of alice client

#importing socket,hashing,base64,cryptographic libraries
import socket            
import hashlib
import os
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


#declaring the secret key of alice
alicekey="alice"
alicekey = bytes(alicekey, 'utf-8')
alicekey = base64.urlsafe_b64encode(kdf.derive(alicekey))
print("------------------------------------------------")
print("ALICE SECRET KEY:",alicekey)


# Creating a socket
s = socket.socket()        

# defining the port number
port = 4000
    
# connecting to the KDCserver(local)
s.connect(('127.0.0.1', port))

#taking the nonce 
nonce=input("Enter nonce : ")
nonce=nonce+",alice"+",bob"
#sending a nonce to server
s.send(nonce.encode())

# receive the messege from server which consists of nonce,session key which can be decrypted by using the secret of alice and the session key which is encrpted with the secret key of bob
rec=s.recv(1024).decode()
print("MSG FROM KDC:",rec)


#extracting the messege for alice and bob
messegeforalice = Fernet(alicekey).decrypt(rec.encode())
print("---------------------------------------")
messegeforalice=messegeforalice.decode()
print("DECRYPTED MESSEGE:",messegeforalice)
received=messegeforalice.split("||")

#printing the seperated contents
print(received)
print("---------------------------------------")
messegeforalice=received[0].split(",")
print("NONCE SENT FROM KDC:",messegeforalice[0])
print("RECEIVER:",messegeforalice[1])
print("SESSION KEY:",messegeforalice[2])


#checking if the nonce sent by KDC is match with the nonce we sent
recnonce=messegeforalice[0]
if recnonce != nonce:
    #if the nonce dont match the connection will be closed
    s.close()
sessionkey=messegeforalice[2]
messegeforbob=received[1]

#displaying session key sent by KDC 
# print("SESSION KEY:",sessionkey)


#closing the connection with KDC
s.close()  


#starting connection with recevier(bob)

salt= b"'fjgodifaoesidhaoekmwe"
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=50,
    backend=backend
)


#hashing the derived session key with the same hash fucntion as that of bob
sessionkey = bytes(sessionkey, 'utf-8')
sessionkey = base64.urlsafe_b64encode(kdf.derive(sessionkey))

print("Connection with server closed")


#creating new socketobject to connect with bob
s = socket.socket()        

# defing the port number
port = 5000
    
# connecting to the server(local)
s.connect(('127.0.0.1', port))

# messegeforbob=messegeforbob.decode('UTF-8')
#sendin the messege received from KDC to bob which is encrypted with the secret key of bob

s.send(str(messegeforbob).encode())  


#receiving the nonce from bob and decrypting it with the session key created by KDC
receivednonce = s.recv(1024).decode()
receivednonce=Fernet(sessionkey).decrypt(receivednonce.encode())
receivednonce=receivednonce.decode()
print("NONCE RECEIVED FROM BOB:",receivednonce)
receivednonce=int(receivednonce)
receivednonce=receivednonce-1
receivednonce=str(receivednonce)
receivednonce=Fernet(sessionkey).encrypt(receivednonce.encode())
receivednonce=receivednonce.decode('UTF-8')
s.send(str(receivednonce).encode())  
s.close()