#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch, RemoteController, OVSKernelSwitch,OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.topo import Topo
from mininet.link import Link, TCLink
from threading import Thread
import os
import subprocess
import sys





timeToSend=300000

def myController(): 

    net = Mininet(controller=RemoteController, switch=OVSSwitch)

    print "*** Creating the reference to controller"

    c1 = net.addController('c1', controller=RemoteController, ip="127.0.0.1", port=6633)

    print "*** Creating switches"
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')
    s5 = net.addSwitch('s5')

    print "*** Creating hosts"

    ListHostS1=[]
    for i in range (1,20):
        ListHostS1.append(net.addHost('h'+str(i),ip=('10.0.0.'+str(i))))

    ListHostS2 = []
    for i in range(21, 40):
        ListHostS2.append(net.addHost('h' + str(i), ip=('10.0.0.' + str(i))))

    ListHostS3 = []
    for i in range(41, 60):
        ListHostS3.append(net.addHost('h' + str(i), ip=('10.0.0.' + str(i))))

    ListHostS5 = []
    for i in range(61, 70):
        ListHostS5.append(net.addHost('h' + str(i), ip=('10.0.0.' + str(i))))


    #h1 = net.addHost('h1', ip='10.0.0.1')
    #h2 = net.addHost('h2', ip='10.0.0.2')
    #h3 = net.addHost('h3', ip='10.0.0.3')
    #h4 = net.addHost('h4', ip='10.0.0.4')

    print "*** Creating links"

    for i in range(len(ListHostS1)):
        s1.linkTo(ListHostS1[i])

    for i in range(len(ListHostS2)):
        s2.linkTo(ListHostS2[i])

    for i in range(len(ListHostS3)):
        s3.linkTo(ListHostS3[i])

    for i in range(len(ListHostS5)):
        s5.linkTo(ListHostS5[i])

    s4.linkTo(s5)
    s2.linkTo(s4)
    s3.linkTo(s4)
    s1.linkTo(s4)
    
   
    

    #s1.linkTo(h1)
    #s1.linkTo(h2)
    #s1.linkTo(s2)
    #s2.linkTo(h3)
    #s2.linkTo(h4)

    print "*** Starting the net"
    net.build()
    c1.start()
    s1.start([c1])
    s2.start([c1])
    s3.start([c1])
    s4.start([c1])
    s5.start([c1])

    
    #print "*** Testing the connection between hosts "
    #net.staticArp()
    def createQueue():
        os.system("ovs-vsctl -- --all destroy QoS -- --all destroy Queue")
        os.system("ovs-vsctl set port s2-eth20 qos=@newqos -- --id=@newqos create qos type=linux-htb queues=0=@q0,1=@q1 -- --id=@q0 create queue other-config:min-rate=1000000000 other-config:max-rate=100000000 -- --id=@q1 create queue other-config:min-rate=2000000 other-config:max-rate=2000000")
        os.system("ovs-ofctl add-flow s2 \"priority=65535,in_port=1,actions=enqueue:20:0\"")
        for i in range(2,20):
            os.system("ovs-ofctl add-flow s2 \"priority=65535, in_port="+str(i)+",actions=enqueue:20:1\"")

        os.system("ovs-vsctl set port s4-eth3 qos=@newqos -- --id=@newqos create qos type=linux-htb queues=0=@q0,1=@q1 -- --id=@q0 create queue other-config:min-rate=1000000000 other-config:max-rate=100000000 -- --id=@q1 create queue other-config:min-rate=2000000 other-config:max-rate=2000000")
        os.system("ovs-ofctl add-flow s4 \"priority=65535,nw_src=10.0.0.21,actions=enqueue:3:0\"")
        for i in range(22,40):
           os.system("ovs-ofctl add-flow s4 \"priority=65535,nw_src=10.0.0."+str(i)+",actions=enqueue:3:1\"")

     
    net.start()
    #net.pingAllFull()

    

    def cleanArqs():
        os.system("rm /home/leandroall/logsminet/logReceiverMain.log &")
        os.system("rm /home/leandroall/logsminet/logSenderMain.log &")
        os.system("rm /home/leandroall/logsminet/logmininet.log")
        for i in range(len(ListHostS2)):
            os.system(("rm /home/leandroall/logsminet/sendermininet" +str(i)+ ".log &"))

    def startReceiver():
        for i in range(len(ListHostS3)):
             hS3=net.get(ListHostS3[i].name)
             hS3.waiting = False
             hS3.cmd("> /home/leandroall/logsminet/logmininet.log")
             hS3.cmd("/home/leandroall/D-ITG-2.8.1-r1023/bin/ITGRecv &" )

    def startSender():
        #time.sleep(6)
        for i in range(len(ListHostS2)):
          ListHostS2[i].waiting = False	
          ListHostS2[i].cmd(("> /home/leandroall/logsminet/sendermininet"+str(i)+".log"))
          #Enviando para S3
          ListHostS2[i].cmd(("/home/leandroall/D-ITG-2.8.1-r1023/bin/ITGSend -a 10.0.0."+str(41+i)+" -T TCP -E 167 -c 1500 -t 3000000 -l /home/leandroall/logsminet/sendermininet" +str(i)+ ".log -x /home/leandroall/logsminet/logmininet.log &"))
          
    def startMainReceiver():
        h68=net.get('h68')
        h68.waiting = False
        h68.cmd("> /home/leandroall/logsminet/logReceiverMain.log &")
        h68.cmd("/home/leandroall/D-ITG-2.8.1-r1023/bin/ITGRecv &" )

    def startMainSender():
        h2=net.get('h2')
        h2.waiting = False
        h2.cmd(("> /home/leandroall/logsminet/logSenderMain.log &"))
        h2.cmd(("/home/leandroall/D-ITG-2.8.1-r1023/bin/ITGSend  -a 10.0.0.68 -T UDP -E 15 -u 78 2718 -t 3000000 -l /home/leandroall/logsminet/logSenderMain.log -x /home/leandroall/logsminet/logReceiverMain.log &"))   
 
    #Perda boa: -a 10.0.0.69 -C 1000 -c 512 -T UDP -t 300000

    print "*** Set conf to QOS "

    createQueue()

    #os.system("curl -X POST -H \"content-type:application/json\" http://localhost:8181/onos/v1/flows -d @/home/leandroall/onosPriorityS2.json  --user onos:rocks")
    #os.system("curl -X POST -H \"content-type:application/json\" http://localhost:8181/onos/v1/flows -d @/home/leandroall/onosPriorityS3.json  --user onos:rocks")
   # os.system("curl -X POST -H \"content-type:application/json\" http://localhost:8181/onos/v1/flows -d @/home/leandroall/onosPriorityS4.json  --user onos:rocks")
   
    
    #os.system("curl -X POST -H \"content-type:application/json\" http://localhost:8181/onos/v1/flows -d @/home/leandroall/queueImpl.json  --user onos:rocks")
    #Espera 5min
    #wipe-out please  -- comando para lmpar o onos
    

    print "*** Clearing All Files "
    
    cleanArqs()

    print "*** Start Regular Receiver to Listen"

    startReceiver()  

    print "*** Starting Regular Sends"
    
    startSender()

    print "*** Start the Main Receiver to Listen"

    startMainReceiver()
    
    print "*** Start the Main Sender"
    
    startMainSender()
    
    print "*** Waiting the process finish"
    
    CLI(net)



if __name__ == '__main__':
    setLogLevel('info')  # for CLI output
    myController()
