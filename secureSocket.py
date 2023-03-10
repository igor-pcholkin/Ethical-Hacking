import socket
import ssl

client_key = '/home/kali/client.key'
client_cert = '/home/kali/client.crt'
server_cert = '/home/kali/server.crt'
port = 8080
hostname = '192.168.1.101'
context = ssl.SSLContext(ssl.PROTOCOL_TLS, cafile=server_cert)
context.load_cert_chain(certfile=client_cert, keyfile=client_key)
context.load_verify_locations(cafile=server_cert)
context.verify_mode=ssl.CERT_REQUIRED
context.options |= ssl.OP_SINGLE_ECDH_USE
#context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2

with socket.create_connection((hostname, port)) as sock:
    with context.wrap_socket(sock, server_side=False, server_hostname=hostname) as ssock:
        print(ssock.version())
        message = input("Enter message: ")
        ssock.send(message.encode())
        receives = ssock.recv(1024)
        print(receives)
        
