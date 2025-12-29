"""Delete Device Dialog - Dialog xóa thiết bị."""

import tkinter as tk
from tkinter import ttk, messagebox


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
