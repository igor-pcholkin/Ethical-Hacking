import socketserver
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

class ClientHandler(socketserver.BaseRequestHandler):

    def handle(self):
        encrypted_key = self.request.recv(1024).strip()
        print ("Implement decryption of data " + str(encrypted_key) )
        #------------------------------------
        #      Decryption Code Here
        #------------------------------------
        
        with open("/home/kali/pub_priv_pair.key", "rb") as key_file:
	        private_key = serialization.load_pem_private_key(key_file.read(),
		        password=None
	        )
        
        decryptedSymmetricKey = private_key.decrypt(
    		encrypted_key,
    		padding.OAEP(
        		mgf=padding.MGF1(algorithm=hashes.SHA256()),
        		algorithm=hashes.SHA256(),
        		label=None)
		)
        self.request.sendall(decryptedSymmetricKey)
        
if __name__ == "__main__":
    HOST, PORT = "", 8000

    tcpServer =  socketserver.TCPServer((HOST, PORT), ClientHandler)
    try:
        tcpServer.serve_forever()
    except: 
        print("There was an error")
