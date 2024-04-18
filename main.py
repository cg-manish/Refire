import json
import socket
import threading
from utils import *
import argparse


def reject_request(client_socket):


    body=json.dumps({"error": "Forbidden", 
                     "message": "You are not allowed to access this resource",
                     "statusCode": 403})
    
    length=len(body)
    response = "HTTP/1.1 403 Forbidden\r\n"
    response += f"Content-Length: " + f"{length}"+"\r\n"
    response += "Connection: close\r\n"
    response += "\r\n"
    response += body

    client_socket.sendall(response.encode())
    client_socket.close()

    
def handle_client(client_socket, client_address):
    request = client_socket.recv(4096)
    print("[INFO] Accepted connection from:", client_address)
    print(f"[INFO] Client address: {client_address}")
    print("[INFO] Received request from client:", request)

    # country_allowed(client_address[0])
    # reject_request(client_socket)

    if not country_allowed:
      reject_request(client_socket)

    if BLOCK_RULES["BLOCK_AWS"]:
        is_aws_ip= check_aws_ip(client_address[0])

    if is_aws_ip:
        print(f"[INFO] Blocking request from AWS IP: {client_address[0]}")
        reject_request(client_socket)


    response= forward_request(request, 8080)

    if(response):
        print("[RESPONSE] Received response from localhost:8080:", response)
        client_socket.sendall(response)
        client_socket.close()

def country_allowed(ip):
    country= get_country_from_ip(ip)

    if country in blocked_country_list:
        print(f"[INFO] Blocking request from {ip} whose country is: {country}")
        return False
    return True


def forward_request(request, port):
    
    try:
        destination_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        destination_socket.connect(('localhost', port))

        destination_socket.sendall(request)
        # Receive the response from localhost:8080
        response = destination_socket.recv(4096)

        # print("[RESPONSE] Received response from localhost:8080:", response)
        # Close the socket to localhost:8080
        destination_socket.close()

        return response
    
    except Exception as e:

        print("[ERROR]  `Error while forwarding request:", e)
        return None


def start_proxy(port):
    # Create a socket object, AF_INET for IPv4, SOCK_STREAM for TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to port 80
    server_socket.bind(('0.0.0.0', port))
    
    # Listen for incoming connections , quueue up to 5
    server_socket.listen(100)
    
    print(f"[INFO] Proxy server started on port {port}")
    
    while True:
        # Accept incoming client connections
        client_socket, client_address = server_socket.accept()
        print("\n [INFO] Accepted connection from:", client_address)
        
        # Start a new thread to handle the client request
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()
        # handle_client(client_socket, client_address)

def parse_args():
    parser = argparse.ArgumentParser(description="My Python Script")
    parser.add_argument("-p", "--port", type=int, default=80, help="Port number")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()

    start_proxy(port=args.port)
