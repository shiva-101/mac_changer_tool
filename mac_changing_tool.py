#!/usr/bin/env python

import subprocess
import argparse
import re
import sys


def get_arguments():
    parser = argparse.ArgumentParser(description="A script to change MAC address")
    parser.add_argument("-i", "--interface", dest="interface", help="Enter interface name.", required=True)
    parser.add_argument("-m", "--mac", dest="new_mac", help="Enter MAC address.", required=True)
    args = parser.parse_args()

    if not validate_interface(args.interface):
        parser.error("[-] Invalid interface name.")

    if not validate_mac(args.new_mac):
        parser.error("[-] Invalid MAC address format.")

    return args


def validate_interface(interface):
    # Check if the interface name is valid
    # This is a basic check, you might want to improve it based on your system requirements
    return bool(re.match(r'^[a-zA-Z0-9_]+$', interface))


def validate_mac(mac):
    # Validate the MAC address format
    return bool(re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', mac))


def change_mac(interface, new_mac):
    print(f"[+] Changing MAC Address of {interface} to {new_mac}")
    try:
        subprocess.run(["ifconfig", interface, "down"], check=True)
        subprocess.run(["ifconfig", interface, "hw", "ether", new_mac], check=True)
        subprocess.run(["ifconfig", interface, "up"], check=True)
        print("[+] MAC Address changed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[-] Failed to change MAC Address: {e}")
        sys.exit(1)


if __name__ == "__main__":
    options = get_arguments()
    change_mac(options.interface, options.new_mac)