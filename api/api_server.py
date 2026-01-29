"""REST API Server - API cho Smart Home Controller.

API server cho phép điều khiển thiết bị từ xa qua HTTP requests.
Sử dụng Flask để tạo RESTful API.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
from typing import Optional


class APIServer:
    """REST API Server cho Smart Home Controller."""
    
    def __init__(self, controller, timer_manager, host='0.0.0.0', port=5000):
        """Khởi tạo API Server.
        
        Args:
            controller: DeviceController instance
            timer_manager: TimerManager instance
            host: Host address (default: 0.0.0.0 để accept từ mọi IP)
            port: Port number (default: 5000)
        """
        self.controller = controller
        self.timer_manager = timer_manager
        self.host = host
        self.port = port
        
        # Create Flask app
        self.app = Flask(__name__, static_folder='static', static_url_path='')
        CORS(self.app)  # Enable CORS để app Android có thể gọi API
        
        # Setup routes
        self._setup_routes()
        
        # Server thread
        self.server_thread: Optional[threading.Thread] = None
        self.is_running = False
        
        print(f"🌐 API Server đã khởi tạo tại {host}:{port}")
    
    def _setup_routes(self):
        """Setup các API routes."""
        
        # Serve web dashboard
        @self.app.route('/', methods=['GET'])
        def index():
            """Serve web dashboard."""
            return self.app.send_static_file('index.html')
        
        # Health check
        @self.app.route('/api/health', methods=['GET'])
        def health_check():
            """Health check endpoint."""
            return jsonify({
                'status': 'ok',
                'message': 'Smart Home API is running'
            })
        
        # ==================== DEVICES ENDPOINTS ====================
        
        @self.app.route('/api/devices', methods=['GET'])
        def get_devices():
            """Lấy danh sách tất cả thiết bị."""
            try:
                devices = self.controller.get_all_devices()
                devices_data = [self._device_to_dict(device) for device in devices]
                
                return jsonify({
                    'success': True,
                    'count': len(devices_data),
                    'devices': devices_data
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/devices/<device_id>', methods=['GET'])
        def get_device(device_id):
            """Lấy thông tin chi tiết một thiết bị."""
            try:
                device = self.controller.get_device(device_id)
                if not device:
                    return jsonify({
                        'success': False,
                        'error': 'Device not found'
                    }), 404
                
                return jsonify({
                    'success': True,
                    'device': self._device_to_dict(device)
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/devices/<device_id>/control', methods=['POST'])
        def control_device(device_id):
            """Điều khiển thiết bị.
            
            Request body:
            {
                "command": "turn_on" | "turn_off" | "lock" | "lock_with_close" | "unlock" | "set_brightness" | "set_speed",
                "params": {  // Optional
                    "brightness": 80,  // For set_brightness
                    "speed": 2  // For set_speed
                }
            }
            """
            try:
                data = request.get_json()
                if not data or 'command' not in data:
                    return jsonify({
                        'success': False,
                        'error': 'Missing command parameter'
                    }), 400
                
                command = data['command']
                params = data.get('params', {})
                
                # Validate device exists
                device = self.controller.get_device(device_id)
                if not device:
                    return jsonify({
                        'success': False,
                        'error': 'Device not found'
                    }), 404
                
                # Execute command
                result = self.controller.control_device(device_id, command, params)
                
                if result:
                    # Get updated device status
                    updated_device = self._device_to_dict(device)
                    
                    return jsonify({
                        'success': True,
                        'message': f'Command {command} executed successfully',
                        'device': updated_device
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': f'Failed to execute command {command}'
                    }), 400
                    
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/rooms', methods=['GET'])
        def get_rooms():
            """Lấy danh sách các phòng và thiết bị trong mỗi phòng."""
            try:
                all_devices = self.controller.get_all_devices()
                
                # Group devices by room
                rooms = {}
                for device in all_devices:
                    room = device.room
                    if room not in rooms:
                        rooms[room] = []
                    rooms[room].append(self._device_to_dict(device))
                
                return jsonify({
                    'success': True,
                    'rooms': rooms
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        # ==================== TIMERS ENDPOINTS ====================
        
        @self.app.route('/api/timers', methods=['GET'])
        def get_timers():
            """Lấy danh sách tất cả timers đang active."""
            try:
                timers = self.timer_manager.get_active_timers()
                timers_data = [self._timer_to_dict(timer) for timer in timers]
                
                return jsonify({
                    'success': True,
                    'count': len(timers_data),
                    'timers': timers_data
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/timers', methods=['POST'])
        def create_timer():
            """Tạo timer mới.
            
            Request body:
            {
                "device_id": "door_01",
                "action": "lock_with_close",
                "delay_seconds": 300
            }
            """
            try:
                data = request.get_json()
                
                # Validate required fields
                required_fields = ['device_id', 'action', 'delay_seconds']
                for field in required_fields:
                    if field not in data:
                        return jsonify({
                            'success': False,
                            'error': f'Missing required field: {field}'
                        }), 400
                
                device_id = data['device_id']
                action = data['action']
                delay_seconds = int(data['delay_seconds'])
                
                # Validate device exists
                device = self.controller.get_device(device_id)
                if not device:
                    return jsonify({
                        'success': False,
                        'error': 'Device not found'
                    }), 404
                
                # Create timer
                timer_id = self.timer_manager.schedule_timer(device_id, action, delay_seconds)
                
                if timer_id:
                    timer = self.timer_manager.get_timer(timer_id)
                    return jsonify({
                        'success': True,
                        'message': 'Timer created successfully',
                        'timer': self._timer_to_dict(timer)
                    }), 201
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Failed to create timer'
                    }), 400
                    
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/timers/<timer_id>', methods=['DELETE'])
        def cancel_timer(timer_id):
            """Hủy timer."""
            try:
                result = self.timer_manager.cancel_timer(timer_id)
                
                if result:
                    return jsonify({
                        'success': True,
                        'message': 'Timer cancelled successfully'
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Timer not found'
                    }), 404
                    
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/timers/device/<device_id>', methods=['GET'])
        def get_device_timers(device_id):
            """Lấy tất cả timers của một thiết bị."""
            try:
                timers = self.timer_manager.get_timers_for_device(device_id)
                timers_data = [self._timer_to_dict(timer) for timer in timers]
                
                return jsonify({
                    'success': True,
                    'count': len(timers_data),
                    'timers': timers_data
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
    
    def _device_to_dict(self, device) -> dict:
        """Chuyển đổi device object sang dictionary.
        
        Args:
            device: Device object
            
        Returns:
            Dictionary representation của device
        """
        status = device.get_status()
        device_dict = {
            'device_id': device.device_id,
            'name': device.name,
            'room': device.room,
            'device_type': status.get('device_type'),
            'is_on': status.get('is_on'),
            'last_update': status.get('last_update')
        }
        
        # Add device-specific fields
        if status.get('device_type') == 'light':
            device_dict['brightness'] = status.get('brightness')
        elif status.get('device_type') == 'fan':
            device_dict['speed'] = status.get('speed')
        elif status.get('device_type') == 'door':
            device_dict['state'] = status.get('state')
            device_dict['state_name'] = status.get('state_name')
            device_dict['is_locked'] = status.get('is_locked')
        
        return device_dict
    
    def _timer_to_dict(self, timer) -> dict:
        """Chuyển đổi timer object sang dictionary.
        
        Args:
            timer: TimerTask object
            
        Returns:
            Dictionary representation của timer
        """
        return {
            'timer_id': timer.timer_id,
            'device_id': timer.device_id,
            'device_name': timer.device_name,
            'action': timer.action,
            'scheduled_time': timer.scheduled_time.isoformat(),
            'delay_seconds': timer.delay_seconds,
            'time_remaining': timer.time_remaining(),
            'is_active': timer.is_active()
        }
    
    def start(self):
        """Khởi động API server trong background thread."""
        if self.is_running:
            print("⚠️ API Server đã đang chạy")
            return
        
        def run_server():
            """Chạy Flask server."""
            self.is_running = True
            print(f"\n{'='*60}")
            print(f"🚀 API Server đang chạy tại http://{self.host}:{self.port}")
            print(f"{'='*60}")
            print(f"🌐 Mở web dashboard tại:")
            print(f"   http://localhost:{self.port}")
            print(f"   hoặc từ điện thoại: http://<IP máy tính>:{self.port}")
            print(f"\n📱 Để truy cập từ xa (qua Internet):")
            print(f"   1. Sử dụng playit.gg để expose port {self.port}")
            print(f"   2. Mở URL playit trong browser điện thoại")
            print(f"\n📋 API Endpoints:")
            print(f"   GET  /api/health              - Health check")
            print(f"   GET  /api/devices             - Lấy danh sách thiết bị")
            print(f"   GET  /api/devices/<id>        - Lấy thông tin thiết bị")
            print(f"   POST /api/devices/<id>/control - Điều khiển thiết bị")
            print(f"   GET  /api/rooms               - Lấy danh sách phòng")
            print(f"   GET  /api/timers              - Lấy danh sách timer")
            print(f"   POST /api/timers              - Tạo timer mới")
            print(f"   DELETE /api/timers/<id>       - Hủy timer")
            print(f"{'='*60}\n")
            
            # Run Flask app
            self.app.run(
                host=self.host,
                port=self.port,
                debug=False,
                use_reloader=False,
                threaded=True
            )
        
        # Start server in background thread
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
    
    def stop(self):
        """Dừng API server."""
        self.is_running = False
        print("🛑 API Server đã dừng")
