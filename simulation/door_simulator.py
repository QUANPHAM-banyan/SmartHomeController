"""Door Simulator - Mô phỏng cửa thông minh."""

from typing import Dict, Any
from .base_device import BaseDevice


class Door(BaseDevice):
    """Mô phỏng cửa thông minh với khả năng đóng/mở/khóa."""
    
    # Constants cho trạng thái cửa
    STATE_CLOSED = "closed"
    STATE_OPEN = "open"
    STATE_LOCKED = "locked"
    
    STATE_NAMES = {
        STATE_CLOSED: "Đóng",
        STATE_OPEN: "Mở",
        STATE_LOCKED: "Khóa"
    }
    
    def __init__(self, device_id: str, name: str, room: str):
        """Khởi tạo cửa.
        
        Args:
            device_id: ID duy nhất của cửa
            name: Tên cửa
            room: Phòng chứa cửa
        """
        super().__init__(device_id, name, room)
        self.state = self.STATE_CLOSED
        self.is_locked = False
        self.is_on = False  # False = closed/locked, True = open
    
    def turn_on(self) -> bool:
        """Mở cửa (wrapper cho phương thức open()).
        
        Returns:
            True nếu thành công, False nếu cửa đang khóa
        """
        return self.open()
    
    def turn_off(self) -> bool:
        """Đóng cửa (wrapper cho phương thức close()).
        
        Returns:
            True (luôn thành công)
        """
        return self.close()
    
    def open(self) -> bool:
        """Mở cửa.
        
        Returns:
            True nếu thành công, False nếu cửa đang khóa
        """
        if self.is_locked:
            print(f"🚪 {self.name} - KHÔNG THỂ MỞ: Cửa đang khóa 🔒")
            return False
        
        if self.state == self.STATE_OPEN:
            print(f"🚪 {self.name} - Cửa đã mở rồi")
            return True
        
        self.state = self.STATE_OPEN
        self.is_on = True
        self._update_timestamp()
        print(f"🚪 {self.name} đã MỞ")
        return True
    
    def close(self) -> bool:
        """Đóng cửa.
        
        Returns:
            True (luôn thành công)
        """
        if self.state == self.STATE_CLOSED:
            print(f"🚪 {self.name} - Cửa đã đóng rồi")
            return True
        
        # Nếu đang khóa, chỉ cần chuyển về closed (mở khóa)
        if self.is_locked:
            self.is_locked = False
        
        self.state = self.STATE_CLOSED
        self.is_on = False
        self._update_timestamp()
        print(f"🚪 {self.name} đã ĐÓNG")
        return True
    
    def lock(self) -> bool:
        """Khóa cửa.
        
        Chỉ có thể khóa khi cửa đang đóng.
        
        Returns:
            True nếu thành công, False nếu cửa đang mở
        """
        if self.state == self.STATE_OPEN:
            print(f"🚪 {self.name} - KHÔNG THỂ KHÓA: Cửa đang mở")
            print(f"   Vui lòng đóng cửa trước khi khóa")
            return False
        
        if self.is_locked:
            print(f"🚪 {self.name} - Cửa đã khóa rồi 🔒")
            return True
        
        self.is_locked = True
        self.state = self.STATE_LOCKED
        self.is_on = False
        self._update_timestamp()
        print(f"🔒 {self.name} đã KHÓA")
        return True
    
    def lock_with_close(self) -> bool:
        """Đóng cửa (nếu đang mở) và khóa.
        
        Phương thức này được sử dụng cho hẹn giờ khóa cửa,
        đảm bảo cửa sẽ đóng và khóa bất kể trạng thái hiện tại.
        
        Returns:
            True (luôn thành công)
        """
        # Nếu cửa đang mở, đóng lại trước
        if self.state == self.STATE_OPEN:
            print(f"🚪 {self.name} - Đang đóng cửa trước khi khóa...")
            self.state = self.STATE_CLOSED
            self.is_on = False
        
        # Khóa cửa
        if not self.is_locked:
            self.is_locked = True
            self.state = self.STATE_LOCKED
            self._update_timestamp()
            print(f"🔒 {self.name} đã ĐÓNG VÀ KHÓA")
        else:
            print(f"🔒 {self.name} đã KHÓA (cửa đã khóa từ trước)")
        
        return True
    
    def unlock(self) -> bool:
        """Mở khóa cửa.
        
        Returns:
            True (luôn thành công)
        """
        if not self.is_locked:
            print(f"🚪 {self.name} - Cửa không khóa")
            return True
        
        self.is_locked = False
        self.state = self.STATE_CLOSED
        self._update_timestamp()
        print(f"🔓 {self.name} đã MỞ KHÓA (cửa vẫn đóng)")
        return True
    
    def toggle(self) -> bool:
        """Chuyển đổi trạng thái cửa (mở <-> đóng).
        
        Returns:
            True nếu thành công, False nếu cửa đang khóa
        """
        if self.state == self.STATE_OPEN:
            return self.close()
        else:
            return self.open()
    
    def get_status(self) -> Dict[str, Any]:
        """Lấy trạng thái chi tiết của cửa.
        
        Returns:
            Dictionary chứa thông tin trạng thái
        """
        status = super().get_status()
        status['state'] = self.state
        status['state_name'] = self.STATE_NAMES[self.state]
        status['is_locked'] = self.is_locked
        status['device_type'] = 'door'
        return status
    
    def __str__(self) -> str:
        """String representation."""
        state_name = self.STATE_NAMES[self.state]
        lock_status = " 🔒" if self.is_locked else ""
        return f"🚪 {self.name} ({self.room}) - {state_name}{lock_status}"

