"""Room Visualization - Hiển thị sơ đồ phòng với thiết bị."""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


class DevicePopup(tk.Toplevel):
    """Popup để tương tác nhanh với thiết bị."""
    
    def __init__(self, parent, device, controller):
        """Khởi tạo popup.
        
        Args:
            parent: Widget cha
            device: Đối tượng thiết bị
            controller: DeviceController instance
        """
        super().__init__(parent)
        self.device = device
        self.controller = controller
        
        self.title(f"⚙️ {device.name}")
        self.geometry("300x250")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Tạo widgets."""
        main_frame = ttk.Frame(self, padding="15")
        main_frame.pack(fill="both", expand=True)
        
        # Device info
        status = self.device.get_status()
        device_type_icons = {'light': '💡', 'fan': '🌀', 'door': '🚪'}
        icon = device_type_icons.get(status['device_type'], '🔌')
        
        ttk.Label(
            main_frame,
            text=f"{icon} {self.device.name}",
            font=("Arial", 14, "bold")
        ).pack(pady=(0, 5))
        
        ttk.Label(
            main_frame,
            text=f"Phòng: {self.device.room}",
            font=("Arial", 10)
        ).pack(pady=(0, 15))
        
        # Status indicator
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(pady=10)
        
        device_type = status['device_type']
        
        # Different status for door
        if device_type == 'door':
            if hasattr(self.device, 'state') and self.device.state == "locked":
                status_text = "🔒 Đã khóa"
                status_color = "red"
            elif self.device.is_on:
                status_text = "🟢 Đang mở"
                status_color = "green"
            else:
                status_text = "⚫ Đang đóng"
                status_color = "gray"
        else:
            status_text = "🟢 Đang bật" if self.device.is_on else "🔴 Đang tắt"
            status_color = "green" if self.device.is_on else "red"
        
        self.status_label = ttk.Label(
            status_frame,
            text=status_text,
            font=("Arial", 11, "bold"),
            foreground=status_color
        )
        self.status_label.pack()
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=15)
        
        # Different buttons for door
        if device_type == 'door':
            if self.device.is_on:
                ttk.Button(
                    button_frame,
                    text="🚪 Đóng cửa",
                    command=self._turn_off,
                    width=12
                ).pack(side="left", padx=5)
            else:
                ttk.Button(
                    button_frame,
                    text="🚪 Mở cửa",
                    command=self._turn_on,
                    width=12
                ).pack(side="left", padx=5)
        else:
            if self.device.is_on:
                ttk.Button(
                    button_frame,
                    text="🌙 Tắt",
                    command=self._turn_off,
                    width=12
                ).pack(side="left", padx=5)
            else:
                ttk.Button(
                    button_frame,
                    text="🔆 Bật",
                    command=self._turn_on,
                    width=12
                ).pack(side="left", padx=5)
        
        ttk.Button(
            button_frame,
            text="❌ Đóng",
            command=self.destroy,
            width=12
        ).pack(side="left", padx=5)
        
        # Device-specific quick controls
        self._add_device_controls(main_frame)
    
    def _add_device_controls(self, parent):
        """Thêm controls đặc biệt cho từng loại thiết bị."""
        device_type = self.device.get_status()['device_type']
        
        if device_type == 'light':
            ttk.Label(parent, text="Độ sáng:", font=("Arial", 9)).pack(pady=(5, 0))
            brightness_var = tk.IntVar(value=self.device.brightness)
            scale = ttk.Scale(
                parent, from_=0, to=100, orient="horizontal",
                variable=brightness_var,
                command=lambda v: self._set_brightness(int(float(v)))
            )
            scale.pack(fill="x", padx=20, pady=5)
            
        elif device_type == 'fan':
            ttk.Label(parent, text="Tốc độ:", font=("Arial", 9)).pack(pady=(5, 0))
            speed_frame = ttk.Frame(parent)
            speed_frame.pack(pady=5)
            
            for speed in [1, 2, 3]:
                ttk.Button(
                    speed_frame,
                    text=f"⚡{speed}",
                    command=lambda s=speed: self._set_speed(s),
                    width=6
                ).pack(side="left", padx=2)
        
        elif device_type == 'door':
            door_frame = ttk.Frame(parent)
            door_frame.pack(pady=5)
            
            if self.device.state == "locked":
                ttk.Button(
                    door_frame,
                    text="🔓 Mở khóa",
                    command=self._unlock,
                    width=12
                ).pack(side="left", padx=2)
            else:
                ttk.Button(
                    door_frame,
                    text="🔒 Khóa",
                    command=self._lock,
                    width=12
                ).pack(side="left", padx=2)
    
    def _turn_on(self):
        """Bật thiết bị."""
        self.controller.control_device(self.device.device_id, "turn_on")
        self.destroy()
    
    def _turn_off(self):
        """Tắt thiết bị."""
        self.controller.control_device(self.device.device_id, "turn_off")
        self.destroy()
    
    def _set_brightness(self, value):
        """Đặt độ sáng đèn."""
        self.controller.control_device(self.device.device_id, "set_brightness", {"brightness": value})
    
    def _set_speed(self, speed):
        """Đặt tốc độ quạt."""
        self.controller.control_device(self.device.device_id, "set_speed", {"speed": speed})
        self.destroy()
    
    def _lock(self):
        """Khóa cửa."""
        self.controller.control_device(self.device.device_id, "lock")
        self.destroy()
    
    def _unlock(self):
        """Mở khóa cửa."""
        self.controller.control_device(self.device.device_id, "unlock")
        self.destroy()


class RoomCanvas(ttk.Frame):
    """Canvas hiển thị sơ đồ phòng với các thiết bị."""
    
    def __init__(self, parent, controller, current_room="Tất cả"):
        """Khởi tạo room canvas.
        
        Args:
            parent: Widget cha
            controller: DeviceController instance
            current_room: Phòng hiện tại đang hiển thị
        """
        super().__init__(parent)
        self.controller = controller
        self.device_icons = {}
        self.current_room = current_room
        
        self._create_canvas()
        self._draw_room()
        self._place_devices()
    
    def set_room(self, room_name: str):
        """Đổi phòng hiện tại.
        
        Args:
            room_name: Tên phòng hoặc "Tất cả"
        """
        self.current_room = room_name
        self.refresh()
    
    def _create_canvas(self):
        """Tạo canvas."""
        self.canvas = tk.Canvas(self, height=500, bg="#f5f5dc", relief="sunken", bd=2)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Bind resize event
        self.canvas.bind('<Configure>', self._on_canvas_resize)
    
    def _draw_room(self):
        """Vẽ layout phòng."""
        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Skip if canvas not yet rendered
        if canvas_width <= 1 or canvas_height <= 1:
            return
        
        # Calculate floor dimensions with margins
        margin = 50
        floor_x1 = margin
        floor_y1 = margin
        floor_x2 = canvas_width - margin
        floor_y2 = canvas_height - margin
        
        # Draw floor
        self.canvas.create_rectangle(floor_x1, floor_y1, floor_x2, floor_y2, 
                                     fill="#e6e6d0", outline="#8b8b7a", width=3)
        
        # Draw title
        room_display = self.current_room if self.current_room != "Tất cả" else "Tất cả phòng"
        center_x = canvas_width // 2
        self.canvas.create_text(center_x, 30, text=f"🏠 {room_display}", font=("Arial", 14, "bold"))
        
        # Draw grid lines (subtle)
        for i in range(floor_x1 + 200, floor_x2, 100):
            self.canvas.create_line(i, floor_y1, i, floor_y2, fill="#d0d0c0", dash=(2, 4))
        for i in range(floor_y1 + 50, floor_y2, 50):
            self.canvas.create_line(floor_x1, i, floor_x2, i, fill="#d0d0c0", dash=(2, 4))
    
    def _place_devices(self):
        """Đặt các thiết bị vào sơ đồ."""
        devices = self.controller.get_all_devices()
        
        # Filter by room if needed
        if self.current_room != "Tất cả":
            devices = [d for d in devices if d.room == self.current_room]
        
        # Calculate positions
        positions = self._calculate_positions(len(devices))
        
        # Skip if positions not calculated yet (canvas not rendered)
        if len(positions) < len(devices):
            return
        
        for i, device in enumerate(devices):
            x, y = positions[i]
            self._create_device_icon(device, x, y)
    
    def _calculate_positions(self, count):
        """Tính toán vị trí cho các thiết bị.
        
        Args:
            count: Số lượng thiết bị
            
        Returns:
            List các tuple (x, y)
        """
        positions = []
        
        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Skip if canvas not yet rendered
        if canvas_width <= 1 or canvas_height <= 1:
            return positions
        
        # Calculate floor dimensions
        floor_margin = 50
        device_margin_x = 150
        device_margin_y = 70
        
        floor_width = canvas_width - 2 * floor_margin
        floor_height = canvas_height - 2 * floor_margin
        
        available_width = floor_width - 2 * device_margin_x
        
        # Icon radius = 30, minimum gap between icons = 40px
        # So minimum center-to-center distance = 2*30 + 40 = 100px
        min_spacing = 100
        
        # Calculate how many devices can fit per row
        max_per_row = max(1, (available_width + min_spacing) // min_spacing)
        
        # Calculate number of rows needed
        import math
        num_rows = math.ceil(count / max_per_row)
        
        # Calculate vertical spacing
        spacing_y = 100  # Fixed spacing between rows
        start_x = floor_margin + device_margin_x
        start_y = floor_margin + device_margin_y
        
        # Calculate fixed horizontal spacing based on max_per_row
        spacing_x = (available_width // max(1, max_per_row - 1)) if max_per_row > 1 else 0
        spacing_x = max(spacing_x, min_spacing)
        
        # Place devices in grid layout (unlimited rows, left to right)
        for i in range(count):
            row = i // max_per_row
            col = i % max_per_row
            
            # Calculate x position (always from left to right)
            x = start_x + col * spacing_x
            
            # Calculate y position
            y = start_y + row * spacing_y
            
            positions.append((x, y))
        
        return positions
    
    def _get_light_color(self, device):
        """Tính màu cho đèn dựa trên độ sáng.
        
        Args:
            device: Đối tượng thiết bị đèn
            
        Returns:
            Màu RGB hex string
        """
        if not device.is_on:
            return 'gray'
        
        # Tính màu vàng dựa trên độ sáng (0-100)
        brightness = getattr(device, 'brightness', 100)
        # Từ màu vàng đậm (255, 255, 0) đến vàng nhạt theo brightness
        r = 255
        g = 255
        b = int(255 * (1 - brightness / 100))  # Giảm blue theo độ sáng
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def _create_device_icon(self, device, x, y):
        """Tạo icon cho thiết bị.
        
        Args:
            device: Đối tượng thiết bị
            x, y: Tọa độ
        """
        device_type = device.get_status()['device_type']
        
        # Icon mapping
        icons = {
            'light': ('💡', 'yellow', 'gray'),
            'fan': ('🌀', 'lightblue', 'gray'),
            'door': ('🚪', 'brown', 'gray')
        }
        
        icon, color_on, color_off = icons.get(device_type, ('🔌', 'green', 'gray'))
        
        # Get color based on device state
        if device_type == 'light':
            fill_color = self._get_light_color(device)
        else:
            fill_color = color_on if device.is_on else color_off
        
        # Draw circle background
        r = 30
        circle = self.canvas.create_oval(
            x - r, y - r, x + r, y + r,
            fill=fill_color,
            outline="black", width=2
        )
        
        # Draw icon
        icon_id = self.canvas.create_text(
            x, y - 5, text=icon, font=("Arial", 24)
        )
        
        # Draw label
        label_id = self.canvas.create_text(
            x, y + r + 15, text=device.name,
            font=("Arial", 9)
        )
        
        # Store references
        self.device_icons[device.device_id] = {
            'circle': circle,
            'icon': icon_id,
            'label': label_id,
            'color_on': color_on,
            'color_off': color_off,
            'device_type': device_type
        }
        
        # Bind click events
        self.canvas.tag_bind(circle, '<Button-1>', lambda e, did=device.device_id: self._on_device_click(did))
        self.canvas.tag_bind(icon_id, '<Button-1>', lambda e, did=device.device_id: self._on_device_click(did))
        self.canvas.tag_bind(label_id, '<Button-1>', lambda e, did=device.device_id: self._on_device_click(did))
        
        # Bind hover effects
        self.canvas.tag_bind(circle, '<Enter>', lambda e, c=circle: self._on_hover_enter(c))
        self.canvas.tag_bind(circle, '<Leave>', lambda e, c=circle: self._on_hover_leave(c))
        self.canvas.tag_bind(icon_id, '<Enter>', lambda e, c=circle: self._on_hover_enter(c))
        self.canvas.tag_bind(icon_id, '<Leave>', lambda e, c=circle: self._on_hover_leave(c))
    
    def _on_hover_enter(self, circle_id):
        """Xử lý khi hover vào thiết bị."""
        self.canvas.itemconfig(circle_id, width=4)
        self.canvas.config(cursor="hand2")
    
    def _on_hover_leave(self, circle_id):
        """Xử lý khi hover ra khỏi thiết bị."""
        self.canvas.itemconfig(circle_id, width=2)
        self.canvas.config(cursor="")
    
    def _on_device_click(self, device_id: str):
        """Xử lý khi click vào thiết bị.
        
        Args:
            device_id: ID của thiết bị được click
        """
        device = self.controller.get_device(device_id)
        if device:
            popup = DevicePopup(self, device, self.controller)
            # Center popup relative to main window
            popup.update_idletasks()
            x = self.winfo_toplevel().winfo_x() + (self.winfo_toplevel().winfo_width() // 2) - (popup.winfo_width() // 2)
            y = self.winfo_toplevel().winfo_y() + (self.winfo_toplevel().winfo_height() // 2) - (popup.winfo_height() // 2)
            popup.geometry(f"+{x}+{y}")
    
    def _on_canvas_resize(self, event):
        """Xử lý khi canvas thay đổi kích thước."""
        # Debounce resize events
        if hasattr(self, '_resize_timer'):
            self.after_cancel(self._resize_timer)
        self._resize_timer = self.after(100, self.refresh)
    
    def update_device_icon(self, device_id: str):
        """Cập nhật icon thiết bị.
        
        Args:
            device_id: ID của thiết bị
        """
        if device_id not in self.device_icons:
            return
        
        device = self.controller.get_device(device_id)
        if not device:
            return
        
        icon_data = self.device_icons[device_id]
        
        # Get color based on device type
        if icon_data.get('device_type') == 'light':
            color = self._get_light_color(device)
        else:
            color = icon_data['color_on'] if device.is_on else icon_data['color_off']
        
        self.canvas.itemconfig(icon_data['circle'], fill=color)
    
    def refresh(self):
        """Làm mới toàn bộ canvas."""
        self.canvas.delete("all")
        self.device_icons.clear()
        self._draw_room()
        self._place_devices()
