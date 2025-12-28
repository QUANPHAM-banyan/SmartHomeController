"""Fan Simulator - Mô phỏng thiết bị quạt."""

from typing import Dict, Any
from .base_device import BaseDevice


class Fan(BaseDevice):
    """Mô phỏng thiết bị quạt với 3 mức tốc độ."""
    
    # Constants cho tốc độ
    SPEED_LOW = 1
    SPEED_MEDIUM = 2
    SPEED_HIGH = 3
    
    SPEED_NAMES = {
        SPEED_LOW: "Thấp",
        SPEED_MEDIUM: "Trung bình",
        SPEED_HIGH: "Cao"
    }
    
    def __init__(self, device_id: str, name: str, room: str, speed: int = SPEED_LOW):
        """Khởi tạo quạt.
        
        Args:
            device_id: ID duy nhất của quạt
            name: Tên quạt
            room: Phòng chứa quạt
            speed: Tốc độ ban đầu (1, 2, hoặc 3)
        """
        super().__init__(device_id, name, room)
        self._speed = speed if speed in [1, 2, 3] else self.SPEED_LOW
    
    @property
    def speed(self) -> int:
        """Lấy tốc độ hiện tại."""
        return self._speed
    
    def turn_on(self) -> bool:
        """Bật quạt.
        
        Returns:
            True (luôn thành công)
        """
        self.is_on = True
        self._update_timestamp()
        speed_name = self.SPEED_NAMES.get(self._speed, "Không xác định")
        print(f"🌀 {self.name} đã BẬT - Tốc độ: {speed_name} ({self._speed})")
        return True
    
    def turn_off(self) -> bool:
        """Tắt quạt.
        
        Returns:
            True (luôn thành công)
        """
        self.is_on = False
        self._update_timestamp()
        print(f"🌀 {self.name} đã TẮT")
        return True
    
    def set_speed(self, speed: int) -> bool:
        """Điều chỉnh tốc độ quạt.
        
        Args:
            speed: Tốc độ mong muốn (1=Thấp, 2=Trung bình, 3=Cao)
            
        Returns:
            True nếu thành công, False nếu giá trị không hợp lệ
        """
        if speed not in [self.SPEED_LOW, self.SPEED_MEDIUM, self.SPEED_HIGH]:
            print(f"⚠️ Tốc độ phải là 1, 2, hoặc 3, nhận: {speed}")
            return False
        
        self._speed = speed
        self._update_timestamp()
        
        speed_name = self.SPEED_NAMES[speed]
        if self.is_on:
            print(f"🌀 {self.name} - Tốc độ: {speed_name} ({speed})")
        else:
            print(f"🌀 {self.name} - Tốc độ đặt: {speed_name} ({speed}) (quạt đang tắt)")
        
        return True
    
    def increase_speed(self) -> bool:
        """Tăng tốc độ lên 1 cấp.
        
        Returns:
            True nếu tăng được, False nếu đã ở mức cao nhất
        """
        if self._speed >= self.SPEED_HIGH:
            print(f"🌀 {self.name} - Đã ở tốc độ cao nhất")
            return False
        return self.set_speed(self._speed + 1)
    
    def decrease_speed(self) -> bool:
        """Giảm tốc độ xuống 1 cấp.
        
        Returns:
            True nếu giảm được, False nếu đã ở mức thấp nhất
        """
        if self._speed <= self.SPEED_LOW:
            print(f"🌀 {self.name} - Đã ở tốc độ thấp nhất")
            return False
        return self.set_speed(self._speed - 1)
    
    def get_status(self) -> Dict[str, Any]:
        """Lấy trạng thái chi tiết của quạt.
        
        Returns:
            Dictionary chứa thông tin trạng thái bao gồm tốc độ
        """
        status = super().get_status()
        status['speed'] = self._speed
        status['speed_name'] = self.SPEED_NAMES[self._speed]
        status['device_type'] = 'fan'
        return status
    
    def __str__(self) -> str:
        """String representation."""
        if self.is_on:
            speed_name = self.SPEED_NAMES[self._speed]
            return f"🌀 {self.name} ({self.room}) - BẬT (Tốc độ: {speed_name})"
        else:
            return f"🌀 {self.name} ({self.room}) - TẮT"

