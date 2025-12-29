"""Device Control Panel - Panel điều khiển thiết bị."""

import tkinter as tk
from tkinter import ttk


class DeviceControlPanel(ttk.Frame):
    """Panel điều khiển cho một thiết bị - Dạng card."""
    
    def __init__(self, parent, device, controller):
        """Khởi tạo panel điều khiển.
        
        Args:
            parent: Widget cha
            device: Đối tượng thiết bị
            controller: DeviceController instance
        """
        super().__init__(parent, padding="12", relief="solid", borderwidth=1)
        self.device = device
        self.controller = controller
        self.device_id = device.device_id
        self.device_type = device.get_status()['device_type']
        
        self._create_widgets()
        self.update_display()
    
    def _create_widgets(self):
        """Tạo các widgets cho panel."""
        # Header
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # Device name and icon - aligned to top
        icon = self._get_device_icon()
        ttk.Label(header_frame, text=icon, font=("Arial", 22)).pack(side="left", anchor="n", padx=(0, 10))
        ttk.Label(header_frame, text=self.device.name, font=("Arial", 10, "bold")).pack(side="left", anchor="n")
        
        # Status label - fixed width for consistent alignment
        self.status_label = ttk.Label(self, text="", font=("Arial", 8), width=15, anchor="w")
        self.status_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        # On/Off buttons (only for light and fan)
        if self.device_type in ["light", "fan"]:
            button_frame = ttk.Frame(self)
            button_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10))
            
            self.on_button = ttk.Button(button_frame, text="🔆 Bật", command=self._on_turn_on, width=10)
            self.on_button.pack(side="left", padx=5)
            
            self.off_button = ttk.Button(button_frame, text="🌙 Tắt", command=self._on_turn_off, width=10)
            self.off_button.pack(side="left", padx=5)
        
        # Device-specific controls
        if self.device_type == "light":
            self._create_light_controls()
        elif self.device_type == "fan":
            self._create_fan_controls()
        elif self.device_type == "door":
            self._create_door_controls()
    
    def _create_light_controls(self):
        """Tạo controls cho đèn (brightness)."""
        ttk.Label(self, text="Độ sáng:").grid(row=3, column=0, sticky="w", pady=5)
        
        self.brightness_var = tk.IntVar(value=self.device.brightness)
        self.brightness_scale = ttk.Scale(
            self, from_=0, to=100, orient="horizontal",
            variable=self.brightness_var,
            command=lambda v: self._on_brightness_change()
        )
        self.brightness_scale.grid(row=3, column=1, sticky="ew", pady=5)
        
        self.brightness_label = ttk.Label(self, text=f"{self.device.brightness}%")
        self.brightness_label.grid(row=4, column=1, sticky="w")
    
    def _create_fan_controls(self):
        """Tạo controls cho quạt (speed)."""
        # Speed buttons frame
        speed_frame = ttk.Frame(self)
        speed_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)
        
        ttk.Label(speed_frame, text="Tốc độ:", font=("Arial", 8)).pack(side="left", padx=(0, 8))
        
        self.speed_var = tk.IntVar(value=self.device.speed)
        
        # Speed buttons
        for speed in [1, 2, 3]:
            btn = ttk.Button(
                speed_frame, 
                text=f"Cấp {speed}",
                width=7,
                command=lambda s=speed: self._set_speed(s)
            )
            btn.pack(side="left", padx=2)
            
            # Store button reference for highlighting
            if not hasattr(self, 'speed_buttons'):
                self.speed_buttons = {}
            self.speed_buttons[speed] = btn
    
    def _create_door_controls(self):
        """Tạo controls cho cửa (open/close/lock/unlock)."""
        # Open/Close buttons
        action_frame = ttk.Frame(self)
        action_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        
        self.open_button = ttk.Button(action_frame, text="🚪 Mở cửa", command=self._on_open_door, width=10)
        self.open_button.pack(side="left", padx=5)
        
        self.close_button = ttk.Button(action_frame, text="🚪 Đóng cửa", command=self._on_close_door, width=10)
        self.close_button.pack(side="left", padx=5)
        
        # Lock/Unlock buttons
        lock_frame = ttk.Frame(self)
        lock_frame.grid(row=3, column=0, columnspan=2, pady=5)
        
        self.lock_button = ttk.Button(lock_frame, text="🔒 Khóa", command=self._on_lock, width=10)
        self.lock_button.pack(side="left", padx=5)
        
        self.unlock_button = ttk.Button(lock_frame, text="🔓 Mở khóa", command=self._on_unlock, width=10)
        self.unlock_button.pack(side="left", padx=5)
    
    def _get_device_icon(self) -> str:
        """Lấy icon emoji cho thiết bị."""
        icons = {
            'light': '💡',
            'fan': '🌀',
            'door': '🚪'
        }
        return icons.get(self.device_type, '🔌')
    
    def _on_turn_on(self):
        """Xử lý sự kiện bật thiết bị."""
        self.controller.control_device(self.device_id, "turn_on")
    
    def _on_turn_off(self):
        """Xử lý sự kiện tắt thiết bị."""
        self.controller.control_device(self.device_id, "turn_off")
    
    def _on_brightness_change(self):
        """Xử lý thay đổi độ sáng."""
        level = int(self.brightness_var.get())
        self.brightness_label.config(text=f"{level}%")
        self.controller.control_device(self.device_id, "set_brightness", {"brightness": level})
    
    def _set_speed(self, speed):
        """Đặt tốc độ quạt."""
        self.speed_var.set(speed)
        self.controller.control_device(self.device_id, "set_speed", {"speed": speed})
    
    def _on_open_door(self):
        """Xử lý mở cửa."""
        self.controller.control_device(self.device_id, "turn_on")
    
    def _on_close_door(self):
        """Xử lý đóng cửa."""
        self.controller.control_device(self.device_id, "turn_off")
    
    def _on_lock(self):
        """Xử lý khóa cửa."""
        self.controller.control_device(self.device_id, "lock")
    
    def _on_unlock(self):
        """Xử lý mở khóa cửa."""
        self.controller.control_device(self.device_id, "unlock")
    
    def update_display(self):
        """Cập nhật hiển thị dựa trên trạng thái thiết bị."""
        status = self.controller.get_device_status(self.device_id)
        if not status:
            return
        
        # Update status label
        is_on = status['is_on']
        
        if self.device_type == "door":
            # For door: show open/closed status instead of on/off
            state = status['state_name']
            is_locked = status['is_locked']
            if is_locked:
                status_text = "🔒 ĐÃ KHÓA"
                status_color = "red"
            elif is_on:
                status_text = "🟢 ĐANG MỞ"
                status_color = "green"
            else:
                status_text = "⚫ ĐANG ĐÓNG"
                status_color = "gray"
            
            self.status_label.config(text=status_text, foreground=status_color)
            
            # Update button states
            self.open_button.state(['disabled'] if is_on else ['!disabled'])
            self.close_button.state(['!disabled'] if is_on else ['disabled'])
            self.lock_button.state(['!disabled'] if not is_locked else ['disabled'])
            self.unlock_button.state(['disabled'] if not is_locked else ['!disabled'])
        else:
            # For light and fan: show on/off status
            status_text = "🟢 ĐANG BẬT" if is_on else "⚫ ĐANG TẮT"
            status_color = "green" if is_on else "gray"
            self.status_label.config(text=status_text, foreground=status_color)
        
        # Update device-specific displays
        if self.device_type == "light":
            self.brightness_var.set(status['brightness'])
            self.brightness_label.config(text=f"{status['brightness']}%")
        elif self.device_type == "fan":
            self.speed_var.set(status['speed'])
            # Update speed button states (highlight current speed)
            if hasattr(self, 'speed_buttons'):
                current_speed = status['speed']
                for speed, btn in self.speed_buttons.items():
                    if speed == current_speed:
                        btn.state(['pressed'])
                    else:
                        btn.state(['!pressed'])
