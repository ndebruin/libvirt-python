#!/usr/bin/python

import libvirt

LIBVIRT_URI = "qemu+ssh://192.168.22.231/system"


client = libvirt.openReadOnly(LIBVIRT_URI)
if client == None:
    print("Failed to open connection to " + LIBVIRT_URI)
    exit(1)


domains = client.listAllDomains()
for domain in domains:
    print(domain.memoryParameters())






client.close()
exit(0)
