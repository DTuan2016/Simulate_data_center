import numpy as np
from vm_uuid import VM
import pandas as pd
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
        for i, vm in enumerate(self.vms):
            vm.print_info(i)
        
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
    
    def is_vm_shutdown(self, uuid: str, current_timestamp, window_minutes: int = 5, df_vm=None):
        try:
            if isinstance(current_timestamp, str):
                current_time = datetime.strptime(current_timestamp, "%Y-%m-%d %H:%M:%S")
            elif isinstance(current_timestamp, pd.Timestamp):
                current_time = current_timestamp.to_pydatetime()
            elif isinstance(current_timestamp, datetime):
                current_time = current_timestamp
            else:
                print(f"[HOST] Kiểu thời gian không hợp lệ: {type(current_timestamp)}")
                return False
        except Exception as e:
            print(f"[HOST] Lỗi định dạng thời gian: {e}")
            return False

        time_range = [
            current_time - timedelta(minutes=i) for i in range(window_minutes)
        ]
        df_window = df_vm[df_vm['timestamp'].isin(time_range)]

        for _, row in df_window.iterrows():
            uuid_list = self._parse_list_of_strings(row["uuid_set"])
            usages = self._parse_to_list(row["vm_cpu_usage"])

            if uuid not in uuid_list:
                return False

            idx = uuid_list.index(uuid)
            try:
                usage = float(usages[idx])
                if not np.isnan(usage):
                    return False
            except:
                return False

        return True
