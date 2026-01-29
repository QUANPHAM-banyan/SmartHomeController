"""Timer Manager - Quản lý hẹn giờ cho thiết bị."""

import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class TimerTask:
    """Representation của một timer task."""
    timer_id: str
    device_id: str
    device_name: str
    action: str
    scheduled_time: datetime
    delay_seconds: int
    thread: threading.Timer
    
    def cancel(self):
        """Hủy timer."""
        if self.thread and self.thread.is_alive():
            self.thread.cancel()
    
    def is_active(self) -> bool:
        """Kiểm tra timer còn active không."""
        return self.thread and self.thread.is_alive()
    
    def time_remaining(self) -> int:
        """Tính thời gian còn lại (giây).
        
        Returns:
            Số giây còn lại, 0 nếu đã hết
        """
        if not self.is_active():
            return 0
        
        now = datetime.now()
        remaining = (self.scheduled_time - now).total_seconds()
        return max(0, int(remaining))
    
    def __str__(self) -> str:
        """String representation."""
        remaining = self.time_remaining()
        minutes, seconds = divmod(remaining, 60)
        return f"[{self.timer_id}] {self.device_name} - {self.action} (còn {minutes}p {seconds}s)"


class TimerManager:
    """Quản lý hẹn giờ cho các thiết bị.
    
    Sử dụng threading.Timer để chạy background tasks.
    """
    
    def __init__(self, controller):
        """Khởi tạo TimerManager.
        
        Args:
            controller: DeviceController instance
        """
        self.controller = controller
        self.active_timers: Dict[str, TimerTask] = {}
        self.timer_id_counter = 0
        self._lock = threading.Lock()  # Thread safety
        print("⏰ TimerManager đã khởi tạo")
    
    def schedule_timer(self, device_id: str, action: str, delay_seconds: int) -> Optional[str]:
        """Đặt hẹn giờ cho thiết bị.
        
        Args:
            device_id: ID của thiết bị
            action: Hành động (turn_on, turn_off, v.v.)
            delay_seconds: Số giây trước khi thực thi
            
        Returns:
            Timer ID nếu thành công, None nếu thất bại
        """
        # Validate device exists
        device = self.controller.get_device(device_id)
        if not device:
            print(f"❌ Không tìm thấy thiết bị ID: {device_id}")
            return None
        
        # Validate delay
        if delay_seconds <= 0:
            print(f"❌ Thời gian trễ phải lớn hơn 0")
            return None
        
        with self._lock:
            # Generate timer ID
            self.timer_id_counter += 1
            timer_id = f"timer_{self.timer_id_counter}"
            
            # Calculate scheduled time
            scheduled_time = datetime.now() + timedelta(seconds=delay_seconds)
            
            # Create callback function
            def execute_timer():
                self._execute_timer(timer_id, device_id, action)
            
            # Create threading.Timer
            timer_thread = threading.Timer(delay_seconds, execute_timer)
            
            # Create TimerTask
            task = TimerTask(
                timer_id=timer_id,
                device_id=device_id,
                device_name=device.name,
                action=action,
                scheduled_time=scheduled_time,
                delay_seconds=delay_seconds,
                thread=timer_thread
            )
            
            # Store and start
            self.active_timers[timer_id] = task
            timer_thread.start()
            
            # Format time display
            minutes, seconds = divmod(delay_seconds, 60)
            time_str = f"{minutes} phút {seconds} giây" if minutes > 0 else f"{seconds} giây"
            
            print(f"⏰ Đã đặt hẹn giờ: {device.name} - {action} sau {time_str}")
            print(f"   Timer ID: {timer_id}")
            print(f"   Thời gian thực thi: {scheduled_time.strftime('%H:%M:%S')}")
            
            return timer_id
    
    def _execute_timer(self, timer_id: str, device_id: str, action: str):
        """Thực thi timer (gọi từ background thread).
        
        Args:
            timer_id: ID của timer
            device_id: ID của thiết bị
            action: Hành động cần thực thi
        """
        print(f"\n⏰ TIMER KÍCH HOẠT: {timer_id}")
        
        # Kiểm tra nếu là hành động khóa cửa, sử dụng lock_with_close
        device = self.controller.get_device(device_id)
        if device and device.__class__.__name__ == "Door" and action == "lock":
            # Sử dụng lock_with_close để đảm bảo cửa đóng và khóa
            success = device.lock_with_close()
        else:
            # Execute command bình thường
            success = self.controller.control_device(device_id, action)
        
        if success:
            print(f"✅ Timer thực thi thành công: {action} trên {device_id}")
        else:
            print(f"❌ Timer thực thi thất bại: {action} trên {device_id}")
        
        # Remove from active timers
        with self._lock:
            if timer_id in self.active_timers:
                del self.active_timers[timer_id]
                print(f"🗑️ Đã xóa timer: {timer_id}\n")
    
    def cancel_timer(self, timer_id: str) -> bool:
        """Hủy một timer đang chạy.
        
        Args:
            timer_id: ID của timer cần hủy
            
        Returns:
            True nếu thành công, False nếu không tìm thấy
        """
        with self._lock:
            if timer_id not in self.active_timers:
                print(f"❌ Không tìm thấy timer ID: {timer_id}")
                return False
            
            task = self.active_timers[timer_id]
            task.cancel()
            del self.active_timers[timer_id]
            
            print(f"❌ Đã hủy timer: {task.device_name} - {task.action}")
            return True
    
    def cancel_all_timers(self) -> int:
        """Hủy tất cả timers đang chạy.
        
        Returns:
            Số lượng timers đã hủy
        """
        with self._lock:
            count = len(self.active_timers)
            
            for task in self.active_timers.values():
                task.cancel()
            
            self.active_timers.clear()
            
            if count > 0:
                print(f"❌ Đã hủy {count} timer(s)")
            
            return count
    
    def get_active_timers(self) -> List[TimerTask]:
        """Lấy danh sách các timers đang active.
        
        Returns:
            List các TimerTask
        """
        with self._lock:
            # Filter out completed timers
            active = [task for task in self.active_timers.values() if task.is_active()]
            return active
    
    def get_timer(self, timer_id: str) -> Optional[TimerTask]:
        """Lấy thông tin của một timer.
        
        Args:
            timer_id: ID của timer
            
        Returns:
            TimerTask hoặc None nếu không tìm thấy
        """
        return self.active_timers.get(timer_id)
    
    def get_timers_for_device(self, device_id: str) -> List[TimerTask]:
        """Lấy tất cả timers của một thiết bị.
        
        Args:
            device_id: ID của thiết bị
            
        Returns:
            List các TimerTask
        """
        return [
            task for task in self.get_active_timers()
            if task.device_id == device_id
        ]
    
    def print_active_timers(self):
        """In ra danh sách timers đang active."""
        timers = self.get_active_timers()
        
        if not timers:
            print("\n⏰ Không có timer nào đang chạy")
            return
        
        print("\n" + "="*50)
        print("        TIMERS ĐANG HOẠT ĐỘNG")
        print("="*50)
        
        for task in sorted(timers, key=lambda t: t.scheduled_time):
            remaining = task.time_remaining()
            minutes, seconds = divmod(remaining, 60)
            
            print(f"\n[{task.timer_id}]")
            print(f"  Thiết bị: {task.device_name}")
            print(f"  Hành động: {task.action}")
            print(f"  Thời gian thực thi: {task.scheduled_time.strftime('%H:%M:%S')}")
            print(f"  Còn lại: {minutes} phút {seconds} giây")
        
        print("\n" + "="*50 + "\n")
    
    def cleanup_completed_timers(self):
        """Xóa các timers đã hoàn thành."""
        with self._lock:
            completed = [tid for tid, task in self.active_timers.items() if not task.is_active()]
            for tid in completed:
                del self.active_timers[tid]
            
            if completed:
                print(f"🧹 Đã dọn dẹp {len(completed)} timer(s) đã hoàn thành")

