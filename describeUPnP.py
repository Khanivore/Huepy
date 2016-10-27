# Show descriptions of UPnP devices discovered
# Python 3

import socket
import urllib.request
import xml.etree.ElementTree as ET

descriptions = set([])

msg = \
    'M-SEARCH * HTTP/1.1\r\n' \
    'HOST:239.255.255.250:1900\r\n' \
    'ST:upnp:rootdevice\r\n' \
    'MX:2\r\n' \
    'MAN:"ssdp:discover"\r\n'
 
# Set up UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s.settimeout(2)
s.sendto( bytes(msg, 'utf-8'), ('239.255.255.250', 1900) )
 
try:
    while True:
        data, addr = s.recvfrom(65507)
        msearchResponses = data.decode('utf-8').splitlines()
        for msearchResponseItem in msearchResponses:
            if msearchResponseItem.startswith('LOCATION'):
                descriptions.add(msearchResponseItem[10:])
except socket.timeout:
    pass

for description in descriptions:
    with urllib.request.urlopen(description) as response:
        xmlDescription = response.read().decode('utf-8')
