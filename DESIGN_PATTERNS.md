# 🎨 Design Patterns - Smart Home Controller

Tài liệu này giải thích chi tiết các Design Patterns được sử dụng trong dự án.

---

## 1. 🔷 Singleton Pattern


### Vị trí:
- `application/device_controller.py` - Class `DeviceController`
- `presentation/main_window.py`, `dialogs/`, `panels/` - GUI module hóa

### Mục đích:
Đảm bảo chỉ có **1 instance duy nhất** của DeviceController trong toàn bộ ứng dụng.


### Implementation:

```python
class DeviceController:
    _instance = None  # Class variable lưu instance
    
    def __new__(cls):
        """Override __new__ để kiểm soát object creation."""
        if cls._instance is None:
            cls._instance = super(DeviceController, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Chỉ khởi tạo 1 lần."""
        if self._initialized:
            return
        
        self.devices = {}
        self.observers = []
        self._initialized = True
```

### Lý do sử dụng:
- ✅ **Centralized control**: Tất cả components đều truy cập cùng 1 controller
- ✅ **Shared state**: Đảm bảo devices và observers được sync
- ✅ **Resource management**: Tránh tạo nhiều instance không cần thiết

### Test:
```python
controller1 = DeviceController()
controller2 = DeviceController()
print(controller1 is controller2)  # True - cùng 1 object!
```

---

## 2. 👁️ Observer Pattern


### Vị trí:
- `application/device_controller.py` - Class `Observer` (interface)
- `presentation/main_window.py`, `panels/device_control_panel.py`, `room_visualization.py` - GUI đồng bộ qua observer

### Mục đích:
Cho phép GUI **tự động cập nhật** khi device thay đổi trạng thái, không cần polling.


### Implementation:

```python
# Observer interface
class Observer(ABC):
    @abstractmethod
    def update(self, device_id: str):
        pass

# Subject (DeviceController)
class DeviceController:
    def __init__(self):
        self.observers = []
    
    def register_observer(self, observer: Observer):
        self.observers.append(observer)
    
    def notify_observers(self, device_id: str):
        for observer in self.observers:
            observer.update(device_id)
    
    def control_device(self, device_id, command, params):
        # ... thực thi command ...
        if success:
            self.notify_observers(device_id)  # Notify!

# Observer implementation (GUI)
class MainWindow(tk.Tk, Observer):
    def update(self, device_id: str):
        """GUI tự động refresh khi nhận notify."""
        self.device_panels[device_id].update_display()
```


### Lý do sử dụng:
- Đồng bộ UI nhiều nơi: thay đổi từ popup, panel, sơ đồ phòng đều cập nhật ngay
- GUI module hóa, dễ mở rộng observer mới
- ✅ **Loose coupling**: GUI không cần biết về Device implementation
- ✅ **Real-time updates**: Không cần polling, tiết kiệm CPU
- ✅ **Scalable**: Dễ dàng thêm observers mới (VD: Logger, Database)

### Luồng hoạt động:
```
User Click Button → Controller.control_device()
    → Device thay đổi state
    → Controller.notify_observers()
    → GUI.update() được gọi tự động
    → GUI refresh display
```

---

## 3. 📋 Template Method Pattern

### Vị trí: `simulation/base_device.py` - Class `BaseDevice`

### Mục đích:
Định nghĩa **skeleton algorithm** cho tất cả devices, các subclass chỉ cần override các bước cụ thể.

### Implementation:

```python
# Abstract base class
class BaseDevice(ABC):
    def __init__(self, device_id, name, room):
        """Common initialization."""
        self.device_id = device_id
        self.name = name
        self.room = room
        self.is_on = False
    
    @abstractmethod
    def turn_on(self) -> bool:
        """Bắt buộc implement - specific cho từng device."""
        pass
    
    @abstractmethod
    def turn_off(self) -> bool:
        """Bắt buộc implement."""
        pass
    
    def get_status(self) -> Dict:
        """Common method - tất cả devices dùng chung."""
        return {
            'device_id': self.device_id,
            'name': self.name,
            'is_on': self.is_on
        }

# Concrete implementation
class Light(BaseDevice):
    def turn_on(self):
        """Light-specific implementation."""
        self.is_on = True
        print(f"💡 {self.name} đã BẬT")
        return True
```

### Lý do sử dụng:
- ✅ **Code reuse**: Logic chung (get_status) không bị duplicate
- ✅ **Enforce interface**: Bắt buộc subclass implement turn_on/turn_off
- ✅ **Polymorphism**: Controller làm việc với BaseDevice, không cần biết concrete type

### Class hierarchy:
```
BaseDevice (Abstract)
├── Light (brightness)
├── Fan (speed)
└── Door (lock/unlock)
```

---

## 4. 🧵 Concurrency Pattern (Threading)

### Vị trí: `application/timer_manager.py`

### Mục đích:
Chạy **timer tasks** trên background threads để không block GUI.

### Implementation:

