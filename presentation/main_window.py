"""Main Window - Cửa sổ chính của ứng dụng."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict
from application.device_controller import Observer
from presentation.dialogs import AddDeviceDialog, DeleteDeviceDialog, RoomManagerDialog
from presentation.panels import DeviceControlPanel, TimerPanel
from presentation.room_visualization import RoomCanvas


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
