"""Timer Panel - Panel quản lý hẹn giờ."""

import tkinter as tk
from tkinter import ttk, messagebox


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
