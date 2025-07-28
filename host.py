from vm_uuid import VM
import numpy as np
from vm_uuid import VM
from datetime import datetime, timedelta
import ast

class Host:
    def __init__(self, hostname, host_cpu_usage):
        self.hostname = hostname
        self.host_cpu_usage = host_cpu_usage
        self.vms = []

    def add_vm_to_host(self, vm: VM):
        if vm.hostname == self.hostname:
            self.vms.append(vm)

    def delete_vm_from_host(self, vm_uuid: str):
        for vm in self.vms:
            if vm.uuid == vm_uuid:
                self.vms.remove(vm)
                print(f"[HOST] Đã xóa VM {vm_uuid} khỏi host {vm.hostname}.")
                return
        print(f"[HOST] Không tìm thấy VM {vm_uuid} trong host {self.hostnames}.")

    def show_info_host(self):
        print(f"[HOST] Host: {self.hostname} | CPU Usage: {self.host_cpu_usage:.2f}%")
        for i, vm in self.vms:
            vm.show_info_vm(i)
        
    def _parse_to_list(self, field: str, value_type=float):
        """Parse chuỗi thành list theo kiểu dữ liệu cụ thể (mặc định: float)."""
        if not isinstance(field, str):
            return []

        field = field.strip()

        try:
            # Dạng list Python: "[1, 2, 3]"
            if field.startswith("[") and field.endswith("]"):
                return [value_type(x.strip()) for x in field[1:-1].split(",") if x.strip()]
            # Dạng phân cách bằng dấu ";"
            elif ";" in field:
                return [value_type(x.strip()) for x in field.split(";") if x.strip()]
            # Một giá trị duy nhất
            else:
                return [value_type(field)]
        except Exception:
            return []

    def _parse_list_of_strings(self, field: str):
        """Parse chuỗi thành list string."""
        if isinstance(field, str):
            try:
                return ast.literal_eval(field)
            except Exception:
                return []
        return []
