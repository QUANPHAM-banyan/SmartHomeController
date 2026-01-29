# 🏠 Smart Home Controller

Hệ thống mô phỏng điều khiển thiết bị IoT trong gia đình (Smart Device Controller)

## 📋 Mô tả

Đây là một phần mềm mô phỏng hoàn toàn bằng Python, cho phép người dùng điều khiển các thiết bị IoT cơ bản trong gia đình như đèn, quạt, và cửa thông qua giao diện đồ họa (GUI).

### Tính năng chính:
- ✅ Điều khiển đèn (bật/tắt, điều chỉnh độ sáng 0-100%)
- ✅ Điều khiển quạt (bật/tắt, 3 mức tốc độ)
- ✅ Điều khiển cửa (mở/đóng/khóa/mở khóa)
- ✅ Hẹn giờ tự động bật/tắt thiết bị
- ✅ Hiển thị trạng thái real-time
- ✅ Giao diện trực quan, dễ sử dụng

## 🏗️ Kiến trúc hệ thống

Hệ thống được thiết kế theo **Layered Architecture** với 3 lớp:

```
┌─────────────────────────────────────┐
│   PRESENTATION LAYER (GUI)         │
│   - main_window.py                 │
│   - dialogs/, panels/ (modular GUI)│
│   - room_visualization.py          │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│   APPLICATION LAYER (Logic)        │
│   - device_controller.py           │
│   - timer_manager.py               │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│   SIMULATION LAYER (Devices)       │
│   - base_device.py                 │
│   - light_simulator.py             │
│   - fan_simulator.py               │
│   - door_simulator.py              │
└─────────────────────────────────────┘
```

### Design Patterns sử dụng:
- **Singleton Pattern**: DeviceController (1 instance duy nhất)
- **Observer Pattern**: Notify GUI khi device thay đổi
- **Template Method Pattern**: BaseDevice cho các thiết bị

## 📁 Cấu trúc thư mục

```
SmartHomeController/
├── main.py                     # Entry point
├── requirements.txt            # Dependencies (none - chỉ dùng built-in)
├── README.md                   # Tài liệu này
│
├── simulation/                 # Lớp mô phỏng thiết bị
│   ├── __init__.py
│   ├── base_device.py         # Abstract base class
│   ├── light_simulator.py     # Mô phỏng đèn
│   ├── fan_simulator.py       # Mô phỏng quạt
│   └── door_simulator.py      # Mô phỏng cửa
│
├── application/                # Lớp logic điều khiển
│   ├── __init__.py
│   ├── device_controller.py   # Controller chính (Singleton)
│   └── timer_manager.py       # Quản lý hẹn giờ
│
└── presentation/               # Lớp giao diện
    ├── __init__.py
    ├── main_window.py         # Cửa sổ chính (GUI)
    ├── dialogs/               # Dialogs (thêm/xóa/quản lý phòng)
    │    ├── __init__.py
    │    ├── add_device_dialog.py
    │    ├── delete_device_dialog.py
    │    └── room_manager_dialog.py
    ├── panels/                # Panels (điều khiển thiết bị, timer)
    │    ├── __init__.py
    │    ├── device_control_panel.py
    │    └── timer_panel.py
    └── room_visualization.py  # Hiển thị sơ đồ phòng
```

## 🚀 Cài đặt và Chạy

### Yêu cầu:
- Python 3.8 trở lên
- Tkinter (built-in với Python)

### Chạy ứng dụng:

```bash
# Clone hoặc download project
cd SmartHomeController

# Chạy trực tiếp
python main.py
```


**Không cần cài đặt gì thêm!** Tất cả đều dùng thư viện built-in của Python.

---

## 🆕 Tính năng giao diện mới

- Giao diện chia module: dễ bảo trì, mở rộng
- Sơ đồ phòng (Room Visualization) không giới hạn số hàng thiết bị
- Có thể resize chiều cao sơ đồ phòng bằng chuột (kéo thanh chia)
- Các thiết bị xếp từ trái sang phải, tự động xuống dòng
- Đồng bộ trạng thái thiết bị giữa popup, panel, sơ đồ phòng

