"""Storage Manager - Quản lý lưu/đọc trạng thái thiết bị vào JSON."""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any


class StorageManager:
    """Quản lý persistence cho Device Controller.
    
    Lưu trữ trạng thái thiết bị vào file JSON khi đóng app,
    và khôi phục khi mở lại.
    """
    
    def __init__(self, file_path: str = "devices_state.json"):
        """Khởi tạo Storage Manager.
        
        Args:
            file_path: Đường dẫn file JSON để lưu trữ
        """
        self.file_path = Path(file_path)
        print(f"💾 StorageManager đã khởi tạo (file: {self.file_path})")
    
    def save_state(self, controller) -> bool:
        """Lưu trạng thái tất cả thiết bị vào JSON.
        
        Args:
            controller: DeviceController instance
            
        Returns:
            True nếu lưu thành công, False nếu có lỗi
        """
        try:
            # Collect device states
            devices_data = []
            for device in controller.devices.values():
                status = device.get_status()
                devices_data.append(status)
            
            # Collect rooms
            rooms = list(set(device.room for device in controller.devices.values()))
            
            # Create data structure
            data = {
                "version": "1.0",
                "last_saved": datetime.now().isoformat(),
                "total_devices": len(devices_data),
                "rooms": sorted(rooms),
                "devices": devices_data
            }
            
            # Write to file
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Đã lưu trạng thái {len(devices_data)} thiết bị vào {self.file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi khi lưu trạng thái: {e}")
            return False
    
    def load_state(self) -> Optional[Dict[str, Any]]:
        """Đọc trạng thái đã lưu từ JSON.
        
        Returns:
            Dictionary chứa dữ liệu thiết bị, hoặc None nếu không có file/lỗi
        """
        try:
            # Check if file exists
            if not self.file_path.exists():
                print(f"ℹ️ Không tìm thấy file trạng thái: {self.file_path}")
                return None
            
            # Read file
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"✅ Đã đọc trạng thái {data.get('total_devices', 0)} thiết bị từ {self.file_path}")
            print(f"   Lưu lần cuối: {data.get('last_saved', 'N/A')}")
            
            return data
            
        except json.JSONDecodeError as e:
            print(f"❌ Lỗi parse JSON: {e}")
            return None
        except Exception as e:
            print(f"❌ Lỗi khi đọc trạng thái: {e}")
            return None
    
    def restore_devices(self, controller, saved_data: Dict[str, Any]) -> int:
        """Khôi phục thiết bị từ dữ liệu đã lưu.
        
        Args:
            controller: DeviceController instance
            saved_data: Dữ liệu từ load_state()
            
        Returns:
            Số lượng thiết bị đã khôi phục thành công
        """
        if not saved_data or 'devices' not in saved_data:
            return 0
        
        # Import device classes
        from simulation.light_simulator import Light
        from simulation.fan_simulator import Fan
        from simulation.door_simulator import Door
        
        restored_count = 0
        
        for device_data in saved_data['devices']:
            try:
                device_type = device_data.get('device_type')
                device_id = device_data.get('device_id')
                name = device_data.get('name')
                room = device_data.get('room')
                is_on = device_data.get('is_on', False)
                
                # Create device based on type
                device = None
                
                if device_type == 'light':
                    brightness = device_data.get('brightness', 100)
                    device = Light(device_id, name, room, brightness)
                
                elif device_type == 'fan':
                    speed = device_data.get('speed', 1)
                    device = Fan(device_id, name, room, speed)
                
                elif device_type == 'door':
                    is_locked = device_data.get('is_locked', False)
                    is_closed = device_data.get('is_closed', True)
                    device = Door(device_id, name, room)
                    device.is_locked = is_locked
                    device.is_closed = is_closed
                
                else:
                    print(f"⚠️ Unknown device type: {device_type}")
                    continue
                
                # Restore on/off state
                if device:
                    if is_on:
                        device.turn_on()
                    else:
                        device.turn_off()
                    
                    # Add to controller
                    if controller.add_device(device):
                        restored_count += 1
                
            except Exception as e:
                print(f"❌ Lỗi khi khôi phục thiết bị {device_data.get('device_id')}: {e}")
                continue
        
        print(f"✅ Đã khôi phục {restored_count}/{len(saved_data['devices'])} thiết bị")
        return restored_count
    
    def delete_state(self) -> bool:
        """Xóa file trạng thái đã lưu.
        
        Returns:
            True nếu xóa thành công, False nếu không tồn tại hoặc có lỗi
        """
        try:
            if self.file_path.exists():
                self.file_path.unlink()
                print(f"🗑️ Đã xóa file trạng thái: {self.file_path}")
                return True
            else:
                print(f"ℹ️ Không có file trạng thái để xóa")
                return False
        except Exception as e:
            print(f"❌ Lỗi khi xóa file trạng thái: {e}")
            return False
    
    def get_file_info(self) -> Optional[Dict[str, Any]]:
        """Lấy thông tin về file trạng thái.
        
        Returns:
            Dictionary chứa thông tin file, hoặc None nếu không tồn tại
        """
        try:
            if not self.file_path.exists():
                return None
            
            stat = self.file_path.stat()
            
            return {
                'exists': True,
                'path': str(self.file_path.absolute()),
                'size_bytes': stat.st_size,
                'size_kb': round(stat.st_size / 1024, 2),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
            }
        except Exception as e:
            print(f"❌ Lỗi khi lấy thông tin file: {e}")
            return None
