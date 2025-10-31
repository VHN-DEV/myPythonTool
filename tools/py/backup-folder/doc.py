#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File doc.py - Hướng dẫn sử dụng tool Backup Folder
"""


def get_help():
    """
    Trả về hướng dẫn sử dụng cơ bản của tool
    
    Returns:
        str: Hướng dẫn sử dụng tool
    """
    return """
📋 HƯỚNG DẪN SỬ DỤNG:

1️⃣  Nhập đường dẫn thư mục cần backup

2️⃣  Chọn vị trí lưu backup:
   - Enter: Lưu tại thư mục hiện tại
   - Nhập đường dẫn: Chỉ định thư mục lưu

3️⃣  Chọn định dạng nén:
   - ZIP: Phổ biến, tương thích tốt
   - TAR.GZ: Linux/Unix, tỷ lệ nén cao
   - TAR.BZ2: Nén tốt nhất, chậm hơn

4️⃣  Chọn chế độ backup:
   - 1: Backup toàn bộ (không loại trừ)
   - 2: Backup có loại trừ (exclude patterns)

5️⃣  Nếu chọn chế độ 2:
   - Nhập các pattern loại trừ (cách nhau bởi dấu phẩy)
   - Ví dụ: node_modules,.git,__pycache__,dist,build

6️⃣  Xem kết quả:
   - Dung lượng gốc và dung lượng nén
   - Tỷ lệ nén (%)
   - Đường dẫn file backup

💡 TIP:
   - File backup tự động có timestamp: folder_backup_YYYYMMDD_HHMMSS.ext
   - Loại trừ các thư mục không cần để giảm dung lượng
   - Xem lịch sử backup trong file backup_metadata.json
   - Tự động lưu metadata để tracking

📝 VÍ DỤ:
   Thư mục: D:\\my-project
   Định dạng: ZIP
   Chế độ: 2 (có loại trừ)
   Loại trừ: node_modules,.git,__pycache__
   → Backup thành công!
   → File: D:\\Backups\\my-project_backup_20241029_153045.zip
   → Kích thước: 45.20 MB (từ 120 MB - nén 62.3%)
    """