```python
import threading

class TimerManager:
    def schedule_timer(self, device_id, action, delay_seconds):
        # Create callback
        def execute_timer():
            self._execute_timer(timer_id, device_id, action)
        
        # Create background thread
        timer_thread = threading.Timer(delay_seconds, execute_timer)
        timer_thread.start()  # Không block main thread
        
        return timer_id
    
    def _execute_timer(self, timer_id, device_id, action):
        """Chạy trên background thread."""
        self.controller.control_device(device_id, action)
        # Observer Pattern sẽ notify GUI thread-safe
```

### Thread Safety:

```python
from threading import Lock

class TimerManager:
    def __init__(self, controller):
        self._lock = Lock()  # Protect shared data
        self.active_timers = {}
    
    def cancel_timer(self, timer_id):
        with self._lock:  # Thread-safe access
            if timer_id in self.active_timers:
                task = self.active_timers[timer_id]
                task.cancel()
                del self.active_timers[timer_id]
```

### Lý do sử dụng:
- ✅ **Non-blocking**: GUI không bị freeze khi chờ timer
- ✅ **Concurrent execution**: Nhiều timers chạy song song
- ✅ **Background processing**: Timer tự động thực thi khi hết hạn

---

## 5. 🏗️ Layered Architecture Pattern

### Mục đích:
Tách biệt concerns thành các layers độc lập.

### Implementation:

```
┌─────────────────────────────────┐
│  PRESENTATION LAYER             │  ← User interaction
│  - GUI controls                 │
│  - Event handlers               │
│  - Display logic                │
└────────────┬────────────────────┘
             │ Commands/Queries
             ▼
┌─────────────────────────────────┐
│  APPLICATION LAYER              │  ← Business logic
│  - DeviceController (Singleton) │
│  - TimerManager (Threading)     │
│  - Observer management          │
└────────────┬────────────────────┘
             │ Control signals
             ▼
┌─────────────────────────────────┐
│  SIMULATION LAYER               │  ← Data/Model
│  - BaseDevice (Template Method) │
│  - Light, Fan, Door             │
│  - State management             │
└─────────────────────────────────┘
```

### Principles:
- **Separation of Concerns**: Mỗi layer có trách nhiệm riêng
- **Dependency Rule**: Layer trên phụ thuộc vào layer dưới (không ngược lại)
- **Interface-based**: Layers giao tiếp qua interfaces

---

## 6. 🗂️ Data Transfer Object (DTO)

### Vị trí: `application/timer_manager.py` - Class `TimerTask`

### Implementation:

```python
from dataclasses import dataclass

@dataclass
class TimerTask:
    """Pure data container - không có business logic."""
    timer_id: str
    device_id: str
    device_name: str
    action: str
    scheduled_time: datetime
    delay_seconds: int
    thread: threading.Timer
    
    def cancel(self):
        """Helper method."""
        self.thread.cancel()
```

### Lý do sử dụng:
- ✅ **Type safety**: Rõ ràng về structure
- ✅ **Immutable-ish**: @dataclass tạo __init__, __repr__ tự động
- ✅ **Documentation**: Code tự giải thích

---

## 📊 So sánh với các patterns khác

### Tại sao KHÔNG dùng Factory Pattern?

**Có thể dùng**, nhưng không cần thiết vì:
```python
# Hiện tại (đơn giản)
light = Light("light_001", "Đèn", "Phòng")

# Nếu dùng Factory (phức tạp hơn)
light = DeviceFactory.create("light", "light_001", "Đèn", "Phòng")
```

→ Số lượng device types ít (3), không cần abstraction thêm.

### Tại sao KHÔNG dùng Strategy Pattern?

**Không cần** vì behavior không thay đổi runtime:
- Light luôn có brightness
- Fan luôn có speed
- Door luôn có lock/unlock

→ Template Method đủ cho fixed behaviors.

### Tại sao KHÔNG dùng Command Pattern?

**Có thể dùng** cho undo/redo, nhưng requirements không yêu cầu:
```python
# Với Command Pattern (nếu cần undo)
class TurnOnCommand:
    def execute(self, device):
        device.turn_on()
    
    def undo(self, device):
        device.turn_off()
```

→ Đơn giản hóa vì không cần undo/redo.

---

## 🎯 Kết luận

### Patterns được sử dụng:
1. ✅ **Singleton** - DeviceController
2. ✅ **Observer** - GUI notifications
3. ✅ **Template Method** - BaseDevice hierarchy
4. ✅ **Layered Architecture** - 3-tier system
5. ✅ **Threading** - Timer background tasks
6. ✅ **DTO** - TimerTask data structure

### Lợi ích:
- 🎨 **Maintainable**: Code dễ đọc, dễ sửa
- 🔧 **Extensible**: Dễ thêm device mới
- 🧪 **Testable**: Mỗi layer test riêng
- 📚 **Educational**: Minh họa real-world patterns

### Áp dụng trong dự án khác:

**IoT Projects**: Reuse cả 3 layers
**GUI Apps**: Reuse Observer + Layered Architecture
**Background Jobs**: Reuse Threading pattern
**Device Management**: Reuse Template Method

---

**📖 Tài liệu tham khảo:**
- [Refactoring Guru - Design Patterns](https://refactoring.guru/design-patterns)
- [Python Design Patterns](https://python-patterns.guide/)
- [Gang of Four Book](https://en.wikipedia.org/wiki/Design_Patterns)
