#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File doc.py - Hướng dẫn sử dụng tool Clean Temp Files
"""


def get_help():
    """
    Trả về hướng dẫn sử dụng cơ bản của tool
    
    Returns:
        str: Hướng dẫn sử dụng tool
    """
    return """
📋 HƯỚNG DẪN SỬ DỤNG:

1️⃣  Nhập đường dẫn thư mục cần dọn dẹp

2️⃣  Chọn chức năng:
   - 1: Tìm và xóa file tạm (.tmp, .temp, .log, .bak...)
   - 2: Tìm và xóa thư mục cache (__pycache__, node_modules...)
   - 3: Dọn dẹp toàn bộ (file tạm + cache)

3️⃣  Xem danh sách file/folder sẽ xóa

4️⃣  Xác nhận trước khi xóa (y/n)

💡 TIP:
   - Tự động tính toán dung lượng sẽ giải phóng
   - Hiển thị danh sách trước khi xóa
   - Cẩn thận khi xóa cache (có thể cần rebuild)

📝 VÍ DỤ:
   Thư mục: D:\\my-project
   Chức năng: 3 (Dọn dẹp toàn bộ)
   → Tìm thấy 50 file tạm (2.5 MB)
   → Tìm thấy 10 thư mục cache (150 MB)
   → Tổng giải phóng: 152.5 MB
    """

