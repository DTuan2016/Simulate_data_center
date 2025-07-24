from vm_uuid import VM
import pandas as pd
import ast
from host import Host

class Inspector:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = pd.read_csv(file_path)

    def _parse_list(self, field: str):
        if isinstance(field, str):
            try:
                return ast.literal_eval(field)
            except Exception:
                return []
        return []

    def _parse_float_list(self, field: str):
        if not isinstance(field, str):
            return []

        field = field.strip()

        if field.startswith("[") and field.endswith("]"):
            try:
                return [float(x.strip()) for x in field[1:-1].split(",") if x.strip()]
            except Exception:
                return []

        if ";" in field:
            return [float(x.strip()) for x in field.split(";") if x.strip()]

        try:
            return [float(field)]
        except:
            return []

    def inspect_by_timestamp(self, target_timestamp: str):
        matched_rows = self.df[self.df['timestamp'] == target_timestamp]

        if matched_rows.empty:
            print(f"Không tìm thấy timestamp: {target_timestamp}")
            return

        for _, row in matched_rows.iterrows():
            hostname = row["hostname"]
            uuid_list = self._parse_list(row["uuid_set"])
            steals = self._parse_float_list(row["vm_cpu_steal"])
            usages = self._parse_float_list(row["vm_cpu_usage"])
            net_ins = self._parse_float_list(row["vm_network_in"])
            net_outs = self._parse_float_list(row["vm_network_out"])
            allocs = self._parse_float_list(row["vm_cpu_allocated"])

            host = Host(hostname, target_timestamp)

            for i, uuid in enumerate(uuid_list):
                steal = steals[i] if i < len(steals) else "N/A"
                usage = usages[i] if i < len(usages) else "N/A"
                net_in = net_ins[i] if i < len(net_ins) else "N/A"
                net_out = net_outs[i] if i < len(net_outs) else "N/A"
                alloc = allocs[i] if i < len(allocs) else "N/A"

                vm = VM(uuid, steal, usage, net_in, net_out, alloc)
                host.add_vm(vm)

            host.print_info()
            