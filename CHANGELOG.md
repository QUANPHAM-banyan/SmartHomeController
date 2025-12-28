# 📝 CHANGELOG - Smart Home Controller

## Version 1.1.0 - 2024 (Phiên bản mới nhất)

### ✨ Tính năng mới

#### 1. ⚙️ Quản lý thiết bị động
- **Thêm thiết bị**: Dialog với form chọn loại, tên, và phòng
- **Xóa thiết bị**: Dialog chọn thiết bị và xác nhận xóa
- **Menu quản lý**: Menu "Thiết bị" với các tùy chọn thêm/xóa/làm mới

#### 2. 🏠 Quản lý phòng
- **Lọc theo phòng**: Menu "Phòng" để lọc thiết bị theo từng phòng
- **Thêm phòng mới**: Tạo phòng mới khi thêm thiết bị
- **Sơ đồ phòng động**: Canvas tự động cập nhật theo phòng được chọn
- **Hiển thị tên phòng**: Title canvas thay đổi theo phòng hiện tại

#### 3. 🖱️ Click interaction với thiết bị
- **Click để điều khiển**: Click vào icon thiết bị trong sơ đồ phòng
- **Device Popup**: Popup điều khiển nhanh với:
  - Hiển thị trạng thái (🟢 Đang bật / 🔴 Đang tắt)
  - Nút bật/tắt nhanh
  - Controls đặc biệt (độ sáng, tốc độ, khóa)
- **Hover effect**: 
  - Icon được highlight khi di chuột qua
  - Cursor đổi thành `hand2` (pointer)
  - Border tăng độ dày lên 4px

#### 4. 📊 Cải tiến giao diện
- **Layout mới**: 
  - Sơ đồ phòng ở trên (trong LabelFrame)
  - Device panels và Timer panel ở dưới
  - Tăng kích thước cửa sổ: 1200x800
- **Room Canvas**: 
  - Hiển thị tên phòng hiện tại
  - Filter thiết bị theo phòng được chọn
  - Refresh tự động khi thêm/xóa thiết bị
- **Menu bar**: Thêm menu "Thiết bị", "Phòng", "Trợ giúp"

#### 5. 📖 Dialog và Popup
- **AddDeviceDialog**: 
  - Radio buttons chọn loại thiết bị (💡/🌀/🚪)
  - Entry nhập tên với suggestion tự động
  - Combobox chọn phòng + nút thêm phòng mới
  - Validation đầu vào
- **DeleteDeviceDialog**:
  - Listbox hiển thị tất cả thiết bị
  - Hiển thị tên, phòng, và loại thiết bị
  - Xác nhận trước khi xóa
- **DevicePopup**:
  - Hiển thị icon và tên thiết bị
  - Status indicator màu xanh/đỏ
  - Quick controls cho từng loại thiết bị
  - Tự động center relative to main window

### 🔧 Cải tiến kỹ thuật

- **DeviceController**:
  - Methods `add_device()` và `remove_device()` đã có sẵn
  - Notify observers khi xóa thiết bị
  
- **MainWindow**:
  - Thêm `current_room` property để track phòng hiện tại
  - Methods mới:
    - `_create_menu()`: Tạo menu bar
    - `_update_room_menu()`: Cập nhật danh sách phòng
    - `_filter_by_room()`: Lọc thiết bị theo phòng
    - `_on_add_device()`: Handler thêm thiết bị
    - `_on_remove_device()`: Handler xóa thiết bị
    - `_refresh_all()`: Làm mới toàn bộ UI
    - `_refresh_device_panels()`: Làm mới panels với filter
    - `_show_help()`, `_show_about()`: Hiển thị trợ giúp
  - Observer pattern: Cập nhật cả RoomCanvas khi device thay đổi

- **RoomCanvas**:
  - Constructor nhận `current_room` parameter
  - Methods mới:
    - `set_room()`: Đổi phòng hiển thị
    - `_on_device_click()`: Handler click vào thiết bị
    - `_on_hover_enter()`, `_on_hover_leave()`: Hover effects
  - Bind events cho click và hover
  - Filter thiết bị theo `current_room` trong `_place_devices()`
  - Update title với tên phòng trong `_draw_room()`

