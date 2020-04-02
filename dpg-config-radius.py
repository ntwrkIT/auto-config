#! /usr/bin/env python

from netmiko import ConnectHandler
from netmiko import Netmiko
from getpass import getpass
from datetime import datetime


"""
# connection handler to device
net_connect = Netmiko('10.200.0.149', username=input("Username:"),
                      password=getpass(), device_type='cisco_ios')

print(net_connect.find_prompt())

# collect configuration commands
print("Which commands do you want to push? (finish with STOP)")
commands = []
command = ""

while command != "STOP":
    command = input("config#:")
    commands.append(command)

# verify commands to be executed and send configuration
print(commands)
configure = input("Is this correct? y/n: ")

if configure == "y":
    output = net_connect.send_config_set(commands)
    print(output)
    net_connect.disconnect()
else:
    print("Configuration aborted.")
    net_connect.disconnect()
"""


def readCommands(commandFile):
    # function that reads a command TXT file into a python dict
    print("Importing commands...")
    print("...\n...\n...")

    with open(commandFile, 'r') as inputFile:
        commands = inputFile.read().splitlines()

    print("These commands will be pushed")
    for rule in commands:
        print(rule)

    return commands


def readHosts(hostFile):
    # function that reads a host TXT file into a python list
    print("Reading hostfile...")
    print("...\n...\n...")

    with open(hostFile, 'r') as inputFile:
        hosts = inputFile.read().splitlines()

    print("These hosts will be modified")
    for rule in hosts:
        print(rule)

    return hosts


def configureHost(hosts, commands):
    # configures host with specific commands
    print("...\n...\n...")

    # connection handler to device
    user = input("Username: ")
    pswd = getpass()

    timestr = datetime.now().strftime("%Y%m%d-%H%M%S")
    logName = timestr + ".log"
    logFile = open(logName, 'w')

    result = {"hosts": "Succes/Failed"}

    for host in hosts:
        print("configuring " + host)
        try:
            net_connect = Netmiko(host, username=user, password=pswd,
                                  device_type='cisco_ios')
            output = net_connect.send_config_set(commands)
            print(output)
            logFile.write(output)
            net_connect.disconnect()
            result[host] = "Success"
        except:
            result[host] = "Failed"
            continue

    for r in result:
        logFile.write(r + ": " + result[r] + "\n")

    logFile.close()


if __name__ == "__main__":
    print("Welcome to the automated device configurator")
    print("...\n...\n...")

    commandFile = input("Your commands filename: ")
    print("...\n...\n...")
    config = readCommands(commandFile)
    print("...\n...\n...")
    hostFile = input("Your host filename: ")
    print("...\n...\n...")
    devices = readHosts(hostFile)
    print("...\n...\n...")

    configureHost(devices, config)
    pass
