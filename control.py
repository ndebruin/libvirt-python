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
    print("Please choose an option\n")
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
            print("List of All VMs on the Host:\n")
            for domain in domains:
                if domain.isActive() == 1:
                    domain_list.append([domain.name(), "Running", str(domain.maxMemory()/1024), str(domain.info()[3])]) 
                elif domain.isActive() == 0:
                    domain_list.append([domain.name(), "Stopped", str(domain.maxMemory()/1024), str(domain.info()[3])]) #why the fuck does maxMemory work offline, but maxVcpus not?
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
            #god i fucking hate this please end this nightmare
            VM.setVcpusFlags(int(change), flags=6)
            #first changes the maximum in the config, then changes the current to match the max
            #this stupidity is needed for when you want to increase the number of vCPUs, but are not needed for decreaseing
            #values from https://libvirt.org/html/libvirt-libvirt-domain.html#virDomainVcpuFlags
            VM.setVcpusFlags(int(change), flags=0)
            
            

        elif config_choice == "2":
            domain_choice = input("Please enter the name of the VM you would like to change: ")
            VM = client.lookupByName(domain_choice)
            change = input("\nPlease enter the amount of RAM in MiB you would like: ")
            #GOD I HAVE TO DO THE SAME BULLSHIT
            VM.setMemoryFlags(int(change)*1024, flags=6)
            #first changes max in config, then matches up the current value to the config
            #values are the same as above
            #https://libvirt.org/html/libvirt-libvirt-domain.html#virDomainMemoryModFlags
            VM.setMemoryFlags(int(change)*1024, flags=0)



    else:
        client.close()
        exit(0)

client.close()
exit(0)
