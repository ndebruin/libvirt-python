#!/usr/bin/python


from tabulate import tabulate
import libvirt
from time import sleep


#LIBVIRT_URI = "qemu+ssh://192.168.22.231/system"
LIBVIRT_URI = "qemu:///system"
client = libvirt.open(LIBVIRT_URI)
if client == None:
    print("Failed to open connection to " + LIBVIRT_URI)
    exit(1)


while True:
    print("\033c", end="")
    print("Please choose an option")
    print("1: List All VMs")
    print("2: VM Power Controls")
    print("3: Change VM Configuration")
    print("4: Exit")

    choice = input("\nYour choice: ")

    if choice == "4":
        client.close()
        exit(0)

    elif choice == "1":
        domains = client.listAllDomains(0)
        if len(domains) != 0:
            print("\033c", end="")
            domain_list = []
            print("List of All VMs on the Host:")
            for domain in domains:
                state, maxmem, mem, cpus, cput = domain.info()
                if domain.isActive() == 1:
                    domain_list.append([domain.name(), "Running", str(mem/1024), str(cpus)])
                elif domain.isActive() == 0:
                    domain_list.append([domain.name(), "Stopped", str(mem/1024), str(cpus)])
            print(tabulate(domain_list, headers=["VM Name", "Status", "Memory Allocated in MiB", "Number of vCPUs"])+"\n")
            input("Press any key to return")

    elif choice == "2":
        print("\033c", end="")
        print("1: Power on VM")
        print("2: Power off VM")
        power_choice = input("\nPlease Enter your choice: ")

        if power_choice == "1":
            domain_choice = input("Please enter the name of the VM you would like to turn on: ")
            VM = client.lookupByName(domain_choice)
            if VM.isActive() == 1:
                print("This VM is already powered up")
                sleep(1)
        
            else:
                VM.create()
                if VM.isActive() == 1:
                    print("VM successfully started")
                    sleep(1)
        
                else:
                    print("Something has gone wrong")
                    sleep(1)

        elif power_choice == "2":
            domain_choice = input("Please enter the name of the VM you would like to turn off: ")
            VM = client.lookupByName(domain_choice)
            if VM.isActive() == 0:
                print("This VM is already powered down")
                sleep(1)
        
            else:
                VM.shutdown()
                sleep(2)
                if VM.isActive() == 0:
                   print("VM successfully shutdown")
                   sleep(1)
        
                else:
                    print("Something has gone wrong")
                    sleep(1)
        
        else:
            sleep(0.01)


    elif choice == "3":
        print("\033c", end="")
        print("1: Change vCPU count")
        print("2: Change Memory size")
        config_choice = input("\nPlease Enter your choice: ")
        
        if config_choice == "1":
            domain_choice = input("Please enter the name of the VM you would like to change: ")
            VM = client.lookupByName(domain_choice)
            change = input("\nPlease enter the number of vCPUs you would like: ")
            VM.setVcpusFlags(int(change), )#flags=VIR_DOMAIN_AFFECT_CURRENT)

        elif config_choice == "2":
            domain_choice = input("Please enter the name of the VM you would like to change: ")
            VM = client.lookupByName(domain_choice)
            change = input("\nPlease enter the amount of RAM in MiB you would like: ")
            VM.setMemory(int(change))


    else:
        client.close()
        exit(0)

client.close()
exit(0)
