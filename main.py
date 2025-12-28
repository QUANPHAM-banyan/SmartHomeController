#!/usr/bin/env python3
"""
Smart Home Controller - Main Entry Point
Hệ thống mô phỏng điều khiển thiết bị IoT trong gia đình
"""

from simulation.light_simulator import Light
from simulation.fan_simulator import Fan
from simulation.door_simulator import Door
from application.device_controller import DeviceController
from application.timer_manager import TimerManager
from presentation.gui import MainWindow


def create_sample_devices(controller):
    """Tạo các thiết bị mẫu cho demo.
    
    Args:
        controller: DeviceController instance
    """
    print("\n" + "="*60)
    print("        TẠO THIẾT BỊ MẪU")
    print("="*60)
    
    # Tạo đèn
    light1 = Light("light_001", "Đèn phòng khách", "Phòng khách", brightness=80)
    light2 = Light("light_002", "Đèn phòng ngủ", "Phòng ngủ", brightness=60)
    light3 = Light("light_003", "Đèn bếp", "Bếp", brightness=100)
    
    # Tạo quạt
    fan1 = Fan("fan_001", "Quạt phòng khách", "Phòng khách", speed=Fan.SPEED_MEDIUM)
    fan2 = Fan("fan_002", "Quạt phòng ngủ", "Phòng ngủ", speed=Fan.SPEED_LOW)
    
    # Tạo cửa
    door1 = Door("door_001", "Cửa chính", "Cửa ra vào")
    door2 = Door("door_002", "Cửa phòng ngủ", "Phòng ngủ")
    
    # Thêm vào controller
    devices = [light1, light2, light3, fan1, fan2, door1, door2]
    for device in devices:
        controller.add_device(device)
    
    print("="*60 + "\n")


def print_welcome():
    """In thông báo chào mừng."""
    print("\n" + "="*60)
    print("      🏠 SMART HOME CONTROLLER 🏠")
    print("="*60)
    print("  Hệ thống mô phỏng điều khiển thiết bị IoT")
    print("="*60 + "\n")


def main():
    """Hàm main - khởi chạy ứng dụng."""
    try:
        # Print welcome message
        print_welcome()
        
        # Khởi tạo controller (Singleton)
        print("🔧 Khởi tạo hệ thống...")
        controller = DeviceController()
        
        # Khởi tạo timer manager
        timer_manager = TimerManager(controller)
        
        # Tạo thiết bị mẫu
        create_sample_devices(controller)
        
        # In thông tin hệ thống
        controller.print_summary()
        
        # Demo một vài lệnh điều khiển
        print("🧪 Demo điều khiển thiết bị:")
        print("-" * 60)
        controller.control_device("light_001", "turn_on")
        controller.control_device("fan_001", "turn_on")
        controller.control_device("door_001", "lock")
        print("-" * 60 + "\n")
        
        # Khởi tạo GUI
        print("🖥️  Khởi động giao diện...")
        app = MainWindow(controller, timer_manager)
        
        print("✅ Ứng dụng đã sẵn sàng!")
        print("="*60 + "\n")
        
        # Chạy GUI
        app.run()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Nhận tín hiệu dừng (Ctrl+C)")
        print("🛑 Đang dọn dẹp...")
    except Exception as e:
        print(f"\n❌ LỖI: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n👋 Cảm ơn bạn đã sử dụng Smart Home Controller!")
        print("="*60 + "\n")


if __name__ == "__main__":
    main()

