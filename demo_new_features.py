"""Demo các tính năng mới của Smart Home Controller v1.1"""

import sys
from application.device_controller import DeviceController
from simulation.light_simulator import Light
from simulation.fan_simulator import Fan
from simulation.door_simulator import Door


def demo_dynamic_device_management():
    """Demo 1: Thêm và xóa thiết bị động."""
    print("\n" + "="*60)
    print("DEMO 1: QUẢN LÝ THIẾT BỊ ĐỘNG")
    print("="*60)
    
    controller = DeviceController()
    
    # Ban đầu không có thiết bị
    print("\n📊 Trạng thái ban đầu:")
    print(f"Số thiết bị: {controller.get_summary()['total_devices']}")
    
    # Thêm thiết bị mới
    print("\n➕ Thêm 3 thiết bị mới:")
    
    light1 = Light("light_001", "Đèn trần phòng khách", "Phòng khách")
    controller.add_device(light1)
    
    fan1 = Fan("fan_001", "Quạt phòng ngủ", "Phòng ngủ")
    controller.add_device(fan1)
    
    door1 = Door("door_001", "Cửa chính", "Lối vào")
    controller.add_device(door1)
    
    print(f"\n📊 Sau khi thêm: {controller.get_summary()['total_devices']} thiết bị")
    
    # Liệt kê thiết bị
    print("\n📋 Danh sách thiết bị:")
    for device in controller.get_all_devices():
        print(f"  - {device.name} ({device.room})")
    
    # Xóa thiết bị
    print("\n🗑️ Xóa thiết bị 'fan_001':")
    controller.remove_device("fan_001")
    
    print(f"\n📊 Sau khi xóa: {controller.get_summary()['total_devices']} thiết bị")
    print("\n📋 Danh sách còn lại:")
    for device in controller.get_all_devices():
        print(f"  - {device.name} ({device.room})")


def demo_room_filtering():
    """Demo 2: Lọc thiết bị theo phòng."""
    print("\n" + "="*60)
    print("DEMO 2: LỌC THIẾT BỊ THEO PHÒNG")
    print("="*60)
    
    controller = DeviceController()
    
    # Thêm nhiều thiết bị vào nhiều phòng
    print("\n➕ Tạo hệ thống với nhiều phòng:")
    
    devices = [
        Light("light_001", "Đèn trần", "Phòng khách"),
        Light("light_002", "Đèn bàn", "Phòng khách"),
        Fan("fan_001", "Quạt trần", "Phòng khách"),
        
        Light("light_003", "Đèn ngủ", "Phòng ngủ"),
        Fan("fan_002", "Quạt đứng", "Phòng ngủ"),
        Door("door_001", "Cửa phòng", "Phòng ngủ"),
        
        Light("light_004", "Đèn bếp", "Bếp"),
        Fan("fan_003", "Quạt hút", "Bếp"),
    ]
    
    for device in devices:
        controller.add_device(device)
    
    print(f"Tổng số: {len(devices)} thiết bị")
    
    # Lấy danh sách phòng
    rooms = sorted(set(d.room for d in controller.get_all_devices()))
    print(f"\n🏠 Các phòng: {', '.join(rooms)}")
    
    # Lọc theo từng phòng
    for room in rooms:
        devices_in_room = [d for d in controller.get_all_devices() if d.room == room]
        print(f"\n📍 {room}:")
        for device in devices_in_room:
            device_type = device.get_status()['device_type']
            icon = {'light': '💡', 'fan': '🌀', 'door': '🚪'}[device_type]
            print(f"  {icon} {device.name}")


def demo_quick_control():
    """Demo 3: Điều khiển nhanh thiết bị."""
    print("\n" + "="*60)
    print("DEMO 3: ĐIỀU KHIỂN NHANH")
    print("="*60)
    
    controller = DeviceController()
    
    # Thêm thiết bị
    light = Light("light_001", "Đèn phòng khách", "Phòng khách")
    fan = Fan("fan_001", "Quạt phòng khách", "Phòng khách")
    door = Door("door_001", "Cửa chính", "Lối vào")
    
    controller.add_device(light)
    controller.add_device(fan)
    controller.add_device(door)
    
    print("\n🎮 Điều khiển nhanh:")
    
    # Light: toggle + brightness
    print("\n💡 Đèn:")
    controller.control_device("light_001", "turn_on")
    print(f"  Trạng thái: {'🟢 Bật' if light.is_on else '🔴 Tắt'}")
    controller.control_device("light_001", "set_brightness", {"brightness": 75})
    print(f"  Độ sáng: {light.brightness}%")
    
    # Fan: toggle + speed
    print("\n🌀 Quạt:")
    controller.control_device("fan_001", "turn_on")
    print(f"  Trạng thái: {'🟢 Bật' if fan.is_on else '🔴 Tắt'}")
    controller.control_device("fan_001", "set_speed", {"speed": 3})
    print(f"  Tốc độ: {fan.speed} ({fan.SPEED_NAMES[fan.speed]})")
    
    # Door: open + lock
    print("\n🚪 Cửa:")
    controller.control_device("door_001", "open")
    print(f"  Trạng thái: {door.state}")
    controller.control_device("door_001", "close")
    controller.control_device("door_001", "lock")
    print(f"  Trạng thái: {door.state} 🔒")


def demo_room_reorganization():
    """Demo 4: Tổ chức lại phòng."""
    print("\n" + "="*60)
    print("DEMO 4: TỔ CHỨC LẠI PHÒNG")
    print("="*60)
    
    controller = DeviceController()
    
    # Thêm thiết bị với phòng ban đầu
    print("\n➕ Cấu hình ban đầu:")
    light = Light("light_001", "Đèn", "Phòng A")
    fan = Fan("fan_001", "Quạt", "Phòng A")
    
    controller.add_device(light)
    controller.add_device(fan)
    
    for device in controller.get_all_devices():
        print(f"  {device.name} → {device.room}")
    
    # Di chuyển thiết bị sang phòng mới (simulate bằng cách xóa và thêm lại)
    print("\n🔄 Di chuyển thiết bị sang 'Phòng B':")
    
    # Cách 1: Trực tiếp thay đổi thuộc tính (trong simulation layer)
    light.room = "Phòng B"
    fan.room = "Phòng B"
    
    print("\n📊 Sau khi di chuyển:")
    for device in controller.get_all_devices():
        print(f"  {device.name} → {device.room}")
    
    # Thống kê theo phòng
    rooms = {}
    for device in controller.get_all_devices():
        rooms[device.room] = rooms.get(device.room, 0) + 1
    
    print("\n📈 Thống kê:")
    for room, count in rooms.items():
        print(f"  {room}: {count} thiết bị")


def demo_device_id_generation():
    """Demo 5: Tự động tạo ID cho thiết bị mới."""
    print("\n" + "="*60)
    print("DEMO 5: TỰ ĐỘNG TẠO DEVICE ID")
    print("="*60)
    
    controller = DeviceController()
    
    print("\n🔢 Tạo ID tự động cho thiết bị mới:")
    
    device_types = [
        ("light", Light, "💡 Đèn"),
        ("fan", Fan, "🌀 Quạt"),
        ("door", Door, "🚪 Cửa"),
    ]
    
    for device_type, DeviceClass, name in device_types:
        print(f"\n{name}:")
        
        # Tạo 3 thiết bị cùng loại
        for i in range(1, 4):
            # Generate ID
            existing_count = len([d for d in controller.get_all_devices() 
                                if d.get_status()['device_type'] == device_type])
            device_id = f"{device_type}_{existing_count + 1:03d}"
            
            # Create device
            device = DeviceClass(device_id, f"{name} {i}", f"Phòng {i}")
            controller.add_device(device)
            
            print(f"  Đã tạo: {device_id} - {device.name}")
    
    print(f"\n📊 Tổng số thiết bị: {controller.get_summary()['total_devices']}")


