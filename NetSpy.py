#!/usr/bin/env python3

import subprocess

# Install required libraries
def install_libraries():
    try:
        subprocess.check_call(['pip', 'install', 'requests', 'dnspython'])
    except subprocess.CalledProcessError:
        print("Failed to install required libraries.")
        exit(1)

# Install required libraries before proceeding
install_libraries()

# Now import the libraries
import socket
import requests
import dns.resolver

def print_heading(heading):
    print(f"\n{'=' * len(heading)}")
    print(heading)
    print('=' * len(heading))

def ip_lookup(hostname):
    try:
        ip_address = socket.gethostbyname(hostname)
        print_heading("IP Lookup")
        print(f"The IP address of {hostname} is {ip_address}")
        get_location(ip_address)
        get_mac_address(ip_address)
        get_subdomains(hostname)
        get_dns_records(hostname)
    except socket.gaierror:
        print(f"Couldn't resolve hostname: {hostname}")

def reverse_ip_lookup(ip_address):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip_address)
        print_heading("Reverse IP Lookup")
        print(f"The hostname for IP address {ip_address} is {hostname}")
        get_location(ip_address)
        get_mac_address(ip_address)
        get_subdomains(hostname)
        get_dns_records(hostname)
    except socket.herror:
        print(f"No hostname associated with IP address: {ip_address}")

def get_location(ip_address):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        data = response.json()
        if data['status'] == 'success':
            print_heading("Location Information")
            print(f"Country: {data['country']}")
            print(f"Region: {data['regionName']}")
            print(f"City: {data['city']}")
            print(f"ISP: {data['isp']}")
        else:
            print("Failed to retrieve location information.")
    except requests.exceptions.RequestException as e:
        print("Error fetching location information:", e)

def get_mac_address(ip_address):
    # This function would typically require access to a local network to retrieve MAC address.
    # Directly obtaining MAC address from an IP address over the internet is not feasible due to network security restrictions.
    print_heading("MAC Address")
    print("MAC address: (Not available over the internet)")

def get_subdomains(hostname):
    try:
        answers = dns.resolver.resolve(hostname, 'A')
        subdomains = []
        # Collect subdomains
        for rdata in answers:
            subdomain_ip = rdata.address
            subdomains.append((hostname, subdomain_ip))

        print_heading("Subdomains")
        # Print at least 20 subdomains if available
        if len(subdomains) >= 20:
            print(f"Found {len(subdomains)} subdomains. Displaying first 20:")
            for i in range(20):
                print(f"Subdomain: {subdomains[i][0]}, IP: {subdomains[i][1]}")
        # Print all subdomains if less than 20
        else:
            print(f"Found {len(subdomains)} subdomains:")
            for subdomain, ip in subdomains:
                print(f"Subdomain: {subdomain}, IP: {ip}")

    except dns.resolver.NoAnswer:
        print("No subdomains found for", hostname)
    except dns.resolver.NXDOMAIN:
        print("Invalid domain:", hostname)
    except Exception as e:
        print("Error fetching subdomains:", e)

def get_dns_records(hostname):
    try:
        answers = dns.resolver.resolve(hostname)
        print_heading("DNS Records")
        for rdata in answers:
            print(rdata)
    except dns.resolver.NoAnswer:
        print("No DNS records found for", hostname)
    except dns.resolver.NXDOMAIN:
        print("Invalid domain:", hostname)
    except Exception as e:
        print("Error fetching DNS records:", e)

def main():
    choice = input("Enter '1' for IP lookup or '2' for reverse IP lookup: ")
    if choice == '1':
        target = input("Enter the hostname or IP address to look up: ")
        ip_lookup(target)
    elif choice == '2':
        target = input("Enter the IP address to perform reverse lookup: ")
        reverse_ip_lookup(target)
    else:
        print("Invalid choice. Please enter '1' or '2'.")

if __name__ == "__main__":
    main()
