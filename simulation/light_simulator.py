"""Light Simulator - Mô phỏng thiết bị đèn."""

from typing import Dict, Any
from .base_device import BaseDevice


class Light(BaseDevice):
    """Mô phỏng thiết bị đèn với khả năng điều chỉnh độ sáng."""
    
    def __init__(self, device_id: str, name: str, room: str, brightness: int = 100):
        """Khởi tạo đèn.
        
        Args:
            device_id: ID duy nhất của đèn
            name: Tên đèn
            room: Phòng chứa đèn
            brightness: Độ sáng ban đầu (0-100)
        """
        super().__init__(device_id, name, room)
        self._brightness = max(0, min(100, brightness))  # Clamp 0-100
    
    @property
    def brightness(self) -> int:
        """Lấy độ sáng hiện tại."""
        return self._brightness
    
    def turn_on(self) -> bool:
        """Bật đèn.
        
        Returns:
            True (luôn thành công)
        """
        self.is_on = True
        self._update_timestamp()
        print(f"💡 {self.name} đã BẬT (Độ sáng: {self._brightness}%)")
        return True
    
    def turn_off(self) -> bool:
        """Tắt đèn.
        
        Returns:
            True (luôn thành công)
        """
        self.is_on = False
        self._update_timestamp()
        print(f"💡 {self.name} đã TẮT")
        return True
    
    def set_brightness(self, level: int) -> bool:
        """Điều chỉnh độ sáng của đèn.
        
        Args:
            level: Mức độ sáng (0-100)
            
        Returns:
            True nếu thành công, False nếu giá trị không hợp lệ
        """
        if not 0 <= level <= 100:
            print(f"⚠️ Độ sáng phải trong khoảng 0-100, nhận: {level}")
            return False
        
        self._brightness = level
        self._update_timestamp()
        
        if self.is_on:
            print(f"💡 {self.name} - Độ sáng: {self._brightness}%")
        else:
            print(f"💡 {self.name} - Độ sáng đặt: {self._brightness}% (đèn đang tắt)")
        
        return True
    
    def get_status(self) -> Dict[str, Any]:
        """Lấy trạng thái chi tiết của đèn.
        
        Returns:
            Dictionary chứa thông tin trạng thái bao gồm độ sáng
        """
        status = super().get_status()
        status['brightness'] = self._brightness
        status['device_type'] = 'light'
        return status
    
    def __str__(self) -> str:
        """String representation."""
        status = f"BẬT ({self._brightness}%)" if self.is_on else "TẮT"
        return f"💡 {self.name} ({self.room}) - {status}"

