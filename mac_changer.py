#!/usr/bin/env python

import subprocess
import optparse
import re

def get_args():
    parser = optparse.OptionParser()

    parser.add_option("-i","--interface", dest = "interface",help="Interface to change MAC Address")
    parser.add_option("-m","--mac", dest = "new_mac",help="New MAC Address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please enter an interface. Use --help for more information")
    if not options.new_mac:
        parser.error("[-] Please enter an new MAC address. Use --help for more information")
    return options

def change_mac(interface, new_mac):
    message = "[+] Changing MAC address for "+ interface + " to " + new_mac

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig",interface,"hw","ether", new_mac])
    subprocess.call(["ifconfig",interface,"up"])

    print(message)

def get_new_mac(interface):
    ifconfig_results = subprocess.check_output(["ifconfig",options.interface])
    mac_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",ifconfig_results)
    if mac_search_result:
        return mac_search_result.group(0)
    else:
        print("[-] MAC address could not be read")

options = get_args()

current_mac = get_new_mac(options.interface)
print("Current MAC address: "+ str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_new_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address has been successfully changed to " + current_mac)
else:
    print("[-] MAC address could not be changed")