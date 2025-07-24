from vm_uuid import VM

class Host:
    def __init__(self, hostname, timestamp):
        self.hostname = hostname
        self.timestamp = timestamp
        self.vms = []

    def add_vm(self, vm: VM):
        self.vms.append(vm)

    def print_info(self):
        print(f"\nTimestamp: {self.timestamp}")
        print(f"Hostname: {self.hostname}")
        for idx, vm in enumerate(self.vms):
            vm.print_info(idx)
