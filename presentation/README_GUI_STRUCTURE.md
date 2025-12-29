# 📂 Cấu trúc GUI mới - Hướng dẫn sử dụng

## 🎯 Tổng quan
File `gui.py` gốc (1221 dòng) đã được chia thành cấu trúc module để dễ bảo trì và phát triển hơn.

## 📁 Cấu trúc thư mục

```
presentation/
├── __init__.py                 # Package exports
├── gui.py                      # Backward compatibility (DEPRECATED)
├── main_window.py             # Cửa sổ chính (MainWindow)
├── room_visualization.py      # Hiển thị sơ đồ phòng (unchanged)
│
├── dialogs/                   # Các dialog (hộp thoại)
│   ├── __init__.py
│   ├── add_device_dialog.py    # Dialog thêm thiết bị
│   ├── delete_device_dialog.py # Dialog xóa thiết bị
│   └── room_manager_dialog.py  # Dialog quản lý phòng
│
└── panels/                    # Các panel (bảng điều khiển)
    ├── __init__.py
    ├── device_control_panel.py # Panel điều khiển từng thiết bị
    └── timer_panel.py          # Panel quản lý hẹn giờ
```

## 📦 Các module

### 1. **dialogs/** - Các hộp thoại

#### `add_device_dialog.py`
- **Class**: `AddDeviceDialog`
- **Chức năng**: Dialog để thêm thiết bị mới
- **Tính năng**:
  - Chọn loại thiết bị (Đèn/Quạt/Cửa)
  - Nhập tên và ID thiết bị
  - Chọn hoặc tạo phòng mới
  - Validation dữ liệu đầu vào

#### `delete_device_dialog.py`
- **Class**: `DeleteDeviceDialog`
- **Chức năng**: Dialog để xóa thiết bị
- **Tính năng**:
  - Hiển thị danh sách thiết bị
  - Xác nhận trước khi xóa

#### `room_manager_dialog.py`
- **Class**: `RoomManagerDialog`
- **Chức năng**: Dialog quản lý phòng
- **Tính năng**:
  - Thêm phòng mới
  - Đổi tên phòng
  - Xóa phòng (nếu không có thiết bị)
  - Hiển thị số lượng thiết bị trong mỗi phòng

### 2. **panels/** - Các bảng điều khiển

#### `device_control_panel.py`
- **Class**: `DeviceControlPanel`
- **Chức năng**: Card điều khiển từng thiết bị
- **Tính năng**:
  - Hiển thị thông tin thiết bị
  - Nút bật/tắt
  - Controls đặc thù cho từng loại thiết bị:
    - **Đèn**: Thanh trượt điều chỉnh độ sáng
    - **Quạt**: Nút chọn tốc độ (1-2-3)
    - **Cửa**: Nút mở/đóng và khóa/mở khóa
  - Cập nhật tự động khi thiết bị thay đổi (Observer pattern)

#### `timer_panel.py`
- **Class**: `TimerPanel`
- **Chức năng**: Panel quản lý hẹn giờ
- **Tính năng**:
  - Chọn thiết bị và hành động
  - Đặt thời gian hẹn giờ (giây/phút)
  - Hiển thị danh sách timers đang chạy
  - Hủy timer

### 3. **main_window.py** - Cửa sổ chính

#### `MainWindow`
- **Class**: `MainWindow(tk.Tk, Observer)`
- **Chức năng**: Cửa sổ chính của ứng dụng
- **Tính năng**:
  - Menu bar (Thiết bị, Phòng, Trợ giúp)
  - Sơ đồ phòng trực quan
  - Grid layout động cho device panels
  - Lọc thiết bị theo phòng
  - Status bar
  - Observer pattern để cập nhật UI

## 🔄 Cách sử dụng

### Import cách mới (khuyến nghị)

```python
# Import trực tiếp từ các module mới
from presentation.main_window import MainWindow
from presentation.dialogs import AddDeviceDialog, DeleteDeviceDialog, RoomManagerDialog
from presentation.panels import DeviceControlPanel, TimerPanel

# Sử dụng
app = MainWindow(controller, timer_manager)
app.run()
```

### Import cách cũ (vẫn hoạt động, backward compatibility)

```python
# Import từ gui.py (được giữ lại để tương thích)
from presentation.gui import MainWindow

# Hoặc
from presentation import MainWindow

# Vẫn hoạt động bình thường
app = MainWindow(controller, timer_manager)
app.run()
```

## ✅ Lợi ích của cấu trúc mới

1. **Dễ bảo trì**: Mỗi class trong file riêng, dễ tìm và sửa lỗi
2. **Dễ mở rộng**: Thêm dialog/panel mới mà không ảnh hưởng code cũ
3. **Dễ test**: Test từng component độc lập
4. **Dễ làm việc nhóm**: Nhiều người có thể làm việc trên các file khác nhau
5. **Code rõ ràng hơn**: Mỗi file có một trách nhiệm cụ thể
6. **Backward compatible**: Code cũ vẫn chạy được mà không cần thay đổi

## 🚀 Chạy thử

```bash
# Chạy ứng dụng (không cần thay đổi gì)
python main.py
```

File `main.py` vẫn import từ `presentation.gui`, nhưng bây giờ `gui.py` chỉ đóng vai trò re-export từ các module mới. Tất cả chức năng vẫn hoạt động bình thường!

## 📝 Notes

- File `gui.py` cũ được giữ lại để **backward compatibility**
- Có thể xóa code legacy trong `gui.py` sau khi đảm bảo tất cả code đều dùng import mới
- Tất cả imports và functionality đều được preserve hoàn toàn
- Không có breaking changes!

## 🔮 Tương lai

Nếu muốn hoàn toàn loại bỏ `gui.py`:

1. Cập nhật `main.py`:
   ```python
   from presentation.main_window import MainWindow
   # hoặc
   from presentation import MainWindow
   ```

2. Xóa hoặc đổi tên `gui.py` thành `gui_legacy.py`

Nhưng hiện tại không cần thiết - cấu trúc hiện tại đã tối ưu!
