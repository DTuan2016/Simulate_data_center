from simulate import Cluster
from datetime import datetime
from pathlib import Path
import time
import threading
import pandas as pd

timer = 0
timer_running = False

def start_timer():
    def run():
        global timer, timer_running
        timer_running = True
        while timer_running:
            time.sleep(60)
            timer += 1
    threading.Thread(target=run, daemon=True).start()


def find_file_path_by_timestamp(timestamp: str, data_type: str):
    """
    Trả về đường dẫn file CSV tương ứng với timestamp.
    `data_type` có thể là "vm" hoặc "host".
    """
    try:
        dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        date_str = dt.strftime("%Y-%m-%d")
        file_name = f"grouped_metrics_{date_str}.csv"

        base_path = Path("/home/thuong/data")
        if data_type == "vm":
            file_path = base_path / "merged_output" / file_name
        elif data_type == "host":
            file_path = base_path / "merged_output" / "merged_output.csv"
        else:
            print(f"[RUN] Không hỗ trợ loại dữ liệu: {data_type}")
            return None

        if file_path.exists():
            return file_path
        else:
            print(f"[RUN] File {file_name} ({data_type}) không tồn tại.")
            return None

    except Exception as e:
        print(f"[RUN] Lỗi xử lý timestamp: {e}")
        return None


def is_september(timestamp_str):
    try:
        dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        return dt.month == 9
    except ValueError:
        print("[RUN] Định dạng thời gian không hợp lệ. Đúng định dạng: YYYY-MM-DD HH:MM:SS")
        return False


def run():
    # start_timer()
    print("[RUN] Nhập thời gian (YYYY-MM-DD HH:MM:SS), hoặc gõ 'exit' để thoát")

    while True:
        input_str = input("[RUN] >>> ")

        if input_str.lower() in ['exit', 'quit']:
            print("[RUN] Thoát chương trình.")
            break

        if not is_september(input_str):
            print("[RUN] Chỉ chấp nhận dữ liệu trong tháng 9.")
            continue

        vm_file = find_file_path_by_timestamp(input_str, "vm")
        host_file = find_file_path_by_timestamp(input_str, "host")

        if vm_file is None or host_file is None:
            print("[RUN] Không tìm thấy đủ file dữ liệu.")
            continue

        try:
            print(f"[RUN] Đã nạp dữ liệu VM từ: {vm_file}")
            print(f"[RUN] Đã nạp dữ liệu Host từ: {host_file}")
            timestamp = input_str
            timer = 0
            timer_running = False
            start_timer()

            # Khởi tạo mô hình trung tâm dữ liệu
            cluster = Cluster(host_file, vm_file, timestamp)
            print("[RUN] DataCenter đã được khởi tạo thành công.")

            while True:
                print("\n[RUN] Chọn một hành động:")
                print("  1. Hiển thị danh sách VM theo từng Host")
                print("  2. Di chuyển VM từ Host này sang Host khác")
                print("  3. Cập nhật data center")
                print("  4. Thoát")

                choice = input("[RUN] >>> ").strip()

                if choice == "1":
                    cluster.show_info_data_center()

                elif choice == "2":
                    source = input("[MIGRATE] Nhập tên host nguồn: ").strip()
                    dest = input("[MIGRATE] Nhập tên host đích: ").strip()
                    vm_id = input("[MIGRATE] Nhập VM UUID cần di chuyển: ").strip()

                    src_host = next((h for h in cluster.hosts if h.hostname == source), None)
                    dst_host = next((h for h in cluster.hosts if h.hostname == dest), None)

                    if not src_host or not dst_host:
                        print("[MIGRATE] Không tìm thấy host nguồn hoặc đích.")
                        continue

                    vm_obj = next((vm for vm in src_host.vms if vm.uuid == vm_id), None)

                    if not vm_obj:
                        print(f"[MIGRATE] Không tìm thấy VM {vm_id} trên host {source}.")
                        continue

                    src_host.vms.remove(vm_obj)
                    dst_host.vms.append(vm_obj)
                    print(f"[MIGRATE] Đã di chuyển VM {vm_id} từ {source} sang {dest}.")

                elif choice == "3":
                    cluster.update_vm_metrics_after_timer(timestamp, 1, vm_file, host_file)

                elif choice == "4":
                    print("[RUN] Thoát chương trình.")
                    return

                else:
                    print("[RUN] Lựa chọn không hợp lệ. Hãy thử lại.")

        except Exception as e:
            print(f"[RUN] Lỗi khi xử lý dữ liệu: {e}")


if __name__ == "__main__":
    run()
