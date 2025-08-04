# import math
import numpy as np
# import ast
from datetime import datetime, timedelta
class VM:
    def __init__(self, hostname, uuid, steal, usage, net_in, net_out, cpu_allocated, is_shutdown):
        self.placemented = False
        self.is_shutdown = is_shutdown
        self.hostname = hostname
        self.uuid = uuid
        self.steal = steal
        self.usage = usage
        self.net_in = net_in
        self.net_out = net_out
        self.cpu_allocated = cpu_allocated
        
    def print_info(self, index):
        print(f"[VM_INFO] [{index}] VM UUID: {self.uuid} | "
              f"CPU Steal: {self.steal:.2f}% | "
              f"CPU Usage: {self.usage:.2f}% | "
              f"Network In: {self.net_in} KB/s | "
              f"Network Out: {self.net_out} KB/s | "
              f"CPU Allocated: {self.cpu_allocated} cores | "
              f"Hostname: {self.hostname}")
