"""Base Device - Abstract base class for all IoT devices."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any


class BaseDevice(ABC):
    """Abstract base class cho tất cả thiết bị IoT.
    
    Sử dụng Template Method Pattern để định nghĩa interface chung,
    các subclass sẽ override các abstract methods.
    """
    
    def __init__(self, device_id: str, name: str, room: str):
        """Khởi tạo thiết bị cơ bản.
        
        Args:
            device_id: ID duy nhất của thiết bị
            name: Tên thiết bị (VD: "Đèn phòng khách")
            room: Phòng chứa thiết bị (VD: "Phòng khách")
        """
        self.device_id = device_id
        self.name = name
        self.room = room
        self.is_on = False
        self.last_update = datetime.now()
    
    @abstractmethod
    def turn_on(self) -> bool:
        """Bật thiết bị.
        
        Returns:
            True nếu thành công, False nếu thất bại
        """
        pass
    
    @abstractmethod
    def turn_off(self) -> bool:
        """Tắt thiết bị.
        
        Returns:
            True nếu thành công, False nếu thất bại
        """
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """Lấy trạng thái hiện tại của thiết bị.
        
        Returns:
            Dictionary chứa thông tin trạng thái
        """
        return {
            'device_id': self.device_id,
            'name': self.name,
            'room': self.room,
            'is_on': self.is_on,
            'last_update': self.last_update.isoformat()
        }
    
    def _update_timestamp(self):
        """Cập nhật timestamp khi có thay đổi."""
        self.last_update = datetime.now()
    
    def __str__(self) -> str:
        """String representation của thiết bị."""
        status = "BẬT" if self.is_on else "TẮT"
        return f"{self.name} ({self.room}) - {status}"
    
    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"{self.__class__.__name__}(id={self.device_id}, name={self.name}, is_on={self.is_on})"

