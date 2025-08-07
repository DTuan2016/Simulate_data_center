# MÔ PHỎNG DATA CENTER CHO MIGRATE VM

Chương trình của tôi có các class như sau:
- Class VM          (file vm_uuid.py)
- Class host        (file host.py)
- Class Cluster  (file simulate.py)

## Class VM:

Lớp `VM` đại diện cho một máy ảo (Virtual Machine), chứa các thông tin liên quan đến hiệu suất tài nguyên, lưu lượng mạng và trạng thái hoạt động.
---
### Khởi tạo đối tượng
```python
def __init__(self, hostname, uuid, steal, usage, net_in, net_out, cpu_allocated, is_shutdown)
```

### In thông tin đối tượng ra
```python
def print_info(self, index)
```

## Class Host:

Lớp `Host` đại diện cho một máy chủ vật lý hoặc logic đang quản lý một danh sách các máy ảo (VM), cùng với thông tin về mwucs sử dụng CPU và các chức năng liên quan đến việc kiểm tra, thêm, xóa và hiện thị VM.
---

### Khởi tạo đối tượng `host`:
```python
def __init__(self, hostname, host_cpu_usage)
```
### Thêm `VM` vào danh sách VM của `host`:
```python
def add_vm_to_host(self, vm: VM)
```
### Xóa `VM` trong danh sách VM của `host`:
```python 
def delete_vm_from_host(self, vm_uuid: str)
```
### Hiển thị thông tin của host và các VM trong host đó:
```python
def show_info_host(self)
```
### Xử lý chuỗi:

2 hàm dưới đây được sử dụng để đọc dữ liệu từ file csv, với file dữ liệu của tôi có 2 loại chuỗi:
- Chuỗi các uuid khác nhau
- Chuỗi dữ liệu (float) ứng với các vm.
Vì thế tôi viết 2 hàm dưới đây để xử lý dữ liệu đọc từ csv vào.

```python
def _parse_to_list(self, field: str, value_type=float)
```

```python
def _parse_list_of_strings(self, field: str)
```

### Kiểm tra VM có được tắt hay không:
Đối với các VM, khi đọc dữ liệu đầu vào sẽ xem VM đó có bật không, đối với việc mô phỏng này. Nếu VM không có giá trị `CPU_USAGE` trong khoảng thời gian `window_minutes` thì tôi sẽ coi là VM đó bị tắt (`window_minutes = 5`)
```python
def is_vm_shutdown(self, uuid: str, current_timestamp, window_minutes: int = 5, df_vm=None)
```

## Class Cluster:
Lớp `Cluster` đại diện cho một cụm máy chủ (Data center), mỗi máy chủ chứa danh sách các máy ảo. Lớp này thực hiện các thao tác như sau:
- Load dữ liệu từ CSV
- Gắn VM vào host theo thời gian
- Di chuyển VM giữa các host
- Cập nhật trạng thái sử dụng tài nguyên của mỗi VM theo thời gian
---

### Khởi tạo đối tượng:
Để khởi tạo được cluster thì phải truyền vào các tham số như địa chỉ của file data host, địa chỉ của file data vm, thời gian muốn khởi tạo (Tôi chỉ có dữ liệu trong tháng 9)
``` python
def __init__(self, path_data_host, path_data_vm, timestamp)
```

### Đọc dữ liệu từ CSV:
Ở hàm khởi tạo, gọi đến hàm đọc dữ liệu từ CSV.
```python
def load_hosts_at_timestamp(self, path_data_host, path_data_vm ,timestamp: str)
```
Hàm này sẽ đọc thông tin từ `path_data_host`, `path_data_vm` để lấy thành Dataframe, sau đó chỉ lấy các dòng có timestamp trùng với `timestamp` truyền vào. Sau đó đọc các `hostname`, `host_cpu_usage` của từng dòng sau đó thêm thông tin vào cho `host`.
Với từng `host` thì lại đọc dữ liệu của các VM rồi add thông tin vào cho `danh sách VM` trong `host`.

### In thông tin của Cluster:
Hàm này gọi đến hàm in thông tin của từng `host`, rồi lại gọi đến hàm in thông tin của từng `VM` trong host đó
```python
def show_info_data_center(self)
```

### Các hàm thực hiện chức năng migrate `VM`:
1. Tìm host bằng hostname, trả về thông tin của `host`.
```python
def find_host_by_hostname(self, hostname)
```
2. Tìm vm bằng uuid, trả về `host`, thông tin của `VM` đó.
```python
def find_vm_by_uuid(self, uuid: str)
```
3. Thực hiện migrate VM đến host khác:
```python 
def migrate_vm_to_other_host(self, uuid: str, target_hostname: str)
```
- Tìm `uuid` truyền vào có tồn tại không, nó ở `host` nào sẽ ra được host nguồn.
- Tìm `target_hostname` có tồn tại trong cluster không, sẽ được thông tin của host đích.
- Thực hiện migrate thì xóa `VM` ở `host` nguồn đi, add `VM` đấy vào `host` đích.

### Update thông tin VM theo thời gian:

Khi bắt đầu khởi tạo cluster, có một bộ đếm timer để track thời gian, mỗi khi muốn cập nhật thì truyền timer vào hàm dưới đây là xong.
```python
def update_vm_metrics_after_timer(self, timestamp_input, timer, data_vm_path, data_host_path)
```