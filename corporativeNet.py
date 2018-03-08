#!/usr/bin/python


from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch, RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.topo import Topo


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

    print "*** Starting  CLI"
    net.start()
    print "*** Testing the connection between hosts "
    net.staticArp()
    net.pingAllFull()
    

    CLI(net)



if __name__ == '__main__':
    setLogLevel('info')  # for CLI output
    myController()