## 📖 Hướng dẫn sử dụng

### 1. Điều khiển thiết bị cơ bản

Khi khởi động ứng dụng, bạn sẽ thấy:
- **Danh sách thiết bị** bên trái (mặc định có 7 thiết bị mẫu)
- **Panel hẹn giờ** bên phải
- **Trạng thái hệ thống** ở dưới cùng

Mỗi thiết bị có:
- **Nút Bật/Tắt**: Điều khiển trạng thái ON/OFF
- **Controls đặc thù**: 
  - Đèn: Thanh trượt điều chỉnh độ sáng
  - Quạt: Radio buttons chọn tốc độ (1, 2, 3)
  - Cửa: Nút Khóa/Mở khóa

### 2. Hẹn giờ thiết bị

1. Chọn thiết bị từ dropdown
2. Chọn hành động (turn_on hoặc turn_off)
3. Nhập thời gian (giây hoặc phút)
4. Click "⏰ Đặt hẹn giờ"

Timer sẽ tự động thực thi và cập nhật GUI.

### 3. Quan sát trạng thái

- **Màu xanh (🟢)**: Thiết bị đang bật
- **Màu xám (⚫)**: Thiết bị đang tắt
- Trạng thái cập nhật **real-time** khi có thay đổi

## 🧪 Ví dụ sử dụng API (Console)

```python
from simulation.light_simulator import Light
from application.device_controller import DeviceController

# Khởi tạo
controller = DeviceController()

# Tạo thiết bị
light = Light("light_001", "Đèn phòng khách", "Phòng khách")
controller.add_device(light)

# Điều khiển
controller.control_device("light_001", "turn_on")
controller.control_device("light_001", "set_brightness", {"level": 75})
controller.control_device("light_001", "turn_off")

# Lấy trạng thái
status = controller.get_device_status("light_001")
print(status)
# {'device_id': 'light_001', 'name': 'Đèn phòng khách', ...}
```

## 🔧 Mở rộng - Thêm thiết bị mới

Để thêm loại thiết bị mới (VD: Air Conditioner):

1. Tạo file `simulation/ac_simulator.py`:

```python
from simulation.base_device import BaseDevice

class AirConditioner(BaseDevice):
    def __init__(self, device_id, name, room, temperature=25):
        super().__init__(device_id, name, room)
        self.temperature = temperature
    
    def turn_on(self):
        self.is_on = True
        return True
    
    def turn_off(self):
        self.is_on = False
        return True
    
    def set_temperature(self, temp):
        if 16 <= temp <= 30:
            self.temperature = temp
            return True
        return False
```

2. Thêm vào `main.py`:

```python
from simulation.ac_simulator import AirConditioner

ac = AirConditioner("ac_001", "Máy lạnh phòng khách", "Phòng khách")
controller.add_device(ac)
```

3. Thêm GUI controls trong `presentation/gui.py`

**Không cần sửa DeviceController!** Nhờ polymorphism và Observer Pattern.

## 📊 Kiểm tra lỗi

Nếu gặp lỗi:

1. **Lỗi import**: Đảm bảo đang ở thư mục gốc `SmartHomeController`
2. **Lỗi Tkinter**: Cài đặt `python-tk` (trên Linux)
3. **Lỗi hiển thị emoji**: Một số terminal không hỗ trợ emoji, nhưng GUI vẫn hoạt động bình thường

## 📚 Tài liệu tham khảo

- **Design Patterns**: [Refactoring Guru](https://refactoring.guru/)
- **Python Tkinter**: [Official Documentation](https://docs.python.org/3/library/tkinter.html)
- **Threading**: [Python Threading Guide](https://docs.python.org/3/library/threading.html)

## 👨‍💻 Tác giả

Đồ án môn học - Đồ án thiết kế 1
Đề tài: Mô phỏng hệ thống điều khiển thiết bị IoT trong gia đình