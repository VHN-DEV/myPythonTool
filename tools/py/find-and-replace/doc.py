#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File doc.py - Hướng dẫn sử dụng tool Find and Replace
"""


def get_help():
    """
    Trả về hướng dẫn sử dụng cơ bản của tool
    
    Returns:
        str: Hướng dẫn sử dụng tool
    """
    return """
📋 HƯỚNG DẪN SỬ DỤNG:

1️⃣  Nhập đường dẫn thư mục chứa file cần tìm/thay thế

2️⃣  Chọn chức năng:
   - 1: Tìm text trong file (hiển thị kết quả)
   - 2: Thay thế text trong file

3️⃣  Nhập thông tin:
   - Text cần tìm
   - Text thay thế (nếu chọn chức năng 2)
   - Loại file cần xử lý (.py .txt .md... - Enter để tất cả)

4️⃣  Chọn tùy chọn:
   - Case sensitive (phân biệt hoa thường): y/n
   - Sử dụng regex: y/n

💡 TIP:
   - Xem kết quả tìm thấy trước khi thay thế
   - Hỗ trợ regex pattern (ví dụ: \d+ tìm số)
   - Hiển thị số dòng và nội dung tìm thấy

📝 VÍ DỤ:
   Thư mục: D:\\my-project\\src
   Tìm: "old_function"
   Thay thế: "new_function"
   Loại file: .py
   → Tìm thấy 15 file, 25 lần xuất hiện
   → Đã thay thế thành công
    """

