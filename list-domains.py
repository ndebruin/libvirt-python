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
    for domain in domains:
        if domain.isActive() == 1:
            #print("     "+domain.name()+"       Running")
            print(tabulate([[domain.name(), "Running"]], headers=["Name", "Status"]))
        else:
            print(tabulate([[domain.name(), "Stopped"]]))
            #print("     "+domain.name()+"       Stopped")

client.close()
exit(0)
