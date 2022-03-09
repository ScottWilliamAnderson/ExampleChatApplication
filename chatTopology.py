"""Custom topology example

Two directly connected switches plus a host for leftSwitch and two for rightSwitch:

   host --- switch --- switch --- host
                            `--- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
import mininet.log
from mininet.log import setLogLevel
from mininet.link import TCLink
from mininet.cli import CLI
import os
import subprocess as sub
import threading as th
import sys
import time
import pexpect


# dir variable should look like dir = "Desktop/NSE/" if ExampleChatApplication folder is inside the NSE folder on my Desktop
dir = "Desktop/NSE/"


def directorySet():
    if not dir:
        raise Exception("Please put the location of ExampleChatApplication-1.0.5 folder into the top of this python file ")

class ChatTopo( Topo ):
    "Simple Chat server with two clients topology."
# https://github.com/mininet/mininet/wiki/Introduction-to-Mininet#setting



    def build( self , n=2):
        directorySet()

        
        print('Cleaning up crumbs from last run')
        os.system('sudo mn -c -v output')
        print('Cleanup Complete')
        
        "Create custom topo."

        "Create chat server host"
        server = self.addHost('server')
        "connect the server host to its switch"
        serverSwitch = self.addSwitch('s1')
        self.addLink(server, serverSwitch)

        userSwitch = self.addSwitch('s2')

        for h in range(n):
            host = self.addHost( 'h%s' % (h + 1))
            # 10 Mbps, 5ms delay, 2% loss, 1000 packet queue, using hierarchical token bucket (HTB) use_htb=True 
            self.addLink( host, userSwitch, bw=10, delay='5ms', loss=2,
                          max_queue_size=1000)

        self.addLink( serverSwitch, userSwitch )

        # self.simpleTest()

def createMininet():
    "Create network and run simple performance test"
    topo = ChatTopo( n=2 )
    net = Mininet( topo=topo, link=TCLink )
    net.start()

    perfTest(net)
    
    # net.stop()

def perfTest(net):
    # pingtest(net)
    chat(net)
    

def pingtest(net):
    print( "Dumping host connections" )
    dumpNodeConnections( net.hosts )
    print( "Testing network connectivity" )
    net.pingAll()
    print( "Testing bandwidth between h1 and server" )
    h1, server = net.get( 'h1', 'server' )
    net.iperf( (h1, server) )

def chat(net):
    print('Testing Chat')

    # serverThread = th.Thread(target = bootServer(net), daemon=True)
    # serverThread.start()
    # server = net.get('server')
 

    server, alice, bob = manualBoot(net)

    alice.cmd("/msg Bob Hello!")

def manualBoot(net):
    server = net.get('server')
    serverIP = server.IP()
    print("Server Host created, lives at IP = " + serverIP)
    alice, bob = net.get('h1'), net.get('h2')

    myScript = "xterm.sh"
    CLI(net, script = myScript)

    # time.sleep(10000)

    return server, alice, bob


def boot(net):
    server = net.get('server')
    serverIP = server.IP()
    print("Server Host created, lives at IP = " + serverIP)
    print('Chat server is booting...')
    serverDirectory = 'ExampleChatApplication-1.0.5/ChatServer/bin/Release/netcoreapp5.0'
    server.cmd("cd " + str(serverDirectory))

    serverInstance = server.popen("dotnet exec ChatServer.dll --global > serverlog.txt", cwd = serverDirectory, shell = True)
    time.sleep(2)
    print("Running server on port 12345 Global Bind True")

    alice, bob = net.get('h1'), net.get('h2')
    print('Alice and Bob start their Chat Clients')
    alice.cmd('cd ExampleChatApplication-1.0.5')
    bob.cmd('cd ExampleChatApplication-1.0.5')

    chatDirectory = 'ExampleChatApplication-1.0.5/ChatClient/bin/Release/netcoreapp5.0'

    alice.cmd('cd '+ str(chatDirectory))
    bob.cmd('cd '+ str(chatDirectory))

    aliceOn = 'dotnet exec ChatClient.dll Alice ' + str(server.IP() + ' > AliceLog.txt')
    #  + ' > AliceLog.txt'
    bobOn = 'dotnet exec ChatClient.dll Bob ' + str(server.IP() + ' > BobLog.txt')
    #  + ' > BobLog.txt'
    # capture_output=True

    aliceOnline = alice.popen(aliceOn, shell = True, cwd = chatDirectory)
    print("Alice logged in")

    bobOnline = bob.popen(bobOn, shell = True, cwd = chatDirectory)
    print("Bob logged in")
    time.sleep(2)

    with "xterm.sh" as myScript:
        CLI(net, script = myScript)

    # with server.popen("dotnet exec ChatServer.dll --global > serverlog.txt", cwd = serverDirectory, shell = True) as serverInstance:

    #     # serverLog(serverBootup.stdout.read())
    #     # print(serverBootup.stdout.read(), flush=True)
    #     # f = open("serverlog.txt", "w", buffering = 1)
    #     # f.write(serverBootup.stdout.read())
    #     # serverBootup = server.popen("dotnet" "exec", "ChatServer.dll", "--global", cwd = serverDirectory)
    #     # serverBootup.stdout.close()
    #     # print(serverBootup)
        
    #     time.sleep(2)

    #     print("Running server on port 12345 Global Bind True")

    #     alice, bob = net.get('h1'), net.get('h2')
    #     print('Alice and Bob start their Chat Clients')
    #     alice.cmd('cd ExampleChatApplication-1.0.5')
    #     bob.cmd('cd ExampleChatApplication-1.0.5')

    #     chatDirectory = 'ExampleChatApplication-1.0.5/ChatClient/bin/Release/netcoreapp5.0'

    #     alice.cmd('cd '+ str(chatDirectory))
    #     bob.cmd('cd '+ str(chatDirectory))

    #     aliceOn = 'dotnet exec ChatClient.dll Alice ' + str(server.IP() + ' > AliceLog.txt')
    #     #  + ' > AliceLog.txt'
    #     bobOn = 'dotnet exec ChatClient.dll Bob ' + str(server.IP() + ' > BobLog.txt')
    #     #  + ' > BobLog.txt'
    #     # capture_output=True

    #     # alice.cmd(aliceOn, shell = True, cwd = chatDirectory)

    #     # alice.sendCmd(aliceOn)
    #     # print("Alice logged in")

    #     # bob.sendCmd(bobOn)
    #     # print("Bob logged in")

    #     # alice.sendCmd(aliceOn)

    #     # aliceOnline = alice.pexpect.spawn(aliceOn)
    #     # print("Alice logged in")

    #     # bobOnline = bob.pexpect.spawn(bobOn)
    #     # print("Bob logged in")

       


    #     with alice.popen(aliceOn, shell = True, cwd = chatDirectory) as aliceOnline:
    #         # print(aliceBootup.stdout.read())

    #         print("Alice logged in")
    #         with bob.popen(bobOn, shell = True, cwd = chatDirectory) as bobOnline:
    #             print("Bob logged in")
    #             time.sleep(2)
    #             # bobOnline.cmd("/msg Alice Hi Alice! I'm online now \n", shell=True)
    #             # print("bob messaged")
    #             # bobOnline.stdin.write("/msg Alice Hi Alice! I'm online now n\n")
    #             # bobOnline.stdin.flush()
    #             # bobOnline.stdin.close()
    #             # bob.pexec("/msg Alice Hi Alice! I'm online now \n", shell=True)
    #             # bobOnline.communicate("/msg Alice Hi Alice! I'm online now \n", shell = True)
    #             # bobOnline.stdin.write("/msg Alice Hi Alice! I'm online now \n")
    #             # bobOnline.stdin.close()
    #             # print("bob messaged")
    #             myScript = "xterm.sh"
    #             CLI(net, script = myScript)






    return server, alice, bob




if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    createMininet()

topos = { 'ChatTopo': ( lambda: ChatTopo() ) }