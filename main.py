
import socket
import threading
from utils import *
from consts import *
import argparse
from ip_crawls import *


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

    

def geo_location_allowed(ip):
    location=get_location_from_ip(ip)
    print(location)
    country=location.country
    state=location.region
    city=location.city

    if country.lower() in BLOCKED_COUNTRY_LIST:
        print(f"[INFO] Blocking request from {ip} whose country is: {country}")
        return False
    elif state.lower() in BLOCKED_STATE_LIST:
        print(f"[INFO] Blocking request from {ip} whose state is: {state}")
        return False
    elif city.lower() in BLOCKED_CITY_LIST:
        print(f"[INFO] Blocking request from {ip} whose city is: {city}")
        return False

    return True

def forward_request(request, port):
    
    try:
        destination_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        destination_socket.connect(('localhost', port))

        destination_socket.sendall(request)
        # Receive the response from localhost:8080
        response = destination_socket.recv(8192)

        # print("[RESPONSE] Received response from localhost:8080:", response)
        # Close the socket to localhost:8080
        destination_socket.close()

        return response
    
    except Exception as e:

        print("[ERROR]  `Error while forwarding request:", e)
        return None

def handle_client(client_socket, client_address, forward_port):
    request = client_socket.recv(8192)

    #  clinet addressed is a typle of (ip, port)
    ip=client_address[0]
    print("[INFO] Accepted connection from:", client_address)
    print(f"[INFO] Client address: {client_address}")
    print("[INFO] Received request from client:", request)

    if not geo_location_allowed(ip):
        reject_request(client_socket)

    # check if the client ip is in malware list
    if ip in LATEST_MALWARE_IPS:
        print(f"[INFO] Blocking request from malware IP: {ip}")
        reject_request(client_socket)



    if BLOCK_RULES["BLOCK_AWS"]:
        is_aws_ip= check_aws_ip(ip)
        if is_aws_ip:
            print(f"[INFO] Blocking request from AWS IP: {ip}")
            reject_request(client_socket)


    if BLOCK_RULES["BLOCK_CLOUDFLARE"]:
       if ip in CLOUDFLARE_IP_LIST:
              print(f"[INFO] Blocking request from Cloudflare IP: {ip}")
              reject_request(client_socket)


    #### if all rejection rules are passed, forward the request to localhost:8080 or specific port
    response= forward_request(request, forward_port)

    ### if response is received from the forwared request, send it back to the client
    if(response):
        print("\n\n [RESPONSE] Received response from localhost:8080:", response)
        client_socket.sendall(response)
        client_socket.close()


def start_proxy(port, forward_port=8080):
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
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, forward_port))
        client_thread.start()
        # handle_client(client_socket, client_address)

def parse_args():
    parser = argparse.ArgumentParser(description="My Python Script")

    parser.add_argument("-p", "--port", type=int, default=80, help="Port number")
    parser.add_argument("-f", "--forward", type=int, default=8080, help="Forward port number")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()

    get_latest_vpn_ips()
    update_botnet_ips()
    get_latest_cloudflare_ips()

    start_proxy(port=args.port, forward_port=args.forward)