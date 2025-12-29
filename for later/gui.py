"""Main GUI - Giao diện chính của Smart Home Controller."""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from application.device_controller import Observer
from typing import Dict
from simulation.light_simulator import Light
from simulation.fan_simulator import Fan
from simulation.door_simulator import Door
from presentation.room_visualization import RoomCanvas


class AddDeviceDialog(tk.Toplevel):
    """Dialog để thêm thiết bị mới."""
    
    def __init__(self, parent, controller):
        """Khởi tạo dialog.
        
        Args:
            parent: Widget cha
            controller: DeviceController instance
        """
        super().__init__(parent)
        self.controller = controller
        self.result = None
        
        self.title("Thêm thiết bị mới")
        self.geometry("400x300")
        self.resizable(False, False)
        
        # Center dialog
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Tạo các widgets cho dialog."""
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Device type
        ttk.Label(main_frame, text="Loại thiết bị:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=10)
        self.device_type_var = tk.StringVar(value="light")
        device_types = [
            ("💡 Đèn", "light"),
            ("🌀 Quạt", "fan"),
            ("🚪 Cửa", "door")
        ]
        
        for i, (label, value) in enumerate(device_types):
            ttk.Radiobutton(
                main_frame, text=label, variable=self.device_type_var,
                value=value, command=self._on_type_change
            ).grid(row=i+1, column=0, sticky="w", padx=20)
        
        # Device name
        ttk.Label(main_frame, text="Tên thiết bị:", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky="w", pady=(10, 5))
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=30)
        self.name_entry.grid(row=5, column=0, sticky="ew", pady=(0, 10))
        
        # Room selection
        ttk.Label(main_frame, text="Phòng:", font=("Arial", 10, "bold")).grid(row=6, column=0, sticky="w", pady=(10, 5))
        
        room_frame = ttk.Frame(main_frame)
        room_frame.grid(row=7, column=0, sticky="ew")
        
        # Get existing rooms
        existing_rooms = self._get_existing_rooms()
        self.room_var = tk.StringVar()
        
        self.room_combo = ttk.Combobox(room_frame, textvariable=self.room_var, values=existing_rooms, width=20)
        self.room_combo.pack(side="left", padx=(0, 5))
        if existing_rooms:
            self.room_combo.current(0)
        
        ttk.Button(room_frame, text="+ Phòng mới", command=self._add_new_room, width=12).pack(side="left")
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=8, column=0, pady=(20, 0))
        
        ttk.Button(button_frame, text="✅ Thêm", command=self._on_ok, width=12).pack(side="left", padx=5)
        ttk.Button(button_frame, text="❌ Hủy", command=self._on_cancel, width=12).pack(side="left", padx=5)
        
        # Set initial focus
        self.name_entry.focus()
        self._on_type_change()
    
    def _get_existing_rooms(self):
        """Lấy danh sách phòng hiện có."""
        devices = self.controller.get_all_devices()
        rooms = sorted(set(device.room for device in devices))
        return rooms if rooms else ["Phòng khách", "Phòng ngủ", "Bếp"]
    
    def _add_new_room(self):
        """Thêm phòng mới."""
        room_name = simpledialog.askstring("Phòng mới", "Nhập tên phòng:", parent=self)
        if room_name and room_name.strip():
            room_name = room_name.strip()
            existing_rooms = list(self.room_combo['values'])
            if room_name not in existing_rooms:
                existing_rooms.append(room_name)
                self.room_combo['values'] = existing_rooms
            self.room_var.set(room_name)
    
    def _on_type_change(self):
        """Cập nhật tên mẫu khi đổi loại thiết bị."""
        device_type = self.device_type_var.get()
        suggestions = {
            'light': 'Đèn ',
            'fan': 'Quạt ',
            'door': 'Cửa '
        }
        if not self.name_var.get() or any(self.name_var.get().startswith(s) for s in suggestions.values()):
            self.name_var.set(suggestions.get(device_type, '') + self.room_var.get())
    
    def _on_ok(self):
        """Xử lý khi nhấn OK."""
        name = self.name_var.get().strip()
        room = self.room_var.get().strip()
        device_type = self.device_type_var.get()
        
        if not name:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên thiết bị!", parent=self)
            return
        
        if not room:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn hoặc nhập phòng!", parent=self)
            return
        
        # Generate unique ID
        device_id = f"{device_type}_{len(self.controller.get_all_devices()) + 1:03d}"
        
        # Create device
        try:
            if device_type == "light":
                device = Light(device_id, name, room)
            elif device_type == "fan":
                device = Fan(device_id, name, room)
            elif device_type == "door":
                device = Door(device_id, name, room)
            else:
                messagebox.showerror("Lỗi", "Loại thiết bị không hợp lệ!", parent=self)
                return
            
            self.result = device
            self.destroy()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tạo thiết bị: {e}", parent=self)
    
    def _on_cancel(self):
        """Hủy dialog."""
        self.result = None
        self.destroy()


class DeleteDeviceDialog(tk.Toplevel):
    """Dialog để xóa thiết bị."""
    
    def __init__(self, parent, controller):
        """Khởi tạo dialog.
        
        Args:
            parent: Widget cha
            controller: DeviceController instance
        """
        super().__init__(parent)
        self.controller = controller
        self.result = None
        
        self.title("Xóa thiết bị")
        self.geometry("400x300")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Tạo widgets."""
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_frame, text="Chọn thiết bị cần xóa:", font=("Arial", 11, "bold")).pack(pady=(0, 10))
        
        # Listbox with devices
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill="both", expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.device_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=("Arial", 10))
        self.device_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.device_listbox.yview)
        
        # Populate devices
        self.devices = self.controller.get_all_devices()
        for device in self.devices:
            self.device_listbox.insert(tk.END, f"{device.name} ({device.room}) - {device.get_status()['device_type']}")
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=(10, 0))
        
        ttk.Button(button_frame, text="🗑️ Xóa", command=self._on_delete, width=12).pack(side="left", padx=5)
        ttk.Button(button_frame, text="❌ Hủy", command=self._on_cancel, width=12).pack(side="left", padx=5)
    
    def _on_delete(self):
        """Xóa thiết bị đã chọn."""
        selection = self.device_listbox.curselection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn thiết bị cần xóa!", parent=self)
            return
        
        device = self.devices[selection[0]]
        confirm = messagebox.askyesno(
            "Xác nhận",
            f"Bạn có chắc muốn xóa thiết bị:\n{device.name} ({device.room})?",
            parent=self
        )
        
        if confirm:
            self.result = device.device_id
            self.destroy()
    
    def _on_cancel(self):
        """Hủy dialog."""
        self.result = None
        self.destroy()


class RoomManagerDialog(tk.Toplevel):
    """Dialog để quản lý phòng."""
    
    def __init__(self, parent, controller):
        """Khởi tạo dialog.
        
        Args:
            parent: Widget cha
            controller: DeviceController instance
        """
        super().__init__(parent)
        self.controller = controller
        self.rooms_data = {}  # {room_name: device_count}
        
        self.title("Quản lý phòng")
        self.geometry("500x400")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        self._load_rooms_data()
        self._create_widgets()
    
    def _load_rooms_data(self):
        """Load thông tin các phòng và số lượng thiết bị."""
        devices = self.controller.get_all_devices()
        self.rooms_data = {}
        
        for device in devices:
            room = device.room
            self.rooms_data[room] = self.rooms_data.get(room, 0) + 1
    
    def _create_widgets(self):
        """Tạo widgets."""
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Title
        ttk.Label(
            main_frame,
            text="🏠 QUẢN LÝ PHÒNG",
            font=("Arial", 14, "bold")
        ).pack(pady=(0, 15))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(
            button_frame,
            text="➕ Thêm phòng",
            command=self._add_room,
            width=15
        ).pack(side="left", padx=5)
        
        ttk.Button(
            button_frame,
            text="✏️ Đổi tên phòng",
            command=self._rename_room,
            width=15
        ).pack(side="left", padx=5)
        
        ttk.Button(
            button_frame,
            text="🗑️ Xóa phòng",
            command=self._delete_room,
            width=15
        ).pack(side="left", padx=5)
        
        # Listbox frame with scrollbar
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill="both", expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.room_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=("Arial", 10),
            height=12
        )
        self.room_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.room_listbox.yview)
        
        self._refresh_list()
        
        # Info label
        self.info_label = ttk.Label(
            main_frame,
            text="💡 Click chọn phòng rồi nhấn nút để thao tác",
            font=("Arial", 9),
            foreground="gray"
        )
        self.info_label.pack(pady=(5, 10))
        
        # Close button
        ttk.Button(
            main_frame,
            text="✅ Đóng",
            command=self.destroy,
            width=15
        ).pack(pady=10)
    
    def _refresh_list(self):
        """Làm mới danh sách phòng."""
        self.room_listbox.delete(0, tk.END)
        self._load_rooms_data()
        
        if not self.rooms_data:
            self.room_listbox.insert(tk.END, "  (Chưa có phòng nào)")
            return
        
        for room, count in sorted(self.rooms_data.items()):
            device_text = f"{count} thiết bị" if count > 1 else f"{count} thiết bị"
            self.room_listbox.insert(tk.END, f"  📍 {room}  ({device_text})")
    
    def _add_room(self):
        """Thêm phòng mới."""
        room_name = simpledialog.askstring(
            "Thêm phòng mới",
            "Nhập tên phòng:",
            parent=self
        )
        
        if not room_name or not room_name.strip():
            return
        
        room_name = room_name.strip()
        
        # Check if room already exists
        if room_name in self.rooms_data:
            messagebox.showwarning(
                "Cảnh báo",
                f"Phòng '{room_name}' đã tồn tại!",
                parent=self
            )
            return
        
        # Add empty room (no devices yet)
        self.rooms_data[room_name] = 0
        self._refresh_list()
        
        messagebox.showinfo(
            "Thành công",
            f"Đã thêm phòng: {room_name}\n\nBạn có thể thêm thiết bị vào phòng này sau.",
            parent=self
        )
    
    def _rename_room(self):
        """Đổi tên phòng."""
        selection = self.room_listbox.curselection()
        if not selection:
            messagebox.showwarning(
                "Cảnh báo",
                "Vui lòng chọn phòng cần đổi tên!",
                parent=self
            )
            return
        
        # Get selected room name
        selected_text = self.room_listbox.get(selection[0])
        if "(Chưa có phòng nào)" in selected_text:
            return
        
        old_name = selected_text.split("📍")[1].split("(")[0].strip()
        
        # Ask for new name
        new_name = simpledialog.askstring(
            "Đổi tên phòng",
            f"Đổi tên phòng '{old_name}' thành:",
            initialvalue=old_name,
            parent=self
        )
        
        if not new_name or not new_name.strip():
            return
        
        new_name = new_name.strip()
        
        if new_name == old_name:
            return
        
        # Check if new name already exists
        if new_name in self.rooms_data and new_name != old_name:
            messagebox.showwarning(
                "Cảnh báo",
                f"Phòng '{new_name}' đã tồn tại!",
                parent=self
            )
            return
        
        # Rename room in all devices
        devices = self.controller.get_all_devices()
        updated_count = 0
        for device in devices:
            if device.room == old_name:
                device.room = new_name
                updated_count += 1
        
        self._refresh_list()
        
        messagebox.showinfo(
            "Thành công",
            f"Đã đổi tên: '{old_name}' → '{new_name}'\nCập nhật {updated_count} thiết bị.",
            parent=self
        )
    
    def _delete_room(self):
        """Xóa phòng (chỉ nếu không có thiết bị)."""
        selection = self.room_listbox.curselection()
        if not selection:
            messagebox.showwarning(
                "Cảnh báo",
                "Vui lòng chọn phòng cần xóa!",
                parent=self
            )
            return
        
        # Get selected room name
        selected_text = self.room_listbox.get(selection[0])
        if "(Chưa có phòng nào)" in selected_text:
            return
        
        room_name = selected_text.split("📍")[1].split("(")[0].strip()
        device_count = self.rooms_data.get(room_name, 0)
        
        # Check if room has devices
        if device_count > 0:
            messagebox.showwarning(
                "Không thể xóa",
                f"Phòng '{room_name}' có {device_count} thiết bị!\n\n"
                "Vui lòng xóa hoặc di chuyển các thiết bị trước khi xóa phòng.",
                parent=self
            )
            return
        
        # Confirm deletion
        confirm = messagebox.askyesno(
            "Xác nhận",
            f"Bạn có chắc muốn xóa phòng:\n'{room_name}'?",
            parent=self
        )
        
        if not confirm:
            return
        
        # Remove from data (it's an empty room)
        if room_name in self.rooms_data:
            del self.rooms_data[room_name]
        
        self._refresh_list()
        
        messagebox.showinfo(
            "Thành công",
            f"Đã xóa phòng: {room_name}",
            parent=self
        )


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
        self.controller.control_device(self.device_id, "set_brightness", {"level": level})
    
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


class TimerPanel(ttk.LabelFrame):
    """Panel quản lý hẹn giờ."""
    
    def __init__(self, parent, controller, timer_manager):
        """Khởi tạo timer panel.
        
        Args:
            parent: Widget cha
            controller: DeviceController instance
            timer_manager: TimerManager instance
        """
        super().__init__(parent, text="⏰ Hẹn giờ", padding="10")
        self.controller = controller
        self.timer_manager = timer_manager
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Tạo widgets cho timer panel."""
        # Device selection
        ttk.Label(self, text="Thiết bị:").grid(row=0, column=0, sticky="w", pady=5)
        self.device_combo = ttk.Combobox(self, state="readonly", width=20)
        self.device_combo.grid(row=0, column=1, pady=5, padx=5)
        
        # Action selection
        ttk.Label(self, text="Hành động:").grid(row=1, column=0, sticky="w", pady=5)
        self.action_combo = ttk.Combobox(self, values=["turn_on", "turn_off"], state="readonly", width=20)
        self.action_combo.current(0)
        self.action_combo.grid(row=1, column=1, pady=5, padx=5)
        
        # Time input
        ttk.Label(self, text="Sau:").grid(row=2, column=0, sticky="w", pady=5)
        time_frame = ttk.Frame(self)
        time_frame.grid(row=2, column=1, pady=5, padx=5)
        
        self.time_var = tk.IntVar(value=5)
        time_spinbox = ttk.Spinbox(time_frame, from_=1, to=3600, textvariable=self.time_var, width=10)
        time_spinbox.pack(side="left", padx=(0, 5))
        
        self.unit_combo = ttk.Combobox(time_frame, values=["giây", "phút"], state="readonly", width=10)
        self.unit_combo.current(1)  # Default to minutes
        self.unit_combo.pack(side="left")
        
        # Schedule button
        ttk.Button(self, text="⏰ Đặt hẹn giờ", command=self._on_schedule).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Active timers list
        ttk.Label(self, text="Timers đang chạy:").grid(row=4, column=0, columnspan=2, sticky="w", pady=(10, 5))
        
        self.timer_listbox = tk.Listbox(self, height=5, width=40)
        self.timer_listbox.grid(row=5, column=0, columnspan=2, pady=5)
        
        # Cancel button
        ttk.Button(self, text="❌ Hủy timer", command=self._on_cancel).grid(row=6, column=0, columnspan=2, pady=5)
        
        # Refresh button
        ttk.Button(self, text="🔄 Làm mới", command=self.refresh_timer_list).grid(row=7, column=0, columnspan=2, pady=5)
        
        # Initial refresh
        self.refresh_device_list()
        self.refresh_timer_list()
    
    def _on_schedule(self):
        """Xử lý đặt hẹn giờ."""
        # Get selected device
        device_name = self.device_combo.get()
        if not device_name:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn thiết bị")
            return
        
        # Find device by name
        devices = self.controller.get_all_devices()
        device = next((d for d in devices if d.name == device_name), None)
        if not device:
            messagebox.showerror("Lỗi", "Không tìm thấy thiết bị")
            return
        
        # Get action
        action = self.action_combo.get()
        
        # Calculate delay in seconds
        time_value = self.time_var.get()
        unit = self.unit_combo.get()
        delay_seconds = time_value * (60 if unit == "phút" else 1)
        
        # Schedule timer
        timer_id = self.timer_manager.schedule_timer(device.device_id, action, delay_seconds)
        
        if timer_id:
            messagebox.showinfo("Thành công", f"Đã đặt hẹn giờ: {device_name} - {action}")
            self.refresh_timer_list()
        else:
            messagebox.showerror("Lỗi", "Không thể đặt hẹn giờ")
    
    def _on_cancel(self):
        """Hủy timer đã chọn."""
        selection = self.timer_listbox.curselection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn timer cần hủy")
            return
        
        timer_text = self.timer_listbox.get(selection[0])
        timer_id = timer_text.split("]")[0][1:]  # Extract timer_id from [timer_1]
        
        if self.timer_manager.cancel_timer(timer_id):
            messagebox.showinfo("Thành công", "Đã hủy timer")
            self.refresh_timer_list()
    
    def refresh_device_list(self):
        """Làm mới danh sách thiết bị."""
        devices = self.controller.get_all_devices()
        device_names = [d.name for d in devices]
        self.device_combo['values'] = device_names
        if device_names:
            self.device_combo.current(0)
    
    def refresh_timer_list(self):
        """Làm mới danh sách timer."""
        self.timer_listbox.delete(0, tk.END)
        
        timers = self.timer_manager.get_active_timers()
        for task in sorted(timers, key=lambda t: t.scheduled_time):
            self.timer_listbox.insert(tk.END, str(task))


class MainWindow(tk.Tk, Observer):
    """Cửa sổ chính của ứng dụng."""
    
    def __init__(self, controller, timer_manager):
        """Khởi tạo cửa sổ chính.
        
        Args:
            controller: DeviceController instance
            timer_manager: TimerManager instance
        """
        super().__init__()
        
        self.controller = controller
        self.timer_manager = timer_manager
        self.device_panels: Dict[str, DeviceControlPanel] = {}
        self.current_room = "Tất cả"
        
        # Register as observer
        self.controller.register_observer(self)
        
        self._setup_window()
        self._create_menu()
        self._create_widgets()
    
    def _create_menu(self):
        """Tạo menu bar."""
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # Device menu
        device_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="⚙️ Thiết bị", menu=device_menu)
        device_menu.add_command(label="➕ Thêm thiết bị", command=self._on_add_device)
        device_menu.add_command(label="🗑️ Xóa thiết bị", command=self._on_remove_device)
        device_menu.add_separator()
        device_menu.add_command(label="🔄 Làm mới", command=self._refresh_all)
        
        # Room menu
        room_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🏠 Phòng", menu=room_menu)
        room_menu.add_command(label="🏠 Tất cả phòng", command=lambda: self._filter_by_room("Tất cả"))
        room_menu.add_separator()
        room_menu.add_command(label="⚙️ Quản lý phòng", command=self._open_room_manager)
        room_menu.add_separator()
        
        # Add existing rooms
        self.room_menu = room_menu
        self._update_room_menu()
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="❓ Trợ giúp", menu=help_menu)
        help_menu.add_command(label="📖 Hướng dẫn", command=self._show_help)
        help_menu.add_command(label="ℹ️ Về chương trình", command=self._show_about)
    
    def _update_room_menu(self):
        """Cập nhật menu phòng với danh sách phòng hiện tại."""
        # Clear existing room items (keep "Tất cả", separator, "Quản lý phòng", and another separator)
        self.room_menu.delete(4, tk.END)
        
        # Add rooms
        devices = self.controller.get_all_devices()
        rooms = sorted(set(device.room for device in devices))
        
        for room in rooms:
            self.room_menu.add_command(
                label=f"📍 {room}",
                command=lambda r=room: self._filter_by_room(r)
            )
    
    def _filter_by_room(self, room: str):
        """Lọc thiết bị theo phòng.
        
        Args:
            room: Tên phòng hoặc "Tất cả"
        """
        self.current_room = room
        self._refresh_device_panels()
        
        # Update room canvas
        if hasattr(self, 'room_canvas'):
            self.room_canvas.set_room(room)
        
        if room == "Tất cả":
            self.title("🏠 Smart Home Controller - Tất cả phòng")
        else:
            self.title(f"🏠 Smart Home Controller - {room}")
    
    def _calculate_initial_columns(self):
        """Tính số cột ban đầu sau khi canvas đã render."""
        if hasattr(self, 'devices_canvas'):
            canvas_width = self.devices_canvas.winfo_width()
            if canvas_width > 1:  # Canvas đã có kích thước thực
                self.device_grid_cols = max(1, (canvas_width - 10) // self.device_card_min_width)
                self._refresh_device_panels()
    

            # Use after to debounce resize events
            if hasattr(self, '_resize_timer'):
                self.after_cancel(self._resize_timer)
            self._resize_timer = self.after(100, self._refresh_device_panels)
    
    def _layout_device_panels(self, devices):
        """Layout device panels in grid.
        
        Args:
            devices: List of devices to layout
        """
        # Clear old column configurations
        for col in range(10):  # Clear up to 10 columns
            self.devices_frame.grid_columnconfigure(col, weight=0, minsize=0)
        
        # Layout panels
        for idx, device in enumerate(devices):
            row = idx // self.device_grid_cols
            col = idx % self.device_grid_cols
            
            panel = DeviceControlPanel(self.devices_frame, device, self.controller)
            panel.grid(row=row, column=col, padx=6, pady=6)
            self.device_panels[device.device_id] = panel
        
        # Configure grid columns with fixed width (no expansion)
        for col in range(self.device_grid_cols):
            self.devices_frame.grid_columnconfigure(col, weight=0, minsize=self.device_card_min_width)
    
    def _on_add_device(self):
        """Xử lý thêm thiết bị mới."""
        dialog = AddDeviceDialog(self, self.controller)
        self.wait_window(dialog)
        
        if dialog.result:
            device = dialog.result
            self.controller.add_device(device)
            messagebox.showinfo("Thành công", f"Đã thêm thiết bị: {device.name}")
            self._refresh_all()
    
    def _on_remove_device(self):
        """Xử lý xóa thiết bị."""
        dialog = DeleteDeviceDialog(self, self.controller)
        self.wait_window(dialog)
        
        if dialog.result:
            device_id = dialog.result
            self.controller.remove_device(device_id)
            messagebox.showinfo("Thành công", f"Đã xóa thiết bị: {device_id}")
            self._refresh_all()
    
    def _open_room_manager(self):
        """Mở dialog quản lý phòng."""
        dialog = RoomManagerDialog(self, self.controller)
        self.wait_window(dialog)
        
        # Refresh everything after managing rooms
        self._refresh_all()
    
    def _refresh_all(self):
        """Làm mới toàn bộ giao diện."""
        self._refresh_device_panels()
        self._update_room_menu()
        
        # Refresh room canvas
        if hasattr(self, 'room_canvas'):
            self.room_canvas.refresh()
        
        if hasattr(self, 'timer_panel'):
            self.timer_panel.refresh_device_list()
    
    def _refresh_device_panels(self):
        """Làm mới panels của các thiết bị."""
        # Clear existing panels
        for panel in self.device_panels.values():
            panel.destroy()
        self.device_panels.clear()
        
        # Get devices (with room filter if needed)
        devices = self.controller.get_all_devices()
        
        # Filter by room if needed
        if self.current_room != "Tất cả":
            devices = [d for d in devices if d.room == self.current_room]
        
        # Re-layout with current column count
        self._layout_device_panels(devices)
        
        # Update status
        self._update_status()
    
    def _update_status(self):
        """Cập nhật status bar."""
        summary = self.controller.get_summary()
        self.status_label.config(
            text=f"Tổng số thiết bị: {summary['total_devices']} | Đang bật: {summary['devices_on']}"
        )
    
    def _show_help(self):
        """Hiển thị hướng dẫn."""
        help_text = """
        🏠 SMART HOME CONTROLLER - HƯỚNG DẪN SỬ DỤNG
        
        ĐIỀU KHIỂN THIẾT BỊ:
        • Sử dụng các nút Bật/Tắt để điều khiển thiết bị
        • Đèn: Điều chỉnh độ sáng bằng thanh trượt
        • Quạt: Chọn tốc độ từ 1-3
        • Cửa: Mở/Đóng và Khóa/Mở khóa
        
        HẸN GIỜ:
        • Chọn thiết bị và hành động
        • Nhập thời gian và đơn vị (giây/phút)
        • Nhấn "Đặt hẹn giờ"
        
        QUẢN LÝ THIẾT BỊ:
        • Menu "Thiết bị" > "Thêm thiết bị": Thêm thiết bị mới
        • Menu "Thiết bị" > "Xóa thiết bị": Xóa thiết bị hiện có
        
        QUẢN LÝ PHÒNG:
        • Menu "Phòng": Lọc thiết bị theo phòng
        • Khi thêm thiết bị, có thể tạo phòng mới
        """
        messagebox.showinfo("Hướng dẫn sử dụng", help_text, parent=self)
    
    def _show_about(self):
        """Hiển thị thông tin về chương trình."""
        about_text = """
        🏠 SMART HOME CONTROLLER
        Version 1.0
        
        Hệ thống mô phỏng điều khiển thiết bị IoT trong gia đình
        
        Tính năng:
        ✅ Điều khiển đèn, quạt, cửa
        ✅ Hẹn giờ tự động
        ✅ Quản lý nhiều phòng
        ✅ Thêm/xóa thiết bị động
        
        © 2024 - Smart Home Project
        """
        messagebox.showinfo("Về chương trình", about_text, parent=self)
    
    def _setup_window(self):
        """Thiết lập cửa sổ."""
        self.title("🏠 Smart Home Controller")
        self.geometry("1200x800")
        self.configure(bg="#f0f0f0")
        
        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.winfo_screenheight() // 2) - (800 // 2)
        self.geometry(f"1200x800+{x}+{y}")
    
    def _create_widgets(self):
        """Tạo các widgets."""
        # Title
        title_frame = ttk.Frame(self, padding="10")
        title_frame.pack(fill="x")
        ttk.Label(title_frame, text="🏠 SMART HOME CONTROLLER", font=("Arial", 18, "bold")).pack()
        ttk.Label(title_frame, text="Hệ thống điều khiển thiết bị IoT trong gia đình", font=("Arial", 10)).pack()
        
        # Main container with scrollbar
        main_container = ttk.Frame(self)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Top part - Room visualization
        room_frame = ttk.LabelFrame(main_container, text="📍 Sơ đồ phòng", padding="10")
        room_frame.pack(fill="x", pady=(0, 10))
        room_frame.configure(height=300)
        
        self.room_canvas = RoomCanvas(room_frame, self.controller, self.current_room)
        self.room_canvas.pack(fill="both", expand=True)
        
        # Bottom part - Controls
        controls_container = ttk.Frame(main_container)
        controls_container.pack(fill="both", expand=True)
        
        # Left side - Device controls (pack FIRST to avoid z-order overlap)
        left_frame = ttk.Frame(controls_container)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Set minimum size to prevent being squeezed too small
        self.update_idletasks()
        left_frame.update_idletasks()
        
        ttk.Label(left_frame, text="Danh sách thiết bị:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 10))
        
        # Scrollable frame for devices (grid layout)
        canvas_container = ttk.Frame(left_frame)
        canvas_container.pack(fill="both", expand=True)
        
        devices_canvas = tk.Canvas(canvas_container, bg="#f8f9fa", highlightthickness=0)
        devices_scrollbar = ttk.Scrollbar(canvas_container, orient="vertical", command=devices_canvas.yview)
        devices_frame = ttk.Frame(devices_canvas)
        
        # Bind configure to update scrollregion (vertical only)
        def _on_devices_frame_configure(event):
            # Only allow vertical scrolling, clip horizontal
            canvas_width = devices_canvas.winfo_width()
            frame_height = devices_frame.winfo_height()
            devices_canvas.configure(scrollregion=(0, 0, canvas_width, frame_height))
        
        devices_frame.bind("<Configure>", _on_devices_frame_configure)
        
        # Create window for frame inside canvas
        devices_canvas_window = devices_canvas.create_window((5, 5), window=devices_frame, anchor="nw")
        devices_canvas.configure(yscrollcommand=devices_scrollbar.set)
        
        # Bind canvas resize to update frame width
        def _on_canvas_width_change(event):
            # Make frame width match canvas width to prevent overflow
            devices_canvas.itemconfig(devices_canvas_window, width=event.width - 10)  # -10 for padding
        
        devices_canvas.bind("<Configure>", _on_canvas_width_change)
        
        devices_canvas.pack(side="left", fill="both", expand=True)
        devices_scrollbar.pack(side="right", fill="y")
        
        # Store reference for refresh
        self.devices_frame = devices_frame
        self.devices_canvas = devices_canvas
        self.devices_canvas_window = devices_canvas_window  # Store window ID
        
        # Config for grid layout (dynamic columns)
        self.device_card_min_width = 232  # Card width (200) + padx (6*2) + margins (20)
        self.device_grid_cols = 1  # Will be calculated dynamically
        
        # Bind resize event to recalculate columns
        self.after(100, self._calculate_initial_columns)
        
        # Note: Canvas resize already bound above for width management
        # This binding is for recalculating grid columns only
        original_canvas_configure = _on_canvas_width_change
        def _on_canvas_resize_with_grid(event):
            original_canvas_configure(event)
            # Recalculate columns based on new width
            canvas_width = event.width - 10  # Account for scrollbar
            new_cols = max(1, canvas_width // self.device_card_min_width)
            if new_cols != self.device_grid_cols:
                self.device_grid_cols = new_cols
                if hasattr(self, '_resize_timer'):
                    self.after_cancel(self._resize_timer)
                self._resize_timer = self.after(100, self._refresh_device_panels)
        
        devices_canvas.bind("<Configure>", _on_canvas_resize_with_grid)
        
        # Create device panels in grid
        devices = self.controller.get_all_devices()
        self._layout_device_panels(devices)
        
        # Right side - Timer panel (pack AFTER to be on top in z-order)
        right_frame = ttk.Frame(controls_container, width=350)
        right_frame.pack(side="right", fill="y", padx=(10, 0))
        right_frame.pack_propagate(False)  # Prevent shrinking
        
        timer_panel = TimerPanel(right_frame, self.controller, self.timer_manager)
        timer_panel.pack(fill="both", expand=True)
        self.timer_panel = timer_panel
        
        # Status bar
        status_frame = ttk.Frame(self)
        status_frame.pack(fill="x", side="bottom")
        
        summary = self.controller.get_summary()
        self.status_label = ttk.Label(status_frame, text=f"Tổng số thiết bị: {summary['total_devices']} | Đang bật: {summary['devices_on']}", relief="sunken")
        self.status_label.pack(fill="x", padx=5, pady=5)
        
        # Initial status update
        self._update_status()
    
    def update(self, device_id: str):
        """Observer callback - cập nhật UI khi device thay đổi.
        
        Args:
            device_id: ID của thiết bị đã thay đổi
        """
        # Update device panel
        if device_id in self.device_panels:
            self.device_panels[device_id].update_display()
        
        # Update room canvas
        if hasattr(self, 'room_canvas'):
            self.room_canvas.update_device_icon(device_id)
        
        # Update status bar
        self._update_status()
    
    def run(self):
        """Chạy ứng dụng."""
        self.mainloop()
