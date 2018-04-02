#!/usr/bin/env python2.7
from netaddr import IPNetwork
import netaddr.core

def isvalidip(ip):
    '''
    To check if the passed ip address is a valid ipv4 or ipv6 address
    example:
    >>>isvalidip('10.1.1.1')
    True
    >>>isvalidip('10.1.1.1.')
    False
    >>>isvalidip('2001:db8::1/120')
    True
    '''
    try:
        IP = IPNetwork(ip.strip())
        return True
    except netaddr.core.AddrFormatError:
        return False
    except ValueError:
        return False



cust = raw_input("Enter The Customer Name\n")
#vlan = raw_input("Enter vlan id\n")
interface = raw_input("Enter the FastEthernet/GigabitEthernet interface number (ex: 1/0/14)\n")
how_many = input("Enter how many public subnets are assigned to the customer (ex: 1)\n")


def check_subnet(sub):
        while True:
                if isvalidip( sub):
                        if '/' not in sub:
                                sub = raw_input("[!] Please Re-Enter the subnet followed by subnet mask\n")
                        else:
                                return sub
                                #break
                else:
                        sub = raw_input("Please Enter a vaild ip subnet\n")
                        continue 


def get_subnets(i):
        subnet_list = list()
        for iteration in range(i):
                public_subnet = raw_input("Enter the public subnet #" + str(iteration+1) + " (ex: 1.1.1.0/30)\n").strip() 
                subnet_list.append( check_subnet(public_subnet) )
        return subnet_list



def get_wildcard_mask(subnet):
        mask = str( IPNetwork(subnet).netmask )
        ma={'0':'255','128':'127','192':'63','224':'31','240':'15','248':'7','252':'3','254':'1','255':'0'}
        wildcard_mask = '.'.join([ ma[i] for i in mask.split('.') ])
        return wildcard_mask



pub = get_subnets(how_many)
priv = check_subnet( raw_input("Enter the private subnet (ex: 172.16.40.0/30)\n") )

print "\n\nip access-list ex Antispoof_"+cust
print " permit ip",str(IPNetwork(priv).network),str(IPNetwork(priv).hostmask),str(IPNetwork(priv).network),str(IPNetwork(priv).hostmask)
for subnet in pub:
        print " permit ip",str(IPNetwork(subnet).network),str(IPNetwork(subnet).hostmask),"host",str(list(IPNetwork(priv))[1])
print " deny ip any 10.0.0.0 0.255.255.255" 
print " deny ip any 172.16.0.0 0.15.255.255"
print " deny ip any 192.168.0.0 0.0.255.255"
for subnet in pub:
        print " permit ip",str(IPNetwork(subnet).network),get_wildcard_mask(subnet),"any" 
print " deny ip any any"
print "!"

print "interface GigabitEthernet",interface
print "ip access-group Antispoof_"+cust,"in"
print ""
