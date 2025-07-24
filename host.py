from vm_uuid import VM

class Host:
    def __init__(self, hostname, timestamp):
        self.hostname = hostname
        self.timestamp = timestamp
        self.vms = []

    def add_vm(self, vm: VM):
        self.vms.append(vm)

    def show_info(self):
        print(f"\nTimestamp: {self.timestamp}")
        print(f"Hostname: {self.hostname}")
        print (f"Total VMs: {len(self.vms)}\n")
        for i, vm in enumerate(self.vms, 1):
            print(f"    VM {i} - UUID: {vm.uuid}")
            print(f"    - Steal     : {vm.steal}")
            print(f"    - Usage     : {vm.usage}")
            print(f"    - Net In    : {vm.net_in}")
            print(f"    - Net Out   : {vm.net_out}")
            print(f"    - CPU Alloc : {vm.cpu_allocated}")
