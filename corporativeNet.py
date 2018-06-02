#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch, RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.topo import Topo
from mininet.link import Link, TCLink
import os
import json




NHostS1=61
NHostS2=121
NHostS3=181
NHostS5=241
Pref=61

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
    for i in range (1,NHostS1):
        ListHostS1.append(net.addHost('h'+str(i),ip=('10.0.0.'+str(i))))

    ListHostS2 = []
    for i in range(NHostS1, NHostS2):
        ListHostS2.append(net.addHost('h' + str(i), ip=('10.0.0.' + str(i))))

    ListHostS3 = []
    for i in range(NHostS2, NHostS3):
        ListHostS3.append(net.addHost('h' + str(i), ip=('10.0.0.' + str(i))))

    ListHostS5 = []
    for i in range(NHostS3, NHostS5):
        ListHostS5.append(net.addHost('h' + str(i), ip=('10.0.0.' + str(i))))

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
    #print "*** Testing the connection between hosts "
    #net.staticArp()

    #net.pingAllFull()

    def createJsonRule():
        os.system("> /home/leandroall/logsminet/jsonRule.json")
        data = {}  
        data['flows'] = [] 
        for i in range(NHostS1, NHostS2): 
            if ( i == Pref) :
                data['flows'].append({
                                      "priority": 65535,
                                      "timeout": 1800,
                                      "isPermanent": True,
                                      "deviceId": "of:0000000000000002",
                                      "cleared": True,
                                      "treatment": {
                                        "instructions": [
                                          {
                                            "type": "QUEUE",
                                            "queueId":0
                                          },
                                          {
                                            "type": "OUTPUT",
                                            "port":61
                                          }
                                        ]
                                      },
                                      "selector": {
                                        "criteria": [
                                          {
                                            "type": "IPV4_SRC",
                                            "ip": "10.0.0."+str(i)+"/32"
                                          },
                                          {
                                            "type": "ETH_TYPE",
                                            "ethType": "0x0800"
                                          }
                                        ]
                                      }
                                    })
            else:
                 data['flows'].append({
                                      "priority": 65535,
                                      "timeout": 1800,
                                      "isPermanent": True,
                                      "deviceId": "of:0000000000000002",
                                      "cleared": True,
                                      "treatment": {
                                        "instructions": [
                                          {
                                            "type": "QUEUE",
                                            "queueId":1
                                          },
                                          {
                                            "type": "OUTPUT",
                                            "port":61
                                          }
                                        ]
                                      },
                                      "selector": {
                                        "criteria": [
                                          {
                                            "type": "IPV4_SRC",
                                            "ip": "10.0.0."+str(i)+"/32"
                                          },
                                          {
                                            "type": "ETH_TYPE",
                                            "ethType": "0x0800"
                                          }
                                        ]
                                      }
                                    })
        for i in range(NHostS1, NHostS2): 
            if ( i == Pref) :
                data['flows'].append({
                                      "priority": 65535,
                                      "timeout": 1800,
                                      "isPermanent": True,
                                      "deviceId": "of:0000000000000004",
                                      "cleared": True,
                                      "treatment": {
                                        "instructions": [
                                          {
                                            "type": "QUEUE",
                                            "queueId":0
                                          },
                                          {
                                            "type": "OUTPUT",
                                            "port":1
                                          }
                                        ]
                                      },
                                      "selector": {
                                        "criteria": [
                                          {
                                            "type": "IPV4_SRC",
                                            "ip": "10.0.0."+str(i)+"/32"
                                          },
                                          {
                                            "type": "ETH_TYPE",
                                            "ethType": "0x0800"
                                          }
                                        ]
                                      }
                                    })
            else:
                 data['flows'].append({
                                      "priority": 65535,
                                      "timeout": 1800,
                                      "isPermanent": True,
                                      "deviceId": "of:0000000000000004",
                                      "cleared": True,
                                      "treatment": {
                                        "instructions": [
                                          {
                                            "type": "QUEUE",
                                            "queueId":1
                                          },
                                          {
                                            "type": "OUTPUT",
                                            "port":1
                                          }
                                        ]
                                      },
                                      "selector": {
                                        "criteria": [
                                          {
                                            "type": "IPV4_SRC",
                                            "ip": "10.0.0."+str(i)+"/32"
                                          },
                                          {
                                            "type": "ETH_TYPE",
                                            "ethType": "0x0800"
                                          }
                                        ]
                                      }
                                    }) 
        data['flows'].append({
                                      "priority": 45535,
                                      "timeout": 1800,
                                      "isPermanent": True,
                                      "deviceId": "of:0000000000000004",
                                      "cleared": True,
                                      "treatment": {
                                        "instructions": [
                                          {
                                            "type": "QUEUE",
                                            "queueId":1
                                          },
                                          {
                                            "type": "OUTPUT",
                                            "port":3
                                          }
                                        ]
                                      },
                                      "selector": {
                                        "criteria": [
                                          {
                                            "type": "IN_PORT",
                                            "port": 4
                                          },
                                          {
                                            "type": "ETH_TYPE",
                                            "ethType": "0x0800"
                                          }
                                        ]
                                      }
                                    })                                                          


        with open('/home/leandroall/logsminet/jsonRule.json', 'w') as outfile:  
           json.dump(data, outfile)
       


    def createQueue():
        os.system("ovs-vsctl -- --all destroy QoS -- --all destroy Queue")
        os.system("ovs-vsctl set port s2-eth61 qos=@newqos -- --id=@newqos create qos type=linux-htb queues=0=@q0,1=@q1 -- --id=@q0 create queue other-config:priority=1  other-config:min-rate=1000000000 other-config:max-rate=100000000 -- --id=@q1 create queue other-config:priority=2 other-config:min-rate=100000000 other-config:max-rate=100000000")
        #os.system("ovs-ofctl add-flow s2 \"priority=65535,dl_type=0x0800,nw_src=10.0.0.21,actions=enqueue:20:0\"")
        #for i in range(22,40):
           # os.system("ovs-ofctl add-flow s2 \"priority=65535,dl_type=0x0800,nw_src=10.0.0."+str(i)+",actions=enqueue:20:1\"")

        os.system("ovs-vsctl set port s4-eth1 qos=@newqos -- --id=@newqos create qos type=linux-htb queues=0=@q0,1=@q1 -- --id=@q0 create queue other-config:priority=1  other-config:min-rate=1000000000 other-config:max-rate=100000000 -- --id=@q1 create queue other-config:priority=2  other-config:min-rate=100000000 other-config:max-rate=100000000")
        os.system("ovs-vsctl set port s4-eth3 qos=@newqos -- --id=@newqos create qos type=linux-htb queues=0=@q0,1=@q1 -- --id=@q0 create queue other-config:priority=1  other-config:min-rate=1000000000 other-config:max-rate=100000000 -- --id=@q1 create queue other-config:priority=2  other-config:min-rate=100000000 other-config:max-rate=100000000")
        #os.system("ovs-ofctl add-flow s4 \"priority=65535,dl_type=0x0800,nw_src=10.0.0.21,actions=enqueue:3:0\"")
        #for i in range(22,40):
          # os.system("ovs-ofctl add-flow s4 \"priority=65535,dl_type=0x0800,nw_src=10.0.0."+str(i)+",actions=enqueue:3:1\"")

        #os.system("curl -X POST -H \"content-type:application/json\" http://localhost:8181/onos/v1/flows -d @/home/leandroall/onosPriorityS2.json  --user onos:rocks")
        
        #os.system("curl -X POST -H \"content-type:application/json\" http://localhost:8181/onos/v1/flows -d @/home/leandroall/onosPriorityS4.json  --user onos:rocks")  

        os.system("curl -X POST -H \"content-type:application/json\" http://localhost:8181/onos/v1/flows -d @/home/leandroall/logsminet/jsonRule.json  --user onos:rocks")
    
    

    

    def cleanArqs():
        os.system(("rm /home/leandroall/logsminet/jsonRule.json"))
        #Arq S1
        for i in range (1,61):
            os.system(("rm /home/leandroall/logsminet/sendermininet" +str(i)+ ".log &"))
        #Arq S2
        for i in range(61, 121):
            os.system(("rm /home/leandroall/logsminet/sendermininet" +str(i)+ ".log &"))
        #Arq S3
        for i in range(1, 61):
            os.system(("rm /home/leandroall/logsminet/logmininet" +str(i)+ ".log &")) 
        #Arq S5    
        for i in range(61, 121):
            os.system(("rm /home/leandroall/logsminet/logmininet" +str(i)+ ".log &"))         

    def startReceivers():

         #Arq S3
        for i in range(1, 61):
            os.system(("> /home/leandroall/logsminet/logmininet" +str(i)+ ".log &")) 
         #S3 para ouvir   
        for i in range(NHostS2, NHostS3):
             hS3=net.get('h'+str(i))
             hS3.waiting = False
             hS3.cmd("/home/leandroall/D-ITG-2.8.1-r1023/bin/ITGRecv &" ) 

        #Arq S5    
        for i in range(61, 121):
            os.system(("> /home/leandroall/logsminet/logmininet" +str(i)+ ".log &")) 

        #S5 para ouvir
        for i in range(NHostS3, NHostS5):
             hS5=net.get('h'+str(i))
             hS5.waiting = False
             hS5.cmd("/home/leandroall/D-ITG-2.8.1-r1023/bin/ITGRecv &" ) 

                     

    def startSenders():
        #Arq S1
        for i in range (1,41):
           os.system(("> /home/leandroall/logsminet/sendermininet" +str(i)+ ".log &"))
           #S1 envia para S3
           hS1=net.get('h'+str(i))
           hS1.waiting = False
           hS1.cmd(("/home/leandroall/D-ITG-2.8.1-r1023/bin/ITGSend -a 10.0.0."+str((NHostS2-1)+i)+" -C 1000 -c 1500 -T TCP -t 1800000 -l /home/leandroall/logsminet/sendermininet" +str(i)+ ".log -x /home/leandroall/logsminet/logmininet"+str(i)+".log &"))
        
        
        #Arq S2
        for i in range(61, 101):
           os.system(("> /home/leandroall/logsminet/sendermininet" +str(i)+ ".log &"))
           #S2 envia para S5
           hS2=net.get('h'+str(i))
           hS2.waiting = False
           if (i == 61):
               hS2.cmd(("/home/leandroall/D-ITG-2.8.1-r1023/bin/ITGSend -a 10.0.0."+str((NHostS2-1)+i)+" -C 50 -c 20 -T UDP -t 1800000 -l /home/leandroall/logsminet/sendermininet" +str(i)+ ".log -x /home/leandroall/logsminet/logmininet" +str(i)+ ".log &"))
           else:
               hS2.cmd(("/home/leandroall/D-ITG-2.8.1-r1023/bin/ITGSend -a 10.0.0."+str((NHostS2-1)+i)+" -C 1000 -c 1500 -T TCP -t 1800000 -l /home/leandroall/logsminet/sendermininet" +str(i)+ ".log -x /home/leandroall/logsminet/logmininet" +str(i)+ ".log &"))
    #testar 
    #Perda boa: -a 10.0.0.69 -C 1000 -c 512 -T UDP -t 300000


    print "*** Clearing All Files "
    
    cleanArqs()
    
    #print "*** Create jsonRule "

    #createJsonRule()   

    #print "*** Set conf to QOS " 

    #createQueue()     
   
    #wipe-out please  -- comando para lmpar o onos

    time.sleep(50)
    
    print "*** Start Regular Receiver to Listen"

    startReceivers()  

    print "*** Starting Regular Sends"
    
    startSenders()
    
    CLI(net)



if __name__ == '__main__':
    setLogLevel('info')  # for CLI output
    myController()
