from ip2geotools.databases.noncommercial import DbIpCity
import ipaddress
import json
from consts import *

AWS_CIDR_LIST=[]





""" Rule data structure

{
        "rule_name":name of the rule",
        "protocol":"TCP or UDP",
        "from_port":80,// the port on which request arrives
        "cidr_blocks":"", // cidr block or IP address
        "ipv6_cidr_blocks":"", 
}


"""

ingress_rule=[
    {   "rule_name":"",
        "protocol":"TCP",
        "from_port":80,
        "ip_address": "191.23.24.3",
        "cidr_blocks":"",
        "ipv6_cidr_blocks":"",
    }
]




def get_location_from_ip(ip):
    try:
        response = DbIpCity.get(ip, api_key='free')
        return response
    except Exception as e:
        print("Error:", e)
        return None


def parse_aws_cidrs():

    cidr_list=[]
    all_cidr_string=open("aws-ip-range.json", "r").read()
    cidr_json=json.loads(all_cidr_string)

    for item in cidr_json["prefixes"]:
        cidr_list.append(item["ip_prefix"])
    AWS_CIDR_LIST=cidr_list
    print(len(cidr_list))


def check_aws_ip(ip):

    client_ip=ipaddress.ip_address(ip)

    for cidr in AWS_CIDR_LIST:
        if client_ip in ipaddress.ip_network(cidr):
            return True

    return False

def check_azure_ip(ip):
    return None

def check_google_ip(ip):
    return None



def construct_http_response(status_code, status_text, body):
    response = f"HTTP/1.1 {status_code} {status_text}\r\n"
    response += "Content-Type: text/plain\r\n"
    response += f"Content-Length: {len(body)}\r\n"
    response += "\r\n"
    response += body
    return response