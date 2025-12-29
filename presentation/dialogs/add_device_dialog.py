"""Add Device Dialog - Dialog thêm thiết bị mới."""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from simulation.light_simulator import Light
from simulation.fan_simulator import Fan
from simulation.door_simulator import Door


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
