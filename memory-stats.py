import libvirt

LIBVIRT_URI = "qemu+ssh://ndebruin@192.168.22.231/system"


client = libvirt.openReadOnly(LIBVIRT_URI)
if client == None:
    print("Failed to open connection to " + LIBVIRT_URI)
    exit(1)

sysinfo = client.getInfo()
freemem = float(client.getFreeMemory())
freemem = freemem /1024 /1024

totalmem = float(sysinfo[1])
usedmem = totalmem - freemem

print(str(int(totalmem)) + " Total MB of Memory")
print(str(int(usedmem)) + " MB Used of Memory")
print(str(int(freemem)) + " MB Free of Memory")


client.close()
exit(0)
