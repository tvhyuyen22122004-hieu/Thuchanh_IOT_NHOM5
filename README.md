# Báo cáo Thực hành Lập trình Python với Giao thức CoAP

## 1. Thông tin chung

| Họ và tên | Mã sinh viên |
|---|---|
| Trần Văn Hiếu | B23DCCN313 |
| Nguyễn Viết Tỉnh | B23DCCN825 |

| Môn học | Giao thức sử dụng |
|---|---|
| Internet of Things IoT | CoAP qua UDP localhost 5683 |

Thông tin gửi ở Bài 1 có thể thay đổi trong `coap_client_bai1.py`.

## Môi trường

- Python 3.9 trở lên
- Thư viện: `aiocoap`
- Dia chi Server: `127.0.0.1`
- Cong CoAP UDP: `5683`

Cài đặt thư viện:

```powershell
py -m pip install -r requirements.txt
```

Nếu máy tính chưa có Python, hãy cài Python 3 và chọn tùy chọn thêm Python vào PATH.

## Bài 1. Gửi và nhận thông điệp CoAP

Terminal 1:

```powershell
py coap_server_bai1.py
```

Terminal 2:

```powershell
py coap_client_bai1.py
```

URI: `coap://127.0.0.1:5683/iot/lab/message`

Server xu ly GET va POST, in noi dung POST cung thoi diem nhan. GET tra ve loi chao va kem thong diep POST gan nhat neu co.

## Bài 2. Giám sát cảm biến nhiệt độ và độ ẩm

Terminal 1:

```powershell
py sensor_server_bai2.py
```

Terminal 2:

```powershell
py monitor_client_bai2.py
```

URI: `coap://127.0.0.1:5683/iot/lab/sensor01/data`

Sensor Server cap nhat du lieu moi sau moi 3 giay va tra JSON. Monitoring Client truy van moi 3 giay, hien thi du lieu va canh bao khi nhiet do tren 35 C hoac do am duoi 40 %.

## Bài 3. Giám sát và điều khiển đèn với CoAP Observe

Terminal 1:

```powershell
py light_server_bai3.py
```

Terminal 2:

```powershell
py light_monitor_bai3.py
```

Terminal 3:

```powershell
py light_controller_bai3.py
```

URI: `coap://127.0.0.1:5683/iot/lab/light01/status`

Controller chấp nhận `ON`, `OFF`, `STATUS`, `EXIT`. `ON`/`OFF` gửi yêu cầu PUT; `STATUS` đọc trạng thái bằng GET. Monitoring Client đăng ký CoAP Observe nên nhận thông báo khi trạng thái thay đổi, không dùng GET định kỳ. Nhấn Ctrl+C để dừng chương trình.

## Kết quả đạt được

- Bài 1: Client GET và POST thành công; Server phản hồi và lưu thông điệp gần nhất.
- Bài 2: Server trả dữ liệu JSON cho cảm biến `sensor01`; Client hiển thị và cảnh báo theo ngưỡng.
- Bài 3: Controller thay đổi trạng thái bằng PUT; Monitoring Client nhận thông báo qua CoAP Observe khi trạng thái thay đổi.

Khi chay tren hai may khac nhau, thay `127.0.0.1` trong cac file Client bang IP cua may chay Server va cho phep UDP cong 5683 tren tuong lua.
