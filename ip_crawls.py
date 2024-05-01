

import requests
import schedule
LATEST_MALWARE_IPS=[]
VPN_IP_LIST=[]
CLOUDFLARE_IP_LIST=[]

FEEDOTRACKER_URL="https://feodotracker.abuse.ch/downloads/ipblocklist_recommended.json"

VPN_IP_URL="https://raw.githubusercontent.com/X4BNet/lists_vpn/main/ipv4.txt";

CLOUDFLARE_IPS_URL="https://api.cloudflare.com/client/v4/ips"



def get_feedotracker_malware_ips():
    response=requests.get(FEEDOTRACKER_URL)
    data=response.json()
    ip_list=[]
    # print(data)
    for item in data:
        ip_list.append(item["ip_address"])
    LATEST_MALWARE_IPS=ip_list
    print(f"[INFO] Updated malware IPs list is: {LATEST_MALWARE_IPS}")


    print(LATEST_MALWARE_IPS)



def update_botnet_ips():
    schedule.every().hour.do(get_feedotracker_malware_ips)



def get_vpn_ips():
    try:
        response=requests.get(VPN_IP_URL)
        data=response.text
        ip_list=data.split("\n")
        
        VPN_IP_LIST=ip_list
        print(f"[INFO] Updated VPN IPs list is: {VPN_IP_LIST}")
        
    except Exception as e:
        print(f"[ERROR] Error in fetching VPN IPs list: {e}")
        return None


def get_latest_vpn_ips():
    schedule.every().day.do(get_vpn_ips)


def get_cloudflare_ips():
    data = requests.get(CLOUDFLARE_IPS_URL).json()
    print(data)
    CLOUDFLARE_IP_LIST= data['result']['ipv4_cidrs']

def get_latest_cloudflare_ips():
    schedule.every().day.do(get_cloudflare_ips)