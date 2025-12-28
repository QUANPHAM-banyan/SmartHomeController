#!/usr/bin/env python3
"""
Demo Script - Minh họa sử dụng Smart Home Controller qua Console
(Không dùng GUI)
"""

import time
from simulation.light_simulator import Light
from simulation.fan_simulator import Fan
from simulation.door_simulator import Door
from application.device_controller import DeviceController
from application.timer_manager import TimerManager


def demo_basic_control():
    """Demo điều khiển cơ bản."""
    print("\n" + "="*60)
    print("     DEMO 1: ĐIỀU KHIỂN CƠ BẢN")
    print("="*60)
    
    # Khởi tạo
    controller = DeviceController()
    
    # Tạo thiết bị
    light = Light("light_001", "Đèn phòng khách", "Phòng khách")
    fan = Fan("fan_001", "Quạt phòng ngủ", "Phòng ngủ")
    door = Door("door_001", "Cửa chính", "Cửa ra vào")
    
    controller.add_device(light)
    controller.add_device(fan)
    controller.add_device(door)
    
    print("\n--- Điều khiển đèn ---")
    controller.control_device("light_001", "turn_on")
    controller.control_device("light_001", "set_brightness", {"level": 50})
    time.sleep(1)
    controller.control_device("light_001", "set_brightness", {"level": 100})
    time.sleep(1)
    controller.control_device("light_001", "turn_off")
    
    print("\n--- Điều khiển quạt ---")
    controller.control_device("fan_001", "turn_on")
    time.sleep(1)
    controller.control_device("fan_001", "set_speed", {"speed": 2})
    time.sleep(1)
    controller.control_device("fan_001", "set_speed", {"speed": 3})
    time.sleep(1)
    controller.control_device("fan_001", "turn_off")
    
    print("\n--- Điều khiển cửa ---")
    controller.control_device("door_001", "open")
    time.sleep(1)
    controller.control_device("door_001", "close")
    time.sleep(1)
    controller.control_device("door_001", "lock")
    time.sleep(1)
    controller.control_device("door_001", "open")  # Sẽ fail vì đang khóa
    controller.control_device("door_001", "unlock")
    controller.control_device("door_001", "open")  # Bây giờ OK
    
    # In tổng kết
    controller.print_summary()


def demo_timer_system():
    """Demo hệ thống hẹn giờ."""
    print("\n" + "="*60)
    print("     DEMO 2: HỆ THỐNG HẸN GIỜ")
    print("="*60)
    
    controller = DeviceController()
    timer_manager = TimerManager(controller)
    
    # Tạo thiết bị
    light = Light("light_001", "Đèn phòng khách", "Phòng khách")
    controller.add_device(light)
    
    print("\n--- Bật đèn ngay ---")
    controller.control_device("light_001", "turn_on")
    
    print("\n--- Đặt hẹn giờ tắt đèn sau 5 giây ---")
    timer_manager.schedule_timer("light_001", "turn_off", 5)
    
    print("\n--- Đặt thêm hẹn giờ bật lại sau 10 giây ---")
    timer_manager.schedule_timer("light_001", "turn_on", 10)
    
    # Hiển thị timers đang chạy
    timer_manager.print_active_timers()
    
    print("\n⏳ Đang chờ timers kích hoạt...")
    print("   (Chờ 12 giây để xem kết quả)\n")
    
    # Chờ timers thực thi
    time.sleep(12)
    
    print("\n✅ Demo hẹn giờ hoàn tất!")


def demo_observer_pattern():
    """Demo Observer Pattern."""
    print("\n" + "="*60)
    print("     DEMO 3: OBSERVER PATTERN")
    print("="*60)
    
    from application.device_controller import Observer
    
    class ConsoleObserver(Observer):
        """Observer in ra console khi device thay đổi."""
        def update(self, device_id: str):
            print(f"  🔔 Observer nhận thông báo: Device {device_id} đã thay đổi!")
    
    controller = DeviceController()
    
    # Đăng ký observer
    observer = ConsoleObserver()
    controller.register_observer(observer)
    
    # Tạo thiết bị
    light = Light("light_001", "Đèn test", "Test room")
    controller.add_device(light)
    
    print("\n--- Thay đổi thiết bị sẽ trigger observer ---")
    controller.control_device("light_001", "turn_on")
    time.sleep(0.5)
    controller.control_device("light_001", "set_brightness", {"level": 75})
    time.sleep(0.5)
    controller.control_device("light_001", "turn_off")


def demo_multiple_devices():
    """Demo quản lý nhiều thiết bị."""
    print("\n" + "="*60)
    print("     DEMO 4: QUẢN LÝ NHIỀU THIẾT BỊ")
    print("="*60)
    
    controller = DeviceController()
    
    # Tạo nhiều thiết bị cho nhiều phòng
    rooms = {
        "Phòng khách": [
            Light("light_living", "Đèn trần", "Phòng khách"),
            Fan("fan_living", "Quạt trần", "Phòng khách")
        ],
        "Phòng ngủ": [
            Light("light_bed", "Đèn ngủ", "Phòng ngủ"),
            Fan("fan_bed", "Quạt đứng", "Phòng ngủ"),
            Door("door_bed", "Cửa phòng", "Phòng ngủ")
        ],
        "Bếp": [
            Light("light_kitchen", "Đèn bếp", "Bếp")
        ]
    }
    
    # Thêm tất cả thiết bị
    for room, devices in rooms.items():
        for device in devices:
            controller.add_device(device)
    
    print("\n--- Bật tất cả đèn ---")
    lights = controller.get_devices_by_type("light")
    for light in lights:
        controller.control_device(light.device_id, "turn_on")
    
    print("\n--- Bật tất cả quạt ở tốc độ cao ---")
    fans = controller.get_devices_by_type("fan")
    for fan in fans:
        controller.control_device(fan.device_id, "turn_on")
        controller.control_device(fan.device_id, "set_speed", {"speed": 3})
    
    print("\n--- Khóa tất cả cửa ---")
    doors = controller.get_devices_by_type("door")
    for door in doors:
        controller.control_device(door.device_id, "lock")
    
    # Xem devices theo phòng
    print("\n--- Thiết bị trong Phòng ngủ ---")
    bedroom_devices = controller.get_devices_by_room("Phòng ngủ")
    for device in bedroom_devices:
        print(f"  {device}")
    
    controller.print_summary()


def demo_error_handling():
    """Demo xử lý lỗi."""
    print("\n" + "="*60)
    print("     DEMO 5: XỬ LÝ LỖI")
    print("="*60)
    
    controller = DeviceController()
    light = Light("light_001", "Đèn test", "Test")
    controller.add_device(light)
    
    print("\n--- Test các trường hợp lỗi ---")
    
    # Lỗi: Device không tồn tại
    print("\n1. Điều khiển device không tồn tại:")
    controller.control_device("light_999", "turn_on")
    
    # Lỗi: Command không hợp lệ
    print("\n2. Command không hợp lệ:")
    controller.control_device("light_001", "fly")
    
    # Lỗi: Brightness out of range
    print("\n3. Brightness vượt quá giới hạn:")
    controller.control_device("light_001", "set_brightness", {"level": 150})
    
    # Lỗi: Thêm device trùng ID
    print("\n4. Thêm device trùng ID:")
    duplicate = Light("light_001", "Đèn trùng", "Test")
    controller.add_device(duplicate)
    
    print("\n✅ Hệ thống xử lý lỗi ổn định!")


def main():
    """Chạy tất cả demos."""
    print("\n" + "="*60)
    print("    🏠 SMART HOME CONTROLLER - DEMO SCRIPT 🏠")
    print("="*60)
    print("  Các demo sẽ chạy tuần tự, mỗi demo cách nhau 3 giây")
    print("="*60)
    
    demos = [
        ("Điều khiển cơ bản", demo_basic_control),
        ("Hệ thống hẹn giờ", demo_timer_system),
        ("Observer Pattern", demo_observer_pattern),
        ("Quản lý nhiều thiết bị", demo_multiple_devices),
        ("Xử lý lỗi", demo_error_handling)
    ]
    
    for i, (name, func) in enumerate(demos, 1):
        print(f"\n\n{'='*60}")
        print(f"  >>> CHUẨN BỊ DEMO {i}/{len(demos)}: {name.upper()}")
        print(f"{'='*60}")
        time.sleep(2)
        
        try:
            func()
        except Exception as e:
            print(f"\n❌ Lỗi trong demo: {e}")
            import traceback
            traceback.print_exc()
        
        if i < len(demos):
            print("\n⏳ Chờ 3 giây trước demo tiếp theo...")
            time.sleep(3)
    
    print("\n\n" + "="*60)
    print("      🎉 TẤT CẢ DEMOS ĐÃ HOÀN TẤT! 🎉")
    print("="*60)
    print("\n💡 Để chạy GUI, sử dụng: python main.py")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo bị dừng bởi người dùng")
        print("👋 Tạm biệt!\n")
