#!/usr/bin/env python3

import subprocess
import re
import requests
from requests.auth import HTTPBasicAuth

# 🔍 Get local IP range
def get_ip_range():
    result = subprocess.getoutput("ip a")
    match = re.search(r"inet (\d+\.\d+\.\d+)\.\d+/\d+", result)
    if match:
        base_ip = match.group(1)
        return f"{base_ip}.0/24"
    else:
        raise Exception("Couldn't detect local IP range")

# 🔎 Run Nmap ping scan
def scan_hosts(ip_range):
    print(f"[+] Scanning network range {ip_range}...")
    result = subprocess.getoutput(f"sudo nmap -sn {ip_range}")
    ips = re.findall(r"Nmap scan report for (\d+\.\d+\.\d+\.\d+)", result)
    return ips

# 📷 Try default creds on discovered IPs
def check_cameras(ips):
    default_creds = [
        ("admin", "admin"),
        ("admin", "password"),
        ("admin", ""),
        ("root", "root"),
    ]

    for ip in ips:
        url = f"http://{ip}"
        try:
            print(f"[*] Checking {url}...")
            for user, pwd in default_creds:
                response = requests.get(url, auth=HTTPBasicAuth(user, pwd), timeout=3)
                if response.status_code == 200:
                    print(f"[!] Exposed Camera Found: {url} with creds {user}/{pwd}")
                    break
        except:
            continue

# 🧠 Main
if __name__ == "__main__":
    ip_range = get_ip_range()
    live_hosts = scan_hosts(ip_range)
    check_cameras(live_hosts)
