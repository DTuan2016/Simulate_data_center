# SIMULATE DATA CENTER
Mô phỏng cơ bản về một data center gồm nhiều host, mỗi host gồm các VM (virtual machine).
Trong mô phỏng này, tôi mô phỏng việc migrate VM giữa các host khác nhau.
Cũng có một file run.py để chạy thử chương trình.

## Clone dự án:
```bash
https://github.com/DTuan2016/Simulate_data_center.git
cd Simulate_data_center
```
## Tạo môi trường ảo
Trong dự án này của tôi dùng python3.11.0 

### Tạo môi trường trong thư mục trên:
```bash
python -m venv venv
```
### Với Windows:
```bash
venv\Scripts\activate
```
### Với Linux:
```bash
source venv/bin/activate
```
### Cài các thư mục phụ thuộc:
```bash
pip install -r requirements.txt
```
## Documentations: [Tại đây](https://github.com/DTuan2016/Simulate_data_center/blob/master/doc/documentation.md)
