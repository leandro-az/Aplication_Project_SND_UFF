#!/usr/bin/python

import time
from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch, RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.topo import Topo
from threading import Thread
import os
import sys





def myController(): 

    net = Mininet(controller=RemoteController, switch=OVSKernelSwitch)

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

    net.start()
    print "*** Testing the connection between hosts "
    net.staticArp()
    #net.pingAllFull()

    

    def cleanArqs():
        os.system("rm /home/leandroall/logsminet/logReceiverMain.log &")
        os.system("rm /home/leandroall/logsminet/logSenderMain.log &")
        os.system("rm /home/leandroall/logsminet/logmininet.log &")
        for i in range(len(ListHostS1)):
            os.system(("rm /home/leandroall/logsminet/sendermininet" +str(i)+ ".log &"))

    def startReceiver():
        h69=net.get('h69')
        h69.waiting = False
        h69.cmd("> /home/leandroall/logsminet/logmininet.log")
        h69.cmd("/home/leandroall/D-ITG-2.8.1-r1023/bin/ITGRecv &" )

    def startSender():
        #time.sleep(6)
        for i in range(len(ListHostS1)):
          ListHostS1[i].waiting = False	
          ListHostS1[i].cmd(("> /home/leandroall/logsminet/sendermininet"+str(i)+".log"))
          ListHostS1[i].cmd(("/home/leandroall/D-ITG-2.8.1-r1023/bin/ITGSend -a 10.0.0.69 -C 1000 -c 40 -T UDP -t 3000000 -l /home/leandroall/logsminet/sendermininet" +str(i)+ ".log -x /home/leandroall/logsminet/logmininet.log &"))
        
    def startMainReceiver():
        h68=net.get('h68')
        h68.waiting = False
        h68.cmd("> /home/leandroall/logsminet/logReceiverMain.log &")
        h68.cmd("/home/leandroall/D-ITG-2.8.1-r1023/bin/ITGRecv &" )

    def startMainSender():
        h21=net.get('h21')
        h21.waiting = False
        h21.cmd(("> /home/leandroall/logsminet/logSenderMain.log &"))
        h21.cmd(("/home/leandroall/D-ITG-2.8.1-r1023/bin/ITGSend  -a 10.0.0.68 -C 1000 -c 512 -T UDP -t 3000000 -l /home/leandroall/logsminet/logSenderMain.log -x /home/leandroall/logsminet/logReceiverMain.log &"))   
 
    #Perda boa: -a 10.0.0.69 -C 1000 -c 512 -T UDP -t 300000
    
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
