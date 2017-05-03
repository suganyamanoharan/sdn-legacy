#Author: Forum Mehta, Sourav Jain, Suganya Manoharan, Rushi Shah
#Purpose: Modules for integration with SDN and traditional network
#Date: 5/2/2017
#Version: 0.1

from flask import Flask, session
from flask import Flask ,render_template,request, redirect,url_for
import os
import time
import paramiko
import sys
from sys import stdin, stdout, stderr
from asyncio.tasks import sleep

def timest():
    return time.strftime("%X GMT", time.gmtime())           #get the current time

def sdnnodes():                                             #check nodes
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('192.168.56.10', port=22, username='mininet', password='mininet')
    ssh1 = ssh.invoke_shell()
    ssh1.send("sudo python topo.py\n")
    stdin, stdout, stderr = ssh.exec_command("sudo python parse.py\n")
    stdin.close()
    out = str(stdout.read())
    print (type(out))
    #time.sleep(2)
    output = ssh1.recv(65535)
    output = output.decode()
    ssh.close() 
    out1 = out.split("[")[1].split("]")[0]
    dpid = []
    dpid.append((out1.split(",")[0]).strip("'"))
    dpid.append((out1.split(",")[1]).split("'")[1])
    print (dpid)
    switches = []
    for i in dpid:
        switches.append("s" + i[-1])
    return (switches)

def sdn():                                                  #initial setup and ssh into SDN controller (Ryu) 
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('192.168.56.10', port=22, username='mininet', password='mininet')
        ssh1 = ssh.invoke_shell()
        ssh1.send("sudo python topo.py\n")
        stdin, stdout, stderr = ssh.exec_command("sudo python parse.py\n")
        stdin.close()
        dpid = stdout.read()
        time.sleep(2)
        output = ssh1.recv(65535)
        output = output.decode()
        ssh.close() 
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('192.168.80.10', port=22, username='sdn', password='sdn')
        ssh1 = ssh.invoke_shell()
        ssh1.send("python firewallrules1.py\n")
        ssh1.send("python firewallrules2.py\n")
        output1 = ssh1.recv(65535)
        output1 = output1.decode()
        ssh.close()        
        print(output1)
        return (dpid)
    
    
def legacy1(managementIP, devicerange, blockIP, subnet):            #initial setup and ssh into Management IP of the device and execute further configuration
        print("YES")
        devicerange = int(devicerange)
        print(timest().split(':')[2])
        subnet = subnet.split(".")
        sub0 = 255 - int(subnet[0])
        sub1 = 255 - int(subnet[1])
        sub2 = 255 - int(subnet[2])
        sub3 = 255 - int(subnet[3])
        managementIP = managementIP.split(".")
        subnet = str(sub0) + "." + str(sub1) + "." + str(sub2) + "." + str(sub3)
        for i in range(devicerange):
            manIP = int(managementIP[3]) + i
            managementIP1 = str(managementIP[0]) + "." + str(managementIP[1]) + "." + str(managementIP[2]) + "." + str(manIP)
            print(managementIP1)
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(managementIP1, port=22, username='lab', password='lab1')
            ssh1 = ssh.invoke_shell()
            ssh1.send("en\n")
            ssh1.send("lab1\n")
            ssh1.send("conf t\n")
            ssh1.send("access-list 101 deny ip any " + blockIP + " " + subnet + " \n")
            ssh1.send("do show logging \n")
            output = ssh1.recv(65535)
            output = output.decode()
            ssh.close()
        print("Sourav")
        print(timest().split(':')[2])
        print(subnet)
        print(output)