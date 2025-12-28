# 📖 Hướng dẫn sử dụng Smart Home Controller

## 🚀 Khởi động ứng dụng

```bash
python main.py
```

Giao diện chính sẽ hiển thị với:
- **Sơ đồ phòng**: Hiển thị thiết bị trực quan ở phía trên
- **Danh sách thiết bị**: Panel điều khiển chi tiết bên trái
- **Hẹn giờ**: Panel quản lý timer bên phải
- **Menu bar**: Các chức năng quản lý

---

## 🎮 Điều khiển thiết bị

### Cách 1: Sử dụng Device Control Panel (bên trái)

Mỗi thiết bị có panel riêng với:
- **Nút Bật/Tắt**: 🔆 Bật hoặc 🌙 Tắt thiết bị
- **Controls đặc biệt**:
  - **Đèn** 💡: Thanh trượt điều chỉnh độ sáng (0-100%)
  - **Quạt** 🌀: Nút chọn tốc độ 1, 2, 3
  - **Cửa** 🚪: Nút Mở/Đóng và Khóa/Mở khóa

### Cách 2: Click trực tiếp vào thiết bị trong sơ đồ phòng

1. Di chuột qua icon thiết bị trong sơ đồ phòng
2. Icon sẽ được highlight (viền đậm hơn)
3. Click vào thiết bị
4. Popup điều khiển nhanh hiện ra với:
   - Trạng thái hiện tại (🟢 Đang bật / 🔴 Đang tắt)
   - Nút Bật/Tắt nhanh
   - Controls đặc biệt (độ sáng, tốc độ, khóa)

**Ưu điểm**: Điều khiển nhanh mà không cần cuộn danh sách thiết bị

---

## ➕ Thêm thiết bị mới

1. Click menu **⚙️ Thiết bị** > **➕ Thêm thiết bị**
2. Dialog hiện ra với các trường:
   - **Loại thiết bị**: Chọn 💡 Đèn, 🌀 Quạt, hoặc 🚪 Cửa
   - **Tên thiết bị**: Nhập tên (tự động gợi ý theo loại và phòng)
   - **Phòng**: Chọn phòng có sẵn hoặc click **+ Phòng mới**
3. Click **✅ Thêm**
4. Thiết bị mới xuất hiện trong danh sách và sơ đồ phòng

### Thêm phòng mới khi tạo thiết bị:
- Click nút **+ Phòng mới** trong dialog
- Nhập tên phòng (VD: "Phòng làm việc", "Ban công")
- Phòng mới tự động xuất hiện trong danh sách

---

## 🗑️ Xóa thiết bị

1. Click menu **⚙️ Thiết bị** > **🗑️ Xóa thiết bị**
2. Dialog hiển thị danh sách tất cả thiết bị
3. Click chọn thiết bị cần xóa
4. Click **🗑️ Xóa**
5. Xác nhận để xóa vĩnh viễn

**Lưu ý**: Các timer liên quan đến thiết bị cũng sẽ bị xóa

---

## 🏠 Quản lý phòng

### Lọc thiết bị theo phòng

1. Click menu **🏠 Phòng**
2. Chọn:
   - **🏠 Tất cả phòng**: Hiển thị toàn bộ thiết bị
   - **📍 [Tên phòng]**: Chỉ hiển thị thiết bị trong phòng đó
3. Danh sách và sơ đồ tự động cập nhật

### Xem sơ đồ phòng

- **Tất cả phòng**: Hiển thị tất cả thiết bị với layout tối ưu
- **Phòng cụ thể**: Chỉ hiển thị thiết bị trong phòng đó

**Màu sắc icon**:
- 💡 Đèn: Vàng (bật) / Xám (tắt)
- 🌀 Quạt: Xanh nhạt (bật) / Xám (tắt)
- 🚪 Cửa: Nâu (bật) / Xám (tắt)

---

## ⏰ Hẹn giờ tự động

### Đặt hẹn giờ mới

1. Vào panel **Hẹn giờ** (bên phải)
2. **Thiết bị**: Chọn thiết bị cần hẹn giờ
3. **Hành động**: Chọn `turn_on` hoặc `turn_off`
4. **Thời gian**: 
   - Nhập số (VD: 5)
   - Chọn đơn vị: `giây` hoặc `phút`
5. Click **⏰ Đặt hẹn giờ**

### Xem timer đang chạy

- Danh sách timer hiển thị:
  ```
  Timer_001 | Đèn phòng khách | turn_on | 2024-XX-XX XX:XX:XX
  ```
- Các timer được sắp xếp theo thời gian thực thi

### Hủy timer

1. Click chọn timer trong danh sách
2. Click **❌ Hủy timer**
3. Timer bị xóa và không thực thi

---

## 🔄 Làm mới giao diện

Click menu **⚙️ Thiết bị** > **🔄 Làm mới** để:
- Cập nhật danh sách thiết bị
- Refresh sơ đồ phòng
- Đồng bộ tất cả trạng thái

---

## 💡 Mẹo sử dụng

### 1. Tổ chức thiết bị theo phòng
Đặt tên thiết bị rõ ràng theo phòng:
```
✅ Tốt: "Đèn trần phòng khách", "Quạt phòng ngủ"
❌ Tránh: "Đèn 1", "Quạt A"
```

### 2. Sử dụng click interaction cho điều khiển nhanh
- Bật/tắt nhanh → Click vào icon trong sơ đồ
- Điều chỉnh chi tiết → Dùng panel bên trái

### 3. Đặt hẹn giờ thông minh
```
Buổi sáng: Bật đèn sau 5 giây để test
Buổi tối: Tắt quạt sau 30 phút
```

### 4. Lọc phòng khi cần tập trung
- Đang ở phòng ngủ → Lọc theo "Phòng ngủ"
- Chỉ xem và điều khiển thiết bị liên quan

---

## ❓ Trợ giúp

### Trong ứng dụng
Click menu **❓ Trợ giúp**:
- **📖 Hướng dẫn**: Hướng dẫn ngắn gọn
- **ℹ️ Về chương trình**: Thông tin phiên bản

### Kiểm tra lỗi
Nếu thiết bị không hoạt động:
1. Kiểm tra trạng thái trong panel
2. Thử bật/tắt lại
3. Làm mới giao diện (Ctrl+R hoặc menu Làm mới)

---

## 🎯 Workflow đề xuất

### Khi khởi động lần đầu:
1. ✅ Thêm các phòng (Phòng khách, Phòng ngủ, Bếp...)
2. ✅ Thêm thiết bị cho từng phòng
3. ✅ Kiểm tra sơ đồ phòng
4. ✅ Test điều khiển bằng click

### Sử dụng hàng ngày:
1. 🏠 Chọn phòng cần điều khiển
2. 🖱️ Click vào thiết bị trong sơ đồ để bật/tắt nhanh
3. ⏰ Đặt hẹn giờ cho các tác vụ tự động
4. 🔄 Làm mới nếu cần

---

## 🎨 Phím tắt (đề xuất cho tương lai)

```
Ctrl+N: Thêm thiết bị mới
Ctrl+D: Xóa thiết bị
Ctrl+R: Làm mới
Ctrl+T: Đặt hẹn giờ
Ctrl+1-9: Chuyển phòng
```

---

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra file `main.py` có chạy đúng không
2. Xem console output để debug
3. Đọc file `DESIGN_PATTERNS.md` để hiểu kiến trúc

---

**Chúc bạn sử dụng vui vẻ! 🎉**
