#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File doc.py - Hướng dẫn sử dụng tool Image Watermark
"""


def get_help():
    """
    Trả về hướng dẫn sử dụng cơ bản của tool
    
    Returns:
        str: Hướng dẫn sử dụng tool
    """
    return """
📋 HƯỚNG DẪN SỬ DỤNG:

⚠️  YÊU CẦU: Cài đặt Pillow trước khi sử dụng (pip install Pillow)

1️⃣  Chọn chế độ watermark:
   - 1: Text Watermark (chữ)
   - 2: Image Watermark (logo)
   - 3: Dùng Template đã lưu

2️⃣  Text Watermark:
   - Nhập text watermark (vd: © 2024 Your Name)
   - Kích thước chữ (pixels, mặc định: 36)
   - Màu chữ (white/black, mặc định: white)

3️⃣  Image Watermark:
   - Nhập đường dẫn logo/watermark (PNG trong suốt)
   - Kích thước logo (% chiều rộng ảnh, mặc định: 10%)

4️⃣  Cấu hình chung:
   - Vị trí watermark (9 vị trí: top-left, center, bottom-right...)
   - Độ trong suốt (0-255, 0=trong suốt, 255=đặc, mặc định: 128)

5️⃣  Thư mục ảnh:
   - Thư mục chứa ảnh gốc
   - Thư mục output (Enter để tạo 'watermarked' với timestamp)

6️⃣  Xem và xác nhận config

7️⃣  Lưu config thành template? (y/N) - Để tái sử dụng sau

8️⃣  Xử lý hàng loạt và xem kết quả

💡 TIP:
   - Logo nên là PNG trong suốt
   - Opacity càng cao watermark càng rõ
   - Có thể lưu template để dùng lại
   - Hỗ trợ nhiều format: JPG, PNG, WEBP, BMP

📝 VÍ DỤ:
   Chế độ: Text Watermark
   Text: © 2024 My Company
   Vị trí: bottom-right
   Opacity: 128
   Thư mục: D:\\Photos
   → Xử lý 50 ảnh
   → Thành công: 50/50
   → Lưu vào: D:\\Photos\\watermarked_20241029_153045\\
    """

