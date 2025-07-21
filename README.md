# Snake Game 2 Người

Game rắn săn mồi hai người chơi trên cùng màn hình với đồ họa PyGame!

## Tính Năng

### 🎮 Chơi Game Cơ Bản

- **2 Người Chơi**: Mỗi người điều khiển rắn riêng trên cùng bàn cờ
- **Đặt Tên Player**: Nhập tên cho cả hai người chơi trước khi bắt đầu
- **Điều Khiển Riêng Biệt**:
  - Player 1 (Rắn Xanh): Phím mũi tên
  - Player 2 (Rắn Xanh Dương): Phím WASD
- **Hệ Thống Điểm**: Ăn thức ăn +10 điểm, power-up +5 điểm
- **Thắng/Thua**: Rắn sống sót lâu nhất hoặc có điểm cao nhất thắng
- **Ghi Tỷ Số**: Theo dõi số ván thắng của mỗi người chơi, thắng ván +1

### ✨ Tính Năng Nâng Cao

- **Xuyên Tường**: Chạm tường sẽ xuất hiện ở phía đối diện (không chết)
- **Power-ups**: Ba loại vật phẩm đặc biệt:
  - 🟦 **Speed Boost** (Xanh dương): Tăng tốc độ 3 giây
  - 🟣 **Grow** (Tím): Tăng 2 đốt ngay lập tức
  - 🟠 **Shrink Enemy** (Cam): Giảm 2 đốt của đối thủ
- **Chướng Ngại Vật**: Khối xám ngẫu nhiên tạo thử thách
- **Hiệu Ứng Tốc Độ**: Rắn phát sáng khi có speed boost

## Cài Đặt

1. **Cài Python** (3.7 trở lên)
2. **Cài PyGame**:
   ```bash
   pip install -r requirements.txt
   ```
   Hoặc thủ công:
   ```bash
   pip install pygame==2.5.2
   ```

## Chạy Game

```bash
python snake_game.py
```

## Điều Khiển

### Player 1 (Rắn Xanh)

- **↑**: Di chuyển lên
- **↓**: Di chuyển xuống
- **←**: Di chuyển trái
- **→**: Di chuyển phải

### Player 2 (Rắn Xanh Dương)

- **W**: Di chuyển lên
- **S**: Di chuyển xuống
- **A**: Di chuyển trái
- **D**: Di chuyển phải

### Điều Khiển Chung

- **R**: Chơi lại (khi game over)
- **N**: Sửa tên player (khi game over)
- **C**: Reset tỷ số thắng/thua (bất cứ lúc nào)
- **Q**: Thoát game

### Điều Khiển Nhập Tên

- **Enter**: Xác nhận tên hiện tại
- **Tab**: Chuyển sang player tiếp theo
- **Space**: Bắt đầu game với tên hiện tại
- **C**: Reset tỷ số thắng/thua
- **Backspace**: Xóa ký tự
- **ESC**: Bắt đầu với tên mặc định / Quay lại

## Cách Chơi

1. **Nhập Tên**: Đặt tên cho cả hai player trước khi bắt đầu
2. **Mục Tiêu**: Sống sót lâu hơn đối thủ và ghi nhiều điểm
3. **Ăn Thức Ăn**: Ô đỏ cho 10 điểm và làm rắn lớn lên
4. **Nhặt Power-ups**: Các ô màu cho lợi thế tạm thời:
   - Xanh dương = Tăng tốc 3 giây
   - Tím = Tăng 2 đốt ngay
   - Cam = Giảm 2 đốt của đối thủ
5. **Tránh Va Chạm**: Không đâm vào chướng ngại vật, chính mình, hoặc đối thủ
6. **Điều Kiện Thắng**:
   - Rắn sống sót cuối cùng thắng
   - Nếu cả hai chết cùng lúc, điểm cao hơn thắng
   - Hòa nếu cùng điểm khi cả hai chết
7. **Tỷ Số Tổng**: Mỗi ván thắng tích lũy +1 win, hiển thị trên màn hình

## Cơ Chế Game

### Hệ Thống Va Chạm

- **Xuyên Tường**: Chạm rìa màn hình → xuất hiện phía đối diện (không chết)
- **Tự Đâm**: Đâm vào thân mình → chết
- **Đâm Nhau**: Đâm vào thân đối thủ → chết
- **Đầu-Đầu**: Hai đầu va nhau → cả hai chết
- **Chướng Ngại Vật**: Đâm vào khối xám → chết

### Hệ Thống Điểm

- **Thức Ăn**: 10 điểm mỗi ô đỏ (điểm trong ván)
- **Power-ups**: 5 điểm bonus mỗi vật phẩm (điểm trong ván)
- **Thưởng Sống Sót**: Là rắn cuối cùng sống sót thường quyết định thắng thua

### Hệ Thống Tỷ Số

- **Thắng Ván**: +1 win cho người thắng (hiển thị tích lũy)
- **Hòa**: Không ai được cộng win
- **Reset**: Có thể reset tỷ số về 0-0 bằng phím C

### Hiệu Ứng Power-up

- **Speed Boost**: Tăng đôi tốc độ trong 3 giây (hiệu ứng phát sáng)
- **Grow**: Tăng ngay 2 đốt thân
- **Shrink Enemy**: Giảm tối đa 2 đốt của đối thủ (không giết chết)

## Chiến Thuật

1. **Kiểm Soát Trung Tâm**: Vị trí giữa có nhiều lối thoát hơn
2. **Sử Dụng Power-ups Khôn Ngoan**: Speed boost giúp thoát khỏi tình huống nguy hiểm
3. **Chặn Đường Đối Thủ**: Dùng thân mình để hạn chế di chuyển của đối thủ
4. **Tránh Va Chạm Trực Diện**: Không lao vào nhau trực tiếp
5. **Khai Thác Xuyên Tường**: Sử dụng tính năng wrap-around để tấn công bất ngờ

## Chi Tiết Kỹ Thuật

- **Giao Diện Tương Tác**: Màn hình nhập tên với text input thực tế
- **Quản Lý Trạng Thái**: Chuyển đổi giữa name input, playing, game over
- **Di Chuyển Lưới**: Hệ thống lưới 20x20 pixel
- **Hoạt Hình Mượt**: 60 FPS
- **Sinh Ngẫu Nhiên**: Chướng ngại vật và power-up xuất hiện ngẫu nhiên
- **Điều Khiển Thời Gian Thực**: Xử lý input liên tục
- **Tối Ưu Va Chạm**: Kiểm tra va chạm dựa trên vị trí hiệu quả

## Tùy Chỉnh

Có thể chỉnh sửa các hằng số trong `snake_game.py`:

- `WINDOW_WIDTH/HEIGHT`: Thay đổi kích thước bàn cờ
- `GRID_SIZE`: Điều chỉnh độ chi tiết di chuyển
- `base_speed`: Sửa tốc độ rắn cơ bản (số nhỏ hơn = nhanh hơn)
- `powerup_spawn_interval`: Kiểm soát tần suất power-up
- Màu sắc và hiệu ứng có thể tùy chỉnh trong phần color constants

Chúc bạn chơi vui vẻ! 🐍🎮
