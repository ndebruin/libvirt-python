import libvirt

LIBVIRT_URI = "qemu+ssh://ndebruin@192.168.22.231/system"


client = libvirt.open(LIBVIRT_URI)

print(client.listalldomains())
