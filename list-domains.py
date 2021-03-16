#!/usr/bin/python

from tabulate import tabulate
import libvirt

LIBVIRT_URI = "qemu+ssh://192.168.22.231/system"



client = libvirt.openReadOnly(LIBVIRT_URI)
if client == None:
    print("Failed to open connection to " + LIBVIRT_URI)
    exit(1)

print("List of All VMs on the Host:")
domains = client.listAllDomains(0)
if len(domains) != 0:
    domain_list = []
    for domain in domains:
        if domain.isActive() == 1:
            domain_list.append([domain.name(), "Running"])
        elif domain.isActive() == 0:
            domain_list.append([domain.name(), "Stopped"])
    print(tabulate(domain_list, headers=["VM Name", "Status"]))

client.close()
exit(0)
