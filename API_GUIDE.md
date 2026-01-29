# Smart Home Controller API - Hướng dẫn sử dụng

## 📱 Kết nối từ App Android

### Bước 1: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Bước 2: Chạy API Server

**Chạy cả GUI và API:**
```bash
python main.py
```

**Chỉ chạy API (không GUI):**
```bash
python main.py --api-only
```

**Chỉ chạy GUI (không API):**
```bash
python main.py --no-api
```

### Bước 3: Expose API với Playit.gg

1. Tải và cài đặt playit: https://playit.gg/
2. Chạy lệnh:
```bash
playit
```
3. Chọn port 5000
4. Playit sẽ tạo một URL công khai (VD: `https://abc123.playit.gg`)
5. Sử dụng URL này trong app Android

---

## 📋 API Endpoints

### Base URL
```
http://localhost:5000/api
```

hoặc URL từ playit:
```
https://your-playit-url.playit.gg/api
```

---

## 🔌 Devices API

### 1. Lấy danh sách tất cả thiết bị
```http
GET /api/devices
```

**Response:**
```json
{
  "success": true,
  "count": 7,
  "devices": [
    {
      "device_id": "light_001",
      "name": "Đèn phòng khách",
      "room": "Phòng khách",
      "device_type": "light",
      "is_on": true,
      "brightness": 80,
      "last_update": "2026-01-29T10:30:00"
    },
    {
      "device_id": "door_001",
      "name": "Cửa chính",
      "room": "Cửa ra vào",
      "device_type": "door",
      "is_on": false,
      "state": "locked",
      "state_name": "Khóa",
      "is_locked": true,
      "last_update": "2026-01-29T10:25:00"
    }
  ]
}
```

### 2. Lấy thông tin một thiết bị
```http
GET /api/devices/{device_id}
```

**Response:**
```json
{
  "success": true,
  "device": {
    "device_id": "light_001",
    "name": "Đèn phòng khách",
    "is_on": true,
    "brightness": 80
  }
}
```

### 3. Điều khiển thiết bị
```http
POST /api/devices/{device_id}/control
Content-Type: application/json
```

**Request Body - Bật/Tắt thiết bị:**
```json
{
  "command": "turn_on"
}
```
hoặc
```json
{
  "command": "turn_off"
}
```

**Request Body - Khóa cửa (tự động đóng và khóa):**
```json
{
  "command": "lock_with_close"
}
```

**Request Body - Mở khóa cửa:**
```json
{
  "command": "unlock"
}
```

**Request Body - Điều chỉnh độ sáng đèn:**
```json
{
  "command": "set_brightness",
  "params": {
    "brightness": 75
  }
}
```

**Request Body - Điều chỉnh tốc độ quạt:**
```json
{
  "command": "set_speed",
  "params": {
    "speed": 2
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Command turn_on executed successfully",
  "device": {
    "device_id": "light_001",
    "name": "Đèn phòng khách",
    "is_on": true,
    "brightness": 80
  }
}
```

### 4. Lấy danh sách phòng và thiết bị
```http
GET /api/rooms
```

**Response:**
```json
{
  "success": true,
  "rooms": {
    "Phòng khách": [
      {
        "device_id": "light_001",
        "name": "Đèn phòng khách",
        "device_type": "light",
        "is_on": true
      },
      {
        "device_id": "fan_001",
        "name": "Quạt phòng khách",
        "device_type": "fan",
        "is_on": false
      }
    ],
    "Phòng ngủ": [...]
  }
}
```

---

## ⏰ Timers API

### 1. Lấy danh sách timers
```http
GET /api/timers
```

**Response:**
```json
{
  "success": true,
  "count": 2,
  "timers": [
    {
      "timer_id": "timer_1",
      "device_id": "door_001",
      "device_name": "Cửa chính",
      "action": "lock_with_close",
      "scheduled_time": "2026-01-29T11:00:00",
      "delay_seconds": 300,
      "time_remaining": 245,
      "is_active": true
    }
  ]
}
```

### 2. Tạo timer mới
```http
POST /api/timers
Content-Type: application/json
```

**Request Body:**
```json
{
  "device_id": "door_001",
  "action": "lock_with_close",
  "delay_seconds": 300
}
```

**Các actions có thể:**
- `turn_on` - Bật thiết bị
- `turn_off` - Tắt thiết bị
- `lock` - Khóa cửa (cần cửa đóng trước)
- `lock_with_close` - Đóng và khóa cửa (khuyến nghị cho timer)
- `unlock` - Mở khóa cửa

**Response:**
```json
{
  "success": true,
  "message": "Timer created successfully",
  "timer": {
    "timer_id": "timer_1",
    "device_id": "door_001",
    "action": "lock_with_close",
    "time_remaining": 300
  }
}
```

### 3. Hủy timer
```http
DELETE /api/timers/{timer_id}
```

**Response:**
```json
{
  "success": true,
  "message": "Timer cancelled successfully"
}
```

### 4. Lấy timers của một thiết bị
```http
GET /api/timers/device/{device_id}
```

**Response:**
```json
{
  "success": true,
  "count": 1,
  "timers": [...]
}
```

---

## 🔍 Health Check

```http
GET /api/health
```

**Response:**
```json
{
  "status": "ok",
  "message": "Smart Home API is running"
}
```

---

## 💡 Ví dụ sử dụng với Android

### Retrofit Interface (Kotlin)
```kotlin
interface SmartHomeAPI {
    @GET("api/devices")
    suspend fun getDevices(): DevicesResponse
    
    @POST("api/devices/{deviceId}/control")
    suspend fun controlDevice(
        @Path("deviceId") deviceId: String,
        @Body command: ControlCommand
    ): ControlResponse
    
    @GET("api/timers")
    suspend fun getTimers(): TimersResponse
    
    @POST("api/timers")
    suspend fun createTimer(@Body timer: CreateTimerRequest): TimerResponse
    
    @DELETE("api/timers/{timerId}")
    suspend fun cancelTimer(@Path("timerId") timerId: String): Response<Unit>
}

data class ControlCommand(
    val command: String,
    val params: Map<String, Any>? = null
)

data class CreateTimerRequest(
    val device_id: String,
    val action: String,
    val delay_seconds: Int
)
```

### Sử dụng
```kotlin
// Bật đèn
val command = ControlCommand("turn_on")
api.controlDevice("light_001", command)

// Khóa cửa
val lockCommand = ControlCommand("lock_with_close")
api.controlDevice("door_001", lockCommand)

// Đặt hẹn giờ khóa cửa sau 5 phút
val timer = CreateTimerRequest(
    device_id = "door_001",
    action = "lock_with_close",
    delay_seconds = 300
)
api.createTimer(timer)
```

---

## ⚠️ Error Responses

**Device not found:**
```json
{
  "success": false,
  "error": "Device not found"
}
```

**Missing parameters:**
```json
{
  "success": false,
  "error": "Missing command parameter"
}
```

**Command failed:**
```json
{
  "success": false,
  "error": "Failed to execute command lock"
}
```

---

## 🚀 Tips cho App Android

1. **Lưu URL playit vào SharedPreferences**
2. **Thêm timeout cho requests (10-15 giây)**
3. **Xử lý lỗi mạng gracefully**
4. **Auto-refresh danh sách thiết bị mỗi 5-10 giây**
5. **Hiển thị loading state khi gọi API**
6. **Cache dữ liệu offline**

---

## 📱 Screenshot Flow

1. Màn hình nhập URL playit
2. Màn hình danh sách phòng/thiết bị
3. Màn hình điều khiển thiết bị
4. Màn hình quản lý timer
