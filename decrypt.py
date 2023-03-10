
from socket import *
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

def sendEncryptedKey(eKeyFilePath):
    hostname = "192.168.1.101"
    port = 8000
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((hostname, port))
    with open(eKeyFilePath, "rb") as file:
        data = file.read()
        print("data = " + str(data))       
        sock.send(data)
        decryptedSymmetricKey = sock.recv(4064)
        with open(decrypedSymmetricKeyFile, "wb") as out_file:
        	out_file.write(decryptedSymmetricKey)
    sock.close()    	

def decryptFile(filePath, keyFile):
    filePath = "/home/kali/plain.txt"

    with open(keyFile, "rb") as file:	
	    symmetricKey = file.read()
	    print("symmetricKey: " + str(symmetricKey))

    with open(filePath, "rb") as file:
	    file_data = file.read()
	    print("file data: " + str(file_data))
	    FernetInstance = Fernet(symmetricKey)
	    decrypted_data = FernetInstance.decrypt(file_data)

    with open(filePath, "wb") as file:
    	file.write(decrypted_data)
                 
decrypedSymmetricKeyFile = "/home/kali/decrypedSymmetricKey.key"                 
sendEncryptedKey("/home/kali/encryptedSymmetricKey.key")
decryptFile('/home/kali/plain.txt', decrypedSymmetricKeyFile)                 
                 
