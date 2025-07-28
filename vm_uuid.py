import math
class VM:
    def __init__(self, hostname, uuid, steal, usage, net_in, net_out, cpu_allocated):
        self.placemented = False
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

    def is_powered_off(self, cpu_usage_list, timestamps, window_minutes=5):
        """
        Kiểm tra nếu usage là NaN trong toàn bộ cửa sổ 5 phút => VM bị tắt.
        :param cpu_usage_list: list các giá trị usage (có thể có NaN)
        :param timestamps: list các timestamp tương ứng
        :param window_minutes: thời gian kiểm tra (mặc định 5 phút)
        :return: True nếu VM bị tắt, False nếu không
        """
        nan_count = 0
        for u in cpu_usage_list:
            if u is None or (isinstance(u, float) and math.isnan(u)):
                nan_count += 1

        if nan_count == len(cpu_usage_list) and len(cpu_usage_list) > 0:
            last_ts = timestamps[-1] if timestamps else "Unknown"
            print(f"[VM_ALERT] VM {self.uuid} bị tắt tại thời điểm {last_ts}")
            return True
        else:
            print(f"[VM_CHECK] VM {self.uuid} đang hoạt động bình thường.")
            return False