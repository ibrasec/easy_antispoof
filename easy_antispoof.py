#!/usr/bin/env python2.7
from netaddr import IPNetwork


cust = raw_input("Enter The Customer Name\n")
#vlan = raw_input("Enter vlan id\n")
interface = raw_input("Enter the FastEthernet/GigabitEthernet interface number (ex: 1/0/14)\n")
how_many = input("Enter how many public subnets are assigned to the customer (ex: 1)\n")


def get_subnets(i):
        return [ raw_input("Enter the public subnet #" + str(i+1) + " (ex: 1.1.1.0/30)\n").strip() for i in range(i) ]


def get_wildcard_mask(subnet):
        mask = str( IPNetwork(subnet).netmask )
        ma={'0':'255','128':'127','192':'63','224':'31','240':'15','248':'7','252':'3','254':'1','255':'0'}
        wildcard_mask = '.'.join([ ma[i] for i in mask.split('.') ])
        return wildcard_mask

pub = get_subnets(how_many)
priv = raw_input("Enter the private subnet (ex: 172.16.40.0/30)\n")

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
