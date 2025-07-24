class VM:
    def __init__(self, uuid, steal, usage, net_in, net_out, cpu_allocated):
        self.uuid = uuid
        self.steal = steal
        self.usage = usage
        self.net_in = net_in
        self.net_out = net_out
        self.cpu_allocated = cpu_allocated

    def print_info(self, index):
        print(f"VM {index + 1} - UUID: {self.uuid}")
        print(f"    Steal        : {self.steal}")
        print(f"    Usage        : {self.usage}")
        print(f"    Network In   : {self.net_in}")
        print(f"    Network Out  : {self.net_out}")
        print(f"    CPU Allocated: {self.cpu_allocated}")
