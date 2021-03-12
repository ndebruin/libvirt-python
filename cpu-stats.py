import libvirt

LIBVIRT_URI = "qemu+ssh://ndebruin@192.168.22.231/system"


client = libvirt.openReadOnly(LIBVIRT_URI)
if client == None:
    print("Failed to open connection to " + LIBVIRT_URI)
    exit(1)

cpumap = client.getCPUMap()


client.close()
exit(0)
