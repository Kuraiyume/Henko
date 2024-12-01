#!/usr/bin/env python3

import subprocess
import string
import random
import re
import argparse
import os

banner = r"""
 __    __                      __
/  |  /  |                    /  |
$$ |  $$ |  ______   _______  $$ |   __   ______
$$ |__$$ | /      \ /       \ $$ |  /  | /      \
$$    $$ |/$$$$$$  |$$$$$$$  |$$ |_/$$/ /$$$$$$  |
$$$$$$$$ |$$    $$ |$$ |  $$ |$$   $$<  $$ |  $$ |
$$ |  $$ |$$$$$$$$/ $$ |  $$ |$$$$$$  \ $$ \__$$ |
$$ |  $$ |$$       |$$ |  $$ |$$ | $$  |$$    $$/
$$/   $$/  $$$$$$$/ $$/   $$/ $$/   $$/  $$$$$$/
                                    Kuroshiro
"""

def check_if_root():
    if os.geteuid() != 0:
        print("[-] Henko must be run as root.")
        exit()

def generate_mac():
    hex_chars = ''.join(set(string.hexdigits.upper()))
    mac_addr = ""
    for segment in range(6):
        for _ in range(2):
            if segment == 0:
                mac_addr += random.choice("02468ACE")
            else:
                mac_addr += random.choice(hex_chars)
        mac_addr += ":"
    mac_addr = mac_addr.rstrip(":")
    return mac_addr

def fetch_mac(interface):
    result = subprocess.check_output(f"ifconfig {interface}", shell=True).decode()
    return re.search("ether (.+) ", result).group().split()[1].strip()

def set_mac(interface, new_mac):
    subprocess.check_output(f"ifconfig {interface} down", shell=True)
    subprocess.check_output(f"ifconfig {interface} hw ether {new_mac}", shell=True)
    subprocess.check_output(f"ifconfig {interface} up", shell=True)

def revert_mac(interface, original_mac):
    set_mac(interface, original_mac)

def validate_mac(mac):
    if re.match(r"^[0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5}$", mac):
        return True
    elif re.match(r"^[0-9A-Fa-f]{12}$", mac):
        return True
    return False

def interface_exists(interface):
    try:
        subprocess.check_output(f"ifconfig {interface}", shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

if __name__ == "__main__":
    print(banner)
    check_if_root()
    parser = argparse.ArgumentParser(description="Henko: MAC Address Changer for Linux")
    parser.add_argument("interface", help="Network interface to modify")
    parser.add_argument("-r", "--random", action="store_true", help="Generate a random MAC address")
    parser.add_argument("-m", "--mac", help="Specify a new MAC address")
    parser.add_argument("-R", "--revert", action="store_true", help="Revert to the original MAC address")
    parser.add_argument("-b", "--backup", action="store_true", help="Backup the current MAC address before changing")
    args = parser.parse_args()
    iface = args.interface
    if not interface_exists(iface):
        print(f"[-] Network interface {iface} does not exist.")
        exit()
    if args.revert:
        try:
            with open(f"{iface}_orig_mac.txt", "r") as file:
                orig_mac = file.read().strip()
            revert_mac(iface, orig_mac)
            print(f"[+] Reverted to: {orig_mac}")
        except FileNotFoundError:
            print("[-] Original MAC Address file not found.")
        exit()
    if args.backup:
        old_mac = fetch_mac(iface)
        with open(f"{iface}_backup_mac.txt", "w") as file:
            file.write(old_mac)
        print(f"[+] Backup of current MAC address created: {old_mac}")
    old_mac = fetch_mac(iface)
    print(f"[+] Current MAC address: {old_mac}")
    with open(f"{iface}_orig_mac.txt", "w") as file:
        file.write(old_mac)
    if args.random:
        new_mac = generate_mac()
    elif args.mac:
        if not validate_mac(args.mac):
            print("[-] Invalid MAC Address format.")
            exit()
        new_mac = args.mac
    else:
        print("[-] No MAC Address specified.")
        exit()
    set_mac(iface, new_mac)
    new_mac = fetch_mac(iface)
    print(f"[+] New MAC address: {new_mac}")

