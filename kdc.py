#implementation of KDC


#importing socket,hashing,base64,cryptographic libraries
import socket     
import string       
import hashlib
import os
import base64
import random
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

backend = default_backend()
salt= b"'fjgodifaoesidhaoekmwe"
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=50,
    backend=backend
)


#converting the keys to byte format
alicekey="alice"
alicekey = bytes(alicekey, 'utf-8')
bobkey="bob"
bobkey = bytes(bobkey, 'utf-8')

#genearating session key(random)
SK=''.join(random.choices(string.ascii_uppercase +string.digits, k = 10))
# SK = bytes(SK, 'utf-8')

#creating key for alice
alicekey = base64.urlsafe_b64encode(kdf.derive(alicekey))
print("------------------------------------------------")
# print(alicekey)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=50,
    backend=backend
)


#creating key for bob
bobkey = base64.urlsafe_b64encode(kdf.derive(bobkey))
# key = base64.urlsafe_b64encode(kdf.derive(key))


# Creating a socket
s = socket.socket()        
print ("Socket successfully created")

#port assigning
port = 4000        


#binding port to the socket
s.bind(('', port))        
print ("socket binded to %s" %(port))


# socket set to listen
s.listen(3)    
print ("socket is listening")           

while True:
    # Accepting the connection from client.
    c, addr = s.accept()    
    print ('Connection accepted from', addr )

    #receive username from the client program
    rec=c.recv(1024).decode()
    print("REQUEST SENT:",rec)
    rec=rec.split(",")
    noncerec=rec[0]
    sender=rec[1]
    recevier=rec[2]
    #encrypting the messege of sesssion key with key of bob
    messegeforbob=rec[1]+","+SK
    messegeforbob = Fernet(bobkey).encrypt(messegeforbob.encode())


    #creating the messege for alice with sesssion key appended to encrypted messege which should be sent to bob
    messegeforalice=noncerec+","+rec[2]+","+SK+"||"+messegeforbob.decode('UTF-8')

    #encrypting the messege of alice with key of alice
    messegeforalice = Fernet(alicekey).encrypt(messegeforalice.encode())


    #sending the messege to client program
    messegeforalice=messegeforalice.decode('UTF-8')
    c.send(str(messegeforalice).encode())


c.close()
