# easy_antispoof

If you are an ISP Access Network Administrator and you have assigned your
users public ip addresses, you certainly have seen Spoofed packets or
packets that are comming up with source ip addresses other than the one it 
should have, now you could enable dhcp antispoofing if your customers are
getting ip addresses via DHCP, but if your users are getting their public 
ip address just through a static route - you point to their public address
and they point to you as their Default Route - then you have to create an ACL
under the user interface specifying the source ip address that is allowed to
access the network.


## how to use
-------------
simply type

$ python2 easy_antispoof.py


## Output Example:
-------------
Once you execute the python code you will be prompted to answer some questions

###Enter Customer Name
customer_A
###Enter the Gigabit interface number (ex: 1/0/14)
1/0
###Enter how many public ip addresses are there (ex: 1)
1
###Enter the public subnet (ex: 1.1.1.0/30)
1.1.1.0/30
###Enter the private subnet (ex: 172.16.40.0/30)
192.168.1.1/30


ip access-list ex Antispoof_customer_A
 permit ip 192.168.1.0 0.0.0.3 192.168.1.0 0.0.0.3
 permit ip 1.1.1.0 0.0.0.3 host 192.168.1.1
 deny ip any 10.0.0.0 0.255.255.255
 deny ip any 172.16.0.0 0.15.255.255
 deny ip any 192.168.0.0 0.0.255.255
 permit ip 1.1.1.0 0.0.0.3 any
 deny ip any any
!
interface GigabitEthernet 1/0
ip access-group Antispoof_customer_A in


## Caution
----------
This code has been tested on My network invironment and it works well,
but make sure to test it on yours before you implement it on your production Network.