### 📦 Files mới

- `USER_GUIDE.md`: Hướng dẫn sử dụng chi tiết
- `CHANGELOG.md`: File này, ghi nhận lịch sử phát triển

### 🐛 Bug fixes

- Fix: Observer pattern giờ cập nhật cả RoomCanvas
- Fix: Device panels được refresh đúng khi lọc theo phòng
- Fix: Timer panel refresh device list khi thêm/xóa thiết bị

---

## Version 1.0.0 - 2024 (Phiên bản đầu tiên)

### 🎉 Tính năng cốt lõi

#### 1. 🏗️ Kiến trúc 3 lớp
- **Simulation Layer**: BaseDevice, Light, Fan, Door
- **Application Layer**: DeviceController (Singleton), TimerManager (Threading)
- **Presentation Layer**: MainWindow, DeviceControlPanel, TimerPanel, RoomCanvas

#### 2. 🎮 Điều khiển thiết bị cơ bản
- Đèn: Bật/Tắt, Độ sáng 0-100%
- Quạt: Bật/Tắt, 3 tốc độ
- Cửa: Mở/Đóng/Khóa/Mở khóa

#### 3. ⏰ Hệ thống hẹn giờ
- TimerManager với threading.Timer
- Schedule bật/tắt thiết bị
- Xem và hủy timer đang chạy

#### 4. 📊 Giao diện GUI
- Tkinter với ttk widgets
- Device control panels
- Timer management panel
- Room visualization canvas
- Status bar

#### 5. 🎨 Design Patterns
- **Singleton Pattern**: DeviceController
- **Observer Pattern**: Notify GUI khi device thay đổi
- **Template Method Pattern**: BaseDevice hierarchy

#### 6. 📚 Documentation
- `README.md`: Tổng quan hệ thống
- `DESIGN_PATTERNS.md`: Giải thích patterns
- PlantUML diagrams trong documentation
- Demo scripts (`demo.py`) với 5 demos

### 📦 Files ban đầu

**Simulation Layer:**
- `simulation/base_device.py`
- `simulation/light_simulator.py`
- `simulation/fan_simulator.py`
- `simulation/door_simulator.py`

**Application Layer:**
- `application/device_controller.py`
- `application/timer_manager.py`

**Presentation Layer:**
- `presentation/gui.py`
- `presentation/room_visualization.py`

**Entry point:**
- `main.py`
- `demo.py`

**Configuration:**
- `requirements.txt`
- `.gitignore`

### ⚙️ Dependencies
- Python 3.8+
- Zero external dependencies (chỉ dùng standard library)

---

## 🔮 Roadmap (Tương lai)

### Version 1.2.0 (Đề xuất)
- [ ] Lưu/Load cấu hình thiết bị từ JSON
- [ ] Multi-floor support (nhiều tầng nhà)
- [ ] Sensor devices (temperature, humidity)
- [ ] Scheduling theo lịch (daily, weekly)
- [ ] Dark mode theme
- [ ] Export reports (Excel, PDF)

### Version 1.3.0 (Đề xuất)
- [ ] Undo/Redo functionality
- [ ] Device groups/scenes
- [ ] Voice control simulation
- [ ] Energy consumption tracking
- [ ] Mobile-like responsive layout

### Version 2.0.0 (Đề xuất)
- [ ] Web interface (Flask/FastAPI)
- [ ] REST API
- [ ] Database integration (SQLite)
- [ ] Multi-user support
- [ ] Real IoT device integration (MQTT, HTTP)

---

## 📊 Statistics

### Version 1.1.0
- **Lines of code**: ~1200
- **Files**: 12
- **Classes**: 15+
- **Functions/Methods**: 80+
- **Devices supported**: 3 types
- **Design patterns**: 3

### Version 1.0.0
- **Lines of code**: ~900
- **Files**: 11
- **Classes**: 12
- **Functions/Methods**: 60+

---

## 🙏 Credits

**Development**: Smart Home Project Team  
**Language**: Python 3.8+  
**GUI Framework**: Tkinter  
**License**: MIT (đề xuất)

---

**Last updated**: 2024  
**Current version**: 1.1.0