def demo_multi_room_visualization():
    """Demo 6: Mô phỏng hiển thị nhiều phòng."""
    print("\n" + "="*60)
    print("DEMO 6: HIỂN THỊ NHIỀU PHÒNG")
    print("="*60)
    
    controller = DeviceController()
    
    # Tạo hệ thống hoàn chỉnh
    print("\n🏠 Thiết lập Smart Home hoàn chỉnh:")
    
    rooms_config = {
        "Phòng khách": [
            ("light", "Đèn trần"),
            ("light", "Đèn tường"),
            ("fan", "Quạt trần"),
        ],
        "Phòng ngủ chính": [
            ("light", "Đèn ngủ"),
            ("fan", "Quạt đứng"),
            ("door", "Cửa phòng"),
        ],
        "Phòng ngủ trẻ em": [
            ("light", "Đèn học"),
            ("light", "Đèn ngủ"),
        ],
        "Bếp": [
            ("light", "Đèn bếp"),
            ("fan", "Quạt hút"),
        ],
        "Nhà tắm": [
            ("light", "Đèn nhà tắm"),
            ("fan", "Quạt thông gió"),
        ],
    }
    
    device_classes = {
        "light": Light,
        "fan": Fan,
        "door": Door,
    }
    
    device_id_counters = {"light": 0, "fan": 0, "door": 0}
    
    for room, devices_list in rooms_config.items():
        print(f"\n📍 {room}:")
        for device_type, device_name in devices_list:
            device_id_counters[device_type] += 1
            device_id = f"{device_type}_{device_id_counters[device_type]:03d}"
            
            DeviceClass = device_classes[device_type]
            device = DeviceClass(device_id, device_name, room)
            controller.add_device(device)
            
            icon = {'light': '💡', 'fan': '🌀', 'door': '🚪'}[device_type]
            print(f"  {icon} {device_name} ({device_id})")
    
    # Tổng quan
    print("\n" + "-"*60)
    summary = controller.get_summary()
    print(f"📊 TỔNG QUAN:")
    print(f"  Tổng số phòng: {len(rooms_config)}")
    print(f"  Tổng số thiết bị: {summary['total_devices']}")
    print(f"  Đang bật: {summary['devices_on']}")
    print(f"  Đang tắt: {summary['devices_off']}")
    
    # Thống kê theo loại
    device_type_count = {}
    for device in controller.get_all_devices():
        dtype = device.get_status()['device_type']
        device_type_count[dtype] = device_type_count.get(dtype, 0) + 1
    
    print(f"\n  Theo loại:")
    for dtype, count in sorted(device_type_count.items()):
        icon = {'light': '💡', 'fan': '🌀', 'door': '🚪'}.get(dtype, '🔌')
        print(f"    {icon} {dtype.capitalize()}: {count}")


def main():
    """Chạy tất cả demos."""
    print("\n" + "🏠"*20)
    print("SMART HOME CONTROLLER v1.1 - NEW FEATURES DEMO")
    print("🏠"*20)
    
    demos = [
        demo_dynamic_device_management,
        demo_room_filtering,
        demo_quick_control,
        demo_room_reorganization,
        demo_device_id_generation,
        demo_multi_room_visualization,
    ]
    
    for i, demo_func in enumerate(demos, 1):
        demo_func()
        
        if i < len(demos):
            input("\n⏸️  Nhấn Enter để tiếp tục...")
    
    print("\n" + "="*60)
    print("✅ HOÀN THÀNH TẤT CẢ DEMOS")
    print("="*60)
    print("\n💡 Gợi ý: Chạy 'python main.py' để test GUI!")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Đã dừng demo.")
        sys.exit(0)
