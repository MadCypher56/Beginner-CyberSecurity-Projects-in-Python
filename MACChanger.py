#!usr/bin/env python

import subprocess
import optparse
import re

def changeMAC(interface,new_mac):
    print("Changing MAC address of ",interface, " to ",new_mac)
    subprocess.call(['ifconfig',interface,'down'])
    subprocess.call(['ifconfig',interface,'hw','ether',new_mac])
    subprocess.call(['ifconfig',interface,'up'])
    subprocess.call(['ifconfig'])

def getArguments():
    parser = optparse.OptionParser()

    parser.add_option("-i","--interface",dest="interface",help="The interface you want to change")
    parser.add_option("-m","--mac",dest="new_mac",help="New MAC address")
    (options,arguments) =  parser.parse_args()
    
    if not options.interface:
        #Exception handling
        parser.error("[-] Please specify interface")
    if not options.new_mac:
        #Exception handling    
        parser.error("[-] Please specify new MAC address")

    return options


def getCurrMAC(interface):
    ifconfigResult= subprocess.check_output(["ifconfig", interface])
    ifconfigResultString = ifconfigResult.decode('utf-8')
    MACAddSearch = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",ifconfigResultString)

    if MACAddSearch:
        return MACAddSearch.group(0)
    else:
        print("[-] MAC Address not found")

options = getArguments()

currentMAC = getCurrMAC(options.interface)
print("Current MAC: ",str(currentMAC) )

changeMAC(options.interface,options.new_mac)

currentMAC=  getCurrMAC(options.interface)
if currentMAC == options.new_mac:
    print("[-] MAC Address Changed Sucessfully")
else:
    print("[-] MAC address not changed")