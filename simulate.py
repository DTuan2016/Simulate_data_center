from vm_uuid import VM
import pandas as pd
import ast
from host import Host
    
class Cluster:
    def __init__(self, path_data_host, path_data_vm, timestamp):
        self.hosts = self.load_hosts_at_timestamp(path_data_host, path_data_vm, timestamp)

    def load_hosts_at_timestamp(self, path_data_host, path_data_vm ,timestamp: str):
        ts = pd.to_datetime(timestamp)
        
        df_host = pd.read_csv(path_data_host)
        df_vm = pd.read_csv(path_data_vm)
        df_host["timestamp"] = pd.to_datetime(df_host["timestamp"])
        df_vm["timestamp"] = pd.to_datetime(df_vm["timestamp"])
        
        host_rows = df_host[df_host['timestamp'] == ts]
        vm_rows = df_vm[df_vm['timestamp'] == ts]

        if host_rows.empty:
            print(f"[DATACENTER] Không tìm thấy dữ liệu host tại thời điểm {timestamp}")
        if vm_rows.empty:
            print(f"[DATACENTER] Không tìm thấy dữ liệu VM tại thời điểm {timestamp}")

        hosts = []
        for _, row in host_rows.iterrows():
            hostname = row['hostname']
            host_cpu_usage = float(row.get('host_cpu_usage', 0.0))

            # Tạo Host, truyền cả 2 DataFrame để kiểm tra VM shutdown nếu cần
            host = Host(hostname, host_cpu_usage)

            # Lọc VM thuộc host này
            vm_rows_for_host = vm_rows[vm_rows['hostname'] == hostname]
            for _, vm_row in vm_rows_for_host.iterrows():
                uuid_list = host._parse_list_of_strings(vm_row["uuid_set"])
                steals = host._parse_to_list(vm_row["vm_cpu_steal"])
                usages = host._parse_to_list(vm_row["vm_cpu_usage"])
                net_ins = host._parse_to_list(vm_row["vm_network_in"])
                net_outs = host._parse_to_list(vm_row["vm_network_out"])
                allocs = host._parse_to_list(vm_row["vm_cpu_allocated"])

                for i, uuid in enumerate(uuid_list):
                    steal = steals[i] if i < len(steals) else None
                    usage = usages[i] if i < len(usages) else None
                    net_in = net_ins[i] if i < len(net_ins) else None
                    net_out = net_outs[i] if i < len(net_outs) else None
                    alloc = allocs[i] if i < len(allocs) else None

                    vm = VM(hostname, uuid, steal, usage, net_in, net_out, alloc)
                    # vm.is_shutdown = host.is_vm_shutdown(uuid, timestamp)

                    host.add_vm_to_host(vm)

            hosts.append(host)

        return hosts

    # def is_vm_shutdown(self, uuid: str, current_timestamp: str, window_minutes: int = 5):
    #     try:
    #         current_time = datetime.strptime(current_timestamp, "%Y-%m-%d %H:%M:%S")
    #     except Exception as e:
    #         print(f"[HOST] Lỗi định dạng thời gian: {e}")
    #         return False

    #     time_range = [
    #         (current_time - timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M:%S")
    #         for i in range(window_minutes)
    #     ]

    #     df_window = self.df_vm[self.df_vm['timestamp'].isin(time_range)]

    #     for _, row in df_window.iterrows():
    #         uuid_list = self._parse_list_of_strings(row["uuid_set"])
    #         usages = self._parse_to_list(row["vm_cpu_usage"])

    #         if uuid not in uuid_list:
    #             return False

    #         idx = uuid_list.index(uuid)
    #         try:
    #             usage = float(usages[idx])
    #             if not np.isnan(usage):
    #                 return False
    #         except:
    #             return False

    #     return True
    
    def show_info_data_center(self):
        # print(f"\n[SIMULATE] Timestamp: {self.timestamp}")
        for host in self.hosts:
            host.show_info_host()
    
    def find_host_by_hostname(self, hostname):
        for host in self.hosts:
            if host.hostname == hostname:
                return host
        print(f"[SIMULATE] Không tồn tại host nào có tên {hostname}")

    def find_vm_by_uuid(self, uuid: str):
        for host in self.hosts:
            for vm in host.vms:
                if vm.uuid == uuid:
                    print(f"[SIMULATE] VM có {uuid} nằm ở host {host.hostname}")
                    return host, vm

        print(f"[SIMULATE] Không tìm thấy VM có UUID là {uuid}")
        return None, None

    def migrate_vm_to_other_host(self, uuid: str, target_hostname: str):
        source_host, vm_to_migrate = self.find_vm_by_uuid(uuid)
        if source_host is None or vm_to_migrate is None:
            print(f"[DATACENTER] Không thể thực hiện chuyển VM vì không tìm thấy.")
            return

        dest_host = self.find_host_by_hostname(target_hostname)
        if dest_host is None:
            print(f"[DATACENTER] Không tìm thấy host đích {target_hostname}")
            return

        # Di chuyển VM
        source_host.vms.remove(vm_to_migrate)
        vm_to_migrate.hostname = dest_host.hostname
        dest_host.vms.append(vm_to_migrate)

        print(f"[DATACENTER] Đã chuyển VM {uuid} từ host {source_host.hostname} sang host {dest_host.hostname}")