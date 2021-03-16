#!/usr/bin/python

import libvirt

LIBVIRT_URI = "qemu+ssh://192.168.22.231/system"


client = libvirt.openReadOnly(LIBVIRT_URI)
if client == None:
    print("Failed to open connection to " + LIBVIRT_URI)
    exit(1)

cpumap = client.getCPUMap()
cpustats = client.getCPUStats(libvirt.VIR_NODE_CPU_STATS_ALL_CPUS, 0)

print(cpustats)

client.close()
exit(0)
