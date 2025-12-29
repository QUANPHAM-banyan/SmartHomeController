"""Room Manager Dialog - Dialog quản lý phòng."""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


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
