#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File doc.py - Hướng dẫn sử dụng tool Copy Changed Files
"""


def get_help():
    """
    Trả về hướng dẫn sử dụng cơ bản của tool
    
    Returns:
        str: Hướng dẫn sử dụng tool
    """
    return """
📋 HƯỚNG DẪN SỬ DỤNG:

⚠️  YÊU CẦU: Dự án phải là Git repository

1️⃣  Nhập đường dẫn dự án (Git repository)

2️⃣  Nhập commit ID bắt đầu (ví dụ: 9d172f6)
   - Xem danh sách commit: git log --oneline -20

3️⃣  Nhập commit ID kết thúc (Enter để chọn HEAD - commit mới nhất)

4️⃣  Tool sẽ:
   - Lấy danh sách file đã thay đổi giữa 2 commit
   - Copy các file vào thư mục "changed-files-export"
   - Giữ nguyên cấu trúc thư mục gốc
   - Tạo file danh-sach-file-thay-doi.txt

💡 TIP:
   - Chỉ copy file đã thay đổi, không copy file đã xóa
   - Giữ nguyên cấu trúc thư mục để dễ upload lên server
   - Dùng để deploy code đã thay đổi mà không upload toàn bộ

📝 VÍ DỤ:
   Dự án: D:\\my-project
   Commit bắt đầu: 9d172f6
   Commit kết thúc: HEAD
   → Tìm thấy 25 file đã thay đổi
   → Copy vào: changed-files-export/
   → Có thể upload toàn bộ thư mục lên server bằng FileZilla
    """

