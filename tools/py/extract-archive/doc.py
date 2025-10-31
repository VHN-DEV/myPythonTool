#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File doc.py - Hướng dẫn sử dụng tool Extract Archive
"""


def get_help():
    """
    Trả về hướng dẫn sử dụng cơ bản của tool
    
    Returns:
        str: Hướng dẫn sử dụng tool
    """
    return """
📋 HƯỚNG DẪN SỬ DỤNG:

⚠️  LƯU Ý: File .7z cần py7zr, file .rar cần rarfile + WinRAR/unrar

1️⃣  Chọn chế độ:
   - 1: Giải nén 1 file
   - 2: Giải nén tất cả file trong thư mục

2️⃣  Chế độ 1 (Giải nén 1 file):
   - Nhập đường dẫn file nén
   - Nhập thư mục đích (Enter để dùng tên file)
   - Tự động phát hiện format: ZIP, TAR, TAR.GZ, TAR.BZ2, 7Z, RAR

3️⃣  Chế độ 2 (Giải nén hàng loạt):
   - Nhập đường dẫn thư mục chứa file nén
   - Xem danh sách file tìm thấy
   - Nhập thư mục đích chung (Enter để dùng thư mục hiện tại)
   - Xác nhận và giải nén

💡 TIP:
   - Hỗ trợ nhiều format: ZIP, TAR, TAR.GZ, TAR.BZ2, 7Z, RAR
   - Tự động tạo thư mục đích nếu chưa có
   - Hiển thị kích thước trước/sau giải nén
   - Mỗi file giải nén vào thư mục riêng (theo tên file)

📝 VÍ DỤ:
   Chế độ: 2 (Giải nén hàng loạt)
   Thư mục: D:\\Downloads\\archives
   → Tìm thấy 10 file nén
   → Giải nén vào: D:\\Downloads\\archives\\extracted\\
   → Mỗi file có thư mục riêng
    """

