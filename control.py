from tabulate import tabulate
import libvirt

LIBVIRT_URI = "qemu+ssh://192.168.22.231/system"
client = libvirt.open(LIBVIRT_URI)
if client == None:
    print("Failed to open connection to " + LIBVIRT_URI)
    exit(1)

print("Please choose an option")
print("1: List All VMs")
print("2: Power On VM")
print("3: Power Off VM")
print("4: Exit")

choice = input("Your choice: ")

if choice == "4":
    exit(0)

elif choice == "1":
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

elif choice == "2":
    input("Please enter the name of the VM you would like to turn on: ")

elif choice == "3":
    input("Please enter the name of the VM you would like to turn off: ")

else:
    exit(0)
client.close()
exit(0)
