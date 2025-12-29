"""Device Controller - Quản lý tập trung tất cả thiết bị."""

from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod


class Observer(ABC):
    """Observer interface cho Observer Pattern.
    
    Các GUI components sẽ implement interface này để nhận thông báo
    khi thiết bị thay đổi trạng thái.
    """
    
    @abstractmethod
    def update(self, device_id: str):
        """Gọi khi thiết bị thay đổi trạng thái.
        
        Args:
            device_id: ID của thiết bị đã thay đổi
        """
        pass


class DeviceController:
    """Controller quản lý tất cả thiết bị IoT.
    
    Sử dụng Singleton Pattern để đảm bảo chỉ có 1 instance duy nhất.
    Sử dụng Observer Pattern để notify GUI khi có thay đổi.
    """
    
    _instance = None  # Singleton instance
    
    def __new__(cls):
        """Implement Singleton Pattern."""
        if cls._instance is None:
            cls._instance = super(DeviceController, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Khởi tạo controller (chỉ chạy 1 lần)."""
        if self._initialized:
            return
        
        self.devices: Dict[str, Any] = {}  # {device_id: device_object}
        self.observers: List[Observer] = []  # Danh sách observers
        self._initialized = True
        print("✅ DeviceController đã khởi tạo (Singleton)")
    
    def add_device(self, device) -> bool:
        """Thêm thiết bị vào hệ thống.
        
        Args:
            device: Đối tượng thiết bị (kế thừa từ BaseDevice)
            
        Returns:
            True nếu thành công, False nếu device_id đã tồn tại
        """
        if device.device_id in self.devices:
            print(f"⚠️ Thiết bị ID '{device.device_id}' đã tồn tại")
            return False
        
        self.devices[device.device_id] = device
        print(f"✅ Đã thêm thiết bị: {device}")
        return True
    
    def remove_device(self, device_id: str) -> bool:
        """Xóa thiết bị khỏi hệ thống.
        
        Args:
            device_id: ID của thiết bị cần xóa
            
        Returns:
            True nếu thành công, False nếu không tìm thấy
        """
        if device_id not in self.devices:
            print(f"⚠️ Không tìm thấy thiết bị ID: {device_id}")
            return False
        
        device = self.devices.pop(device_id)
        print(f"🗑️ Đã xóa thiết bị: {device.name}")
        self.notify_observers(device_id)
        return True
    
    def control_device(self, device_id: str, command: str, params: Optional[Dict] = None) -> bool:
        """Điều khiển thiết bị.
        
        Args:
            device_id: ID của thiết bị
            command: Lệnh điều khiển (turn_on, turn_off, set_brightness, v.v.)
            params: Tham số bổ sung (VD: {"brightness": 80})
            
        Returns:
            True nếu thành công, False nếu thất bại
        """
        # Validate device exists
        if device_id not in self.devices:
            print(f"❌ Không tìm thấy thiết bị ID: {device_id}")
            return False
        
        device = self.devices[device_id]
        params = params or {}
        
        try:
            # Execute command
            if command == "turn_on":
                result = device.turn_on()
            elif command == "turn_off":
                result = device.turn_off()
            elif command == "set_brightness":
                if hasattr(device, 'set_brightness'):
                    result = device.set_brightness(params.get('brightness', 100))
                else:
                    print(f"❌ Thiết bị {device.name} không hỗ trợ set_brightness")
                    return False
            elif command == "set_speed":
                if hasattr(device, 'set_speed'):
                    result = device.set_speed(params.get('speed', 1))
                else:
                    print(f"❌ Thiết bị {device.name} không hỗ trợ set_speed")
                    return False
            elif command == "lock":
                if hasattr(device, 'lock'):
                    result = device.lock()
                else:
                    print(f"❌ Thiết bị {device.name} không hỗ trợ lock")
                    return False
            elif command == "unlock":
                if hasattr(device, 'unlock'):
                    result = device.unlock()
                else:
                    print(f"❌ Thiết bị {device.name} không hỗ trợ unlock")
                    return False
            elif command == "open":
                if hasattr(device, 'open'):
                    result = device.open()
                else:
                    print(f"❌ Thiết bị {device.name} không hỗ trợ open")
                    return False
            elif command == "close":
                if hasattr(device, 'close'):
                    result = device.close()
                else:
                    print(f"❌ Thiết bị {device.name} không hỗ trợ close")
                    return False
            else:
                print(f"❌ Lệnh không hợp lệ: {command}")
                return False
            
            # Notify observers if command succeeded
            if result:
                self.notify_observers(device_id)
            
            return result
            
        except Exception as e:
            print(f"❌ Lỗi khi thực thi lệnh '{command}': {e}")
            return False
    
    def get_device(self, device_id: str):
        """Lấy đối tượng thiết bị.
        
        Args:
            device_id: ID của thiết bị
            
        Returns:
            Đối tượng thiết bị hoặc None nếu không tìm thấy
        """
        return self.devices.get(device_id)
    
    def get_device_status(self, device_id: str) -> Optional[Dict[str, Any]]:
        """Lấy trạng thái của thiết bị.
        
        Args:
            device_id: ID của thiết bị
            
        Returns:
            Dictionary chứa trạng thái hoặc None nếu không tìm thấy
        """
        device = self.devices.get(device_id)
        if device:
            return device.get_status()
        return None
    
    def get_all_devices(self) -> List:
        """Lấy danh sách tất cả thiết bị.
        
        Returns:
            List các đối tượng thiết bị
        """
        return list(self.devices.values())
    
    def get_devices_by_room(self, room: str) -> List:
        """Lấy tất cả thiết bị trong một phòng.
        
        Args:
            room: Tên phòng
            
        Returns:
            List các thiết bị trong phòng đó
        """
        return [device for device in self.devices.values() if device.room == room]
    
    def get_devices_by_type(self, device_type: str) -> List:
        """Lấy tất cả thiết bị theo loại.
        
        Args:
            device_type: Loại thiết bị ('light', 'fan', 'door')
            
        Returns:
            List các thiết bị cùng loại
        """
        return [
            device for device in self.devices.values()
            if device.get_status().get('device_type') == device_type
        ]
    
    # Observer Pattern Methods
    
    def register_observer(self, observer: Observer):
        """Đăng ký observer.
        
        Args:
            observer: Đối tượng implement Observer interface
        """
        if observer not in self.observers:
            self.observers.append(observer)
            print(f"👁️ Đã đăng ký observer: {observer.__class__.__name__}")
    
    def unregister_observer(self, observer: Observer):
        """Hủy đăng ký observer.
        
        Args:
            observer: Đối tượng cần hủy đăng ký
        """
        if observer in self.observers:
            self.observers.remove(observer)
            print(f"👁️ Đã hủy đăng ký observer: {observer.__class__.__name__}")
    
    def notify_observers(self, device_id: str):
        """Thông báo cho tất cả observers về sự thay đổi.
        
        Args:
            device_id: ID của thiết bị đã thay đổi
        """
        for observer in self.observers:
            try:
                observer.update(device_id)
            except Exception as e:
                print(f"❌ Lỗi khi notify observer {observer.__class__.__name__}: {e}")
    
    def get_summary(self) -> Dict[str, Any]:
        """Lấy thông tin tổng quan về hệ thống.
        
        Returns:
            Dictionary chứa thống kê hệ thống
        """
        total = len(self.devices)
        on_count = sum(1 for d in self.devices.values() if d.is_on)
        off_count = total - on_count
        
        return {
            'total_devices': total,
            'devices_on': on_count,
            'devices_off': off_count,
            'rooms': list(set(d.room for d in self.devices.values())),
            'observers_count': len(self.observers)
        }
    
    def print_summary(self):
        """In ra thông tin tổng quan."""
        summary = self.get_summary()
        print("\n" + "="*50)
        print("        THÔNG TIN HỆ THỐNG")
        print("="*50)
        print(f"Tổng số thiết bị: {summary['total_devices']}")
        print(f"  - Đang bật: {summary['devices_on']}")
        print(f"  - Đang tắt: {summary['devices_off']}")
        print(f"Số phòng: {len(summary['rooms'])}")
        print(f"Observers: {summary['observers_count']}")
        print("="*50 + "\n")

