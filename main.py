#!/usr/bin/env python3
"""
Smart Home Controller - Main Entry Point
Hệ thống mô phỏng điều khiển thiết bị IoT trong gia đình
"""

from application.device_controller import DeviceController
from application.timer_manager import TimerManager
from application.storage_manager import StorageManager
from presentation.main_window import MainWindow
from api.api_server import APIServer
import sys


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
        
        # Kiểm tra command line arguments
        api_only = '--api-only' in sys.argv
        no_api = '--no-api' in sys.argv
        
        # Khởi tạo controller (Singleton)
        print("🔧 Khởi tạo hệ thống...")
        controller = DeviceController()
        
        # Khởi tạo storage manager
        storage = StorageManager("devices_state.json")
        
        # Khởi tạo timer manager
        timer_manager = TimerManager(controller)
        
        # Thử load trạng thái đã lưu
        saved_data = storage.load_state()
        if saved_data:
            # Khôi phục từ file JSON
            restored = storage.restore_devices(controller, saved_data)
            if restored > 0:
                print(f"✅ Đã khôi phục {restored} thiết bị từ lần chạy trước")
        
        # In thông tin hệ thống
        controller.print_summary()
        
        # Khởi động API server (nếu không bị disable)
        api_server = None
        if not no_api:
            try:
                api_server = APIServer(controller, timer_manager, host='0.0.0.0', port=5000)
                api_server.start()
            except Exception as e:
                print(f"⚠️ Không thể khởi động API server: {e}")
                print("   Ứng dụng sẽ chạy chỉ với GUI")
        
        # Nếu chỉ chạy API (không GUI)
        if api_only:
            print("\n🌐 Chạy ở chế độ API-only (không có GUI)")
            print("   Nhấn Ctrl+C để dừng...")
            try:
                # Keep running until interrupted
                import time
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
        else:
            # Khởi tạo GUI
            print("🖥️  Khởi động giao diện...")
            app = MainWindow(controller, timer_manager, storage)
            
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
        print("="*60 + "\n")


if __name__ == "__main__":
    main()

