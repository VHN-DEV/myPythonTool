#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File doc.py - Hướng dẫn sử dụng tool Text Encoding Converter
"""


def get_help():
    """
    Trả về hướng dẫn sử dụng cơ bản của tool
    
    Returns:
        str: Hướng dẫn sử dụng tool
    """
    return """
📋 HƯỚNG DẪN SỬ DỤNG:

⚠️  YÊU CẦU: Cài đặt chardet trước khi sử dụng (pip install chardet)

1️⃣  Nhập đường dẫn thư mục chứa file text

2️⃣  Chỉ xử lý file có đuôi (.txt .py .js - Enter để tất cả)

3️⃣  Xử lý tất cả thư mục con? (Y/n)

4️⃣  Chọn chế độ:
   - 1: Phát hiện encoding (không thay đổi file)
   - 2: Chuyển đổi encoding

5️⃣  Chế độ 2 (Chuyển đổi):
   - Encoding nguồn:
     * Nhập encoding (utf-8, windows-1252, iso-8859-1...)
     * Hoặc nhập 'auto' để tự động phát hiện
   - Encoding đích (vd: utf-8, utf-16, windows-1252...)
   - Tạo backup file gốc (.bak)? (Y/n)

6️⃣  Xác nhận (phải gõ YES để xác nhận)

7️⃣  Xem kết quả: số file đã chuyển đổi, bỏ qua, lỗi

💡 TIP:
   - Dùng 'auto' để tự phát hiện encoding
   - Nên tạo backup trước khi chuyển đổi
   - UTF-8 là encoding khuyên dùng
   - Windows-1252 dùng cho file Windows Western

📝 VÍ DỤ:
   Thư mục: D:\\Documents
   Loại file: .txt .csv
   Encoding nguồn: auto (tự phát hiện)
   Encoding đích: utf-8
   Backup: Có
   → Phát hiện: 20 file windows-1252, 5 file iso-8859-1
   → Chuyển đổi thành công: 25 file
   → Tạo backup: 25 file .bak
    """

