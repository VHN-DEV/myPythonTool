#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File doc.py - Hướng dẫn sử dụng tool File Organizer
"""


def get_help():
    """
    Trả về hướng dẫn sử dụng cơ bản của tool
    
    Returns:
        str: Hướng dẫn sử dụng tool
    """
    return """
📋 HƯỚNG DẪN SỬ DỤNG:

1️⃣  Nhập đường dẫn thư mục cần sắp xếp

2️⃣  Chọn chế độ sắp xếp:
   - 1: Theo loại file (Images, Videos, Documents, Code...)
   - 2: Theo đuôi file (.jpg, .mp4, .pdf...)
   - 3: Theo ngày tháng (modification date)

3️⃣  Chọn định dạng ngày (nếu chọn chế độ 3):
   - 1: Năm-Tháng (2024-01)
   - 2: Năm-Tháng-Ngày (2024-01-15)
   - 3: Chỉ năm (2024)

4️⃣  Chọn thư mục đích:
   - Enter: Tạo thư mục "Organized" trong thư mục nguồn
   - Nhập đường dẫn: Chỉ định thư mục đích

5️⃣  Chọn hành động:
   - 1: Copy (giữ nguyên file gốc)
   - 2: Move (di chuyển file)

6️⃣  Xác nhận (nếu chọn Move)

💡 TIP:
   - Copy an toàn hơn Move (giữ nguyên file gốc)
   - Move sẽ di chuyển file khỏi vị trí gốc
   - Tự động xử lý trùng tên (thêm số thứ tự)
   - Hiển thị thống kê sau khi hoàn thành

📝 VÍ DỤ:
   Thư mục: D:\\Downloads
   Chế độ: 1 (Theo loại file)
   Hành động: Copy
   → Images/ (45 file)
   → Videos/ (12 file)
   → Documents/ (30 file)
   → Code/ (25 file)
   → ...
    """

