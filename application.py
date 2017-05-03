from flask import Flask, session
from flask import Flask ,render_template,request, redirect,url_for
import os
import time
import paramiko
import sys
from sys import stdin, stdout, stderr
from asyncio.tasks import sleep
from integration import sdn ,legacy1, sdnnodes


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selectedValue = request.form['type']
        if(selectedValue) == 'legacy':
            return redirect(url_for('legacy'))
        elif(selectedValue) == 'sdn':
            out = str(sdn())
            print (out)
            return redirect(url_for('sdnf', dpid=out))
        elif (selectedValue) == 'check_nodes':
            switches = sdnnodes()
            return redirect(url_for('nodes', switches=switches))
        else:
            return render_template('cap.html')
    return render_template('cap.html')



@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/cap')
def cap():
    return render_template('cap.html')

        
@app.route('/legacy', methods=['GET', 'POST'])
def legacy():
    if request.method == 'POST':
        #if selectedValue == "legacy":
            managementIP = request.form['managementIP']
            devicerange = request.form['devicerange']
            protocol = request.form['protocol']
            permission = request.form['permission']
            port = request.form['port_no']
            sourceIP = request.form['sourceIP']
            subnet1 = request.form['subnet1']
            destinationIP = request.form['destinationIP']
            subnet2 = request.form['subnet2']
            print(managementIP)
            legacy1(managementIP, devicerange, destinationIP, subnet2)
            return("Configuration successful" )
    return render_template('legacy.html')
    
@app.route('/sdn', methods=['GET', 'POST'])
def sdnf():
    if request.args.get('dpid'):
        print ("Got the dpid")
        out = request.args.get('dpid')
        out1 = out.split("[")[1].split("]")[0]
        dpid = []
        dpid.append((out1.split(",")[0]).strip("'"))
        dpid.append((out1.split(",")[1]).split("'")[1])
        print(dpid)
        print (type(dpid))
        return render_template('sdn.html', dpid=dpid)
    elif request.form['dpid']:
        dpid = request.form['dpid']
        protocol = request.form['protocol']
        Action = request.form['Action']
        print (Action)
        IP = request.form['IP']
        subnet3 = request.form['subnet3']
        if (dpid != "ALL"):
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('192.168.80.10', port=22, username='sdn', password='sdn')
            ssh1 = ssh.invoke_shell()
            ssh1.send("curl -X POST -d "+"'"+"{\"nw_src\": " +"\""+str(IP)+"/32"+"\""+",  \"nw_proto\": "+"\""+ str(protocol)+"\""+", \"action\": "+ "\""+str(Action)+"\""+"}"+"'"+"  http://localhost:8080/firewall/rules/"+ str(dpid)+"\n")
            output = ssh1.recv(65535)
            output = output.decode()
            print (output)
            ssh.close()     
            return ("Configuration success")
        else:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('192.168.80.10', port=22, username='sdn', password='sdn')
            ssh1 = ssh.invoke_shell()
            ssh1.send("curl -X POST -d "+"'"+"{\"nw_src\": " +"\""+str(IP)+"/32"+"\""+",  \"nw_proto\": "+"\""+ str(protocol)+"\""+", \"action\": "+ "\""+str(Action)+"\""+"}"+"'"+"  http://localhost:8080/firewall/rules/"+ str(dpid)+"\n")
            output = ssh1.recv(65535)
            output = output.decode()
            print (output)
            ssh.close()     
            return ("Configuration success")
        
@app.route('/nodes', methods=['GET', 'POST'])
def nodes():
    if request.args.get('switches'):
        out = request.args.get('switches')
        out = []
        out.append("s1")
        out.append("s2")
        print (out)
        return render_template('nodes.html',dpid=out)
#        out1 = out.split("[")[1].split("]")[0]
#        dpid = []
#        dpid.append((out1.split(",")[0]).strip("'"))
#        dpid.append((out1.split(",")[1]).split("'")[1])
#        print(dpid)
#        print (type(dpid))
#        return render_template('sdn.html', dpid=dpid)
    elif request.form['dpid']:
        value = request.form['dpid']
        print (value)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('192.168.56.10', port=22, username='mininet', password='mininet')
        ssh1 = ssh.invoke_shell()
        ssh1.send("sudo ovs-dpctl show s1")
        print (stdout)
        print (stderr)
        output = ssh1.recv(65535)
        output = output.decode()
        print (output)
        ssh.close()
        return(stdout)    
    else:
        return ("not working")
#    ssh = paramiko.SSHClient()
#    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#    ssh.connect('192.168.56.10', port=22, username='mininet', password='mininet')
#    ssh1 = ssh.invoke_shell()
#    ssh1.send("sudo python topo.py\n")
#    stdin, stdout, stderr = ssh.exec_command("sudo python parse.py\n")
#    stdin.close()
#    out = str(stdout.read())
#    print (type(out))
#    #time.sleep(2)
#    output = ssh1.recv(65535)
#    output = output.decode()
#    ssh.close() 
#    out1 = out.split("[")[1].split("]")[0]
#    dpid = []
#    dpid.append((out1.split(",")[0]).strip("'"))
#    dpid.append((out1.split(",")[1]).split("'")[1])
#    print (dpid)
#    switches = []
#    for i in dpid:
#        switches.append("s" + i[-1])
    
#
#@app.route('/nodes', methods=['GET', 'POST'])
#def nodes():
#    if request.method == "POST":
#        value = request.form['type']
#        ssh = paramiko.SSHClient()
#        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#        ssh.connect('192.168.56.10', port=22, username='mininet', password='mininet')
#        ssh1 = ssh.invoke_shell()
#        stdin, stdout, stderr = ssh.exec_command("ovs-dpctl show")
#        print (stdout)
#        print (stderr)
#        output = ssh1.recv(65535)
#        output = output.decode()
#        #print (output)
#        ssh.close()
#        return(stdout)
#    
#   
#    


if __name__=="__main__":
    
    app.debug = True
    app.run(host='127.0.0.1',port=443)
