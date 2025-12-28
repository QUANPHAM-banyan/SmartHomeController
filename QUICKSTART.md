# 🎯 Quick Start Guide - Smart Home Controller

## 🚀 Khởi động nhanh (30 giây)

```bash
# 1. Clone/Download project
cd SmartHomeController

# 2. Chạy ứng dụng (không cần cài đặt gì thêm!)
python main.py
```

**Yêu cầu**: Python 3.8+ (không cần dependencies khác)

---

## 📸 Giao diện

```
┌────────────────────────────────────────────────────────┐
│  🏠 SMART HOME CONTROLLER                              │
│  ═══════════════════════════════════════════════════   │
│  Menu: ⚙️ Thiết bị | 🏠 Phòng | ❓ Trợ giúp            │
├────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │  📍 Sơ đồ phòng: Phòng khách                    │  │
│  │                                                  │  │
│  │     💡         🌀         🚪                     │  │
│  │   Đèn trần   Quạt trần  Cửa chính              │  │
│  │   (Click để điều khiển)                         │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─────────────────────┐  ┌────────────────────────┐  │
│  │ Danh sách thiết bị  │  │   ⏰ Hẹn giờ          │  │
│  │ ─────────────────── │  │   ──────────────       │  │
│  │ 💡 Đèn trần        │  │   Thiết bị: [____]     │  │
│  │   [🔆 Bật][🌙 Tắt] │  │   Hành động: [____]    │  │
│  │   Độ sáng: [====] │  │   Sau: [__] phút       │  │
│  │                     │  │   [⏰ Đặt hẹn giờ]     │  │
│  │ 🌀 Quạt trần       │  │                         │  │
│  │   [🔆 Bật][🌙 Tắt] │  │   Timers đang chạy:    │  │
│  │   Tốc độ: ①②③     │  │   • Timer_001...       │  │
│  │                     │  │   [❌ Hủy timer]        │  │
│  │ 🚪 Cửa chính       │  │                         │  │
│  │   [Mở][Đóng][🔒]   │  │                         │  │
│  └─────────────────────┘  └────────────────────────┘  │
│                                                         │
│  Status: Tổng số thiết bị: 3 | Đang bật: 2            │
└────────────────────────────────────────────────────────┘
```

---

## ⚡ Tính năng nổi bật (v1.1)

### 1. 🖱️ Click để điều khiển
- Click vào thiết bị trong sơ đồ → Popup điều khiển nhanh
- Không cần cuộn danh sách thiết bị

### 2. ➕ Thêm thiết bị mới
```
Menu → Thiết bị → Thêm thiết bị
→ Chọn loại (💡/🌀/🚪) + Tên + Phòng
→ Click "Thêm"
```

### 3. 🏠 Quản lý phòng
```
Menu → Phòng → Chọn phòng
→ Xem chỉ thiết bị trong phòng đó
→ Hoặc "Tất cả phòng"
```

### 4. ⏰ Hẹn giờ thông minh
```
Panel bên phải → Chọn thiết bị
→ Chọn hành động + thời gian
→ Đặt hẹn giờ
```

---

## 🎮 Thử ngay (3 bước)

### Bước 1: Thêm thiết bị mới
1. Menu → Thiết bị → Thêm thiết bị
2. Chọn "💡 Đèn"
3. Tên: "Đèn học"
4. Phòng: Nhập "Phòng làm việc" (phòng mới)
5. Click "Thêm"

### Bước 2: Điều khiển bằng click
1. Nhìn sơ đồ phòng phía trên
2. Click vào icon 💡 "Đèn học"
3. Popup hiện ra → Click "🔆 Bật"
4. Điều chỉnh độ sáng bằng thanh trượt

### Bước 3: Đặt hẹn giờ
1. Panel "Hẹn giờ" bên phải
2. Thiết bị: Chọn "Đèn học"
3. Hành động: "turn_off"
4. Sau: 1 phút
5. Click "⏰ Đặt hẹn giờ"

➡️ Đèn sẽ tự động tắt sau 1 phút!

---

## 📚 Tài liệu chi tiết

- **USER_GUIDE.md**: Hướng dẫn sử dụng đầy đủ
- **CHANGELOG.md**: Lịch sử phát triển
- **DESIGN_PATTERNS.md**: Giải thích kiến trúc
- **README.md**: Tổng quan dự án

---

## 🐛 Troubleshooting

### Lỗi: "No module named 'tkinter'"
```bash
# Windows
pip install tk

# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS (đã có sẵn)
```

### Lỗi: Giao diện không hiển thị
- Kiểm tra Python version: `python --version` (cần 3.8+)
- Thử: `python3 main.py`

### Lỗi: Click vào thiết bị không hoạt động
- Đảm bảo đã click đúng vào icon (💡🌀🚪)
- Không click vào vùng trống

---

## 💡 Tips

### Sắp xếp thiết bị
- Đặt tên rõ ràng: "Đèn trần phòng khách" thay vì "Đèn 1"
- Gom thiết bị theo phòng để dễ quản lý

### Sử dụng hiệu quả
- **Điều khiển nhanh**: Click vào sơ đồ
- **Điều chỉnh chi tiết**: Dùng panel bên trái
- **Tự động hóa**: Đặt hẹn giờ cho các tác vụ lặp lại

### Tổ chức phòng
```
✅ Tốt:
Phòng khách → Đèn trần, Đèn tường, Quạt trần
Phòng ngủ → Đèn ngủ, Quạt đứng, Cửa phòng
Bếp → Đèn bếp, Quạt hút

❌ Tránh:
Phòng A → Tất cả thiết bị
```

---

## 🎯 Demo Console

Muốn test không dùng GUI?

```bash
# Demo tính năng cơ bản
python demo.py

# Demo tính năng mới (v1.1)
python demo_new_features.py
```

---

## 🆘 Cần trợ giúp?

1. **Trong ứng dụng**: Menu → ❓ Trợ giúp
2. **Đọc docs**: USER_GUIDE.md
3. **Xem ví dụ**: demo_new_features.py

---

## 📊 Project Info

- **Version**: 1.1.0
- **Language**: Python 3.8+
- **Dependencies**: Zero (chỉ dùng standard library)
- **Lines of code**: ~1200
- **GUI Framework**: Tkinter

---

**Chúc bạn sử dụng vui vẻ! 🎉**

> 💡 Pro tip: Nhấn `Ctrl+C` trong terminal để thoát ứng dụng
