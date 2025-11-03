#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File doc.py - Hướng dẫn sử dụng tool QR Code
"""


def get_help():
    """
    Trả về hướng dẫn sử dụng cơ bản của tool
    
    Returns:
        str: Hướng dẫn sử dụng tool
    """
    return """
📋 HƯỚNG DẪN SỬ DỤNG:

⚠️  YÊU CẦU: 
   - Tạo QR code: pip install qrcode[pil]
   - Giải mã QR code: pip install opencv-python pyzbar pillow numpy

🔲 CHỨC NĂNG:

1️⃣  TẠO QR CODE (Chức năng 1):
   
   a) Nhập nội dung:
      - URL: https://example.com
      - Text: Hello World
      - Email: mailto:example@email.com
      - Số điện thoại: tel:+84123456789
      - WiFi: WIFI:T:WPA;S:NetworkName;P:Password;;
      - VCard, SMS, và nhiều format khác
   
   b) Đường dẫn lưu:
      - Enter: Lưu mặc định là qr_code.png
      - Nhập đường dẫn: Chỉ định file và thư mục
   
   c) Tùy chỉnh:
      - Kích thước box: Số lớn = QR code lớn hơn (mặc định: 10)
      - Border: Độ dày viền (mặc định: 4)
      - Mức sửa lỗi:
        * L: ~7% (thấp nhất, QR code nhỏ nhất)
        * M: ~15% (mặc định, cân bằng)
        * Q: ~25% (tốt cho logo)
        * H: ~30% (cao nhất, QR code lớn nhất)
      - Màu mã QR: black, #000000, hoặc tên màu khác
      - Màu nền: white, #FFFFFF, hoặc tên màu khác
      - Logo (tùy chọn): Chọn file ảnh logo, tỷ lệ 0.1-0.4

2️⃣  GIẢI MÃ QR CODE (Chức năng 2):
   
   a) Nhập đường dẫn thư mục chứa ảnh
   
   b) Tùy chọn:
      - Di chuyển ảnh thành công vào thư mục 'ok'?
   
   c) Kết quả:
      - File result.txt: Log chi tiết
      - File results.txt: Tổng kết
      - Tỷ lệ thành công/thất bại

💡 TIP TẠO QR CODE:
   - Mức sửa lỗi H (30%) tốt nhất khi có logo
   - Màu tối trên nền sáng dễ quét nhất
   - Kích thước box 10-15 phù hợp cho hầu hết trường hợp
   - Logo nên là hình vuông hoặc gần vuông
   - QR code có thể quét từ xa hơn nếu lớn hơn

💡 TIP GIẢI MÃ QR CODE:
   - Tool tự động xử lý nhiều kỹ thuật: enhance, crop, xoay
   - Hỗ trợ nhiều định dạng: jpg, png, bmp, tiff
   - Tự động thử nhiều phương pháp nếu lần đầu thất bại
   - Quét hàng loạt từ thư mục

📝 VÍ DỤ CLI:

   # Chế độ interactive
   python qr-code.py
   
   # Tạo QR code đơn giản
   python qr-code.py generate -d "https://example.com"
   
   # Tạo với tùy chỉnh
   python qr-code.py generate -d "Hello" -o output.png -s 15 -e H
   
   # Tạo có logo
   python qr-code.py generate -d "URL" -o qr.png --logo logo.png
   
   # Giải mã từ thư mục
   python qr-code.py decode --directory ./images
   
   # Giải mã không di chuyển file
   python qr-code.py decode -d ./images --no-move
    """

