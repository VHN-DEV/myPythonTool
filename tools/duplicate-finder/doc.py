#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File doc.py - Hướng dẫn sử dụng tool Duplicate Finder
"""


def get_help():
    """
    Trả về hướng dẫn sử dụng cơ bản của tool
    
    Returns:
        str: Hướng dẫn sử dụng tool
    """
    return """
📋 HƯỚNG DẪN SỬ DỤNG:

1️⃣  Nhập đường dẫn thư mục cần quét

2️⃣  Chọn tùy chọn:
   - Tìm trong tất cả thư mục con? (Y/n)
   - Kích thước file tối thiểu (KB, Enter để bỏ qua)

3️⃣  Chọn phương pháp tìm:
   - 1: Theo hash MD5 - Chính xác nhưng chậm
   - 2: Theo hash SHA256 - Chính xác hơn MD5
   - 3: Theo kích thước - Nhanh nhưng không chính xác 100%

4️⃣  Chọn sử dụng multiprocessing? (Y/n) - Tăng tốc với file nhiều

5️⃣  Xem kết quả:
   - Hiển thị các nhóm file trùng lặp
   - Tính toán dung lượng lãng phí

6️⃣  Lưu báo cáo? (y/N) - Xuất ra file duplicate_report.txt

7️⃣  Xóa file trùng lặp? (y/N):
   - Chọn cách xóa: Giữ file đầu tiên/mới nhất/cũ nhất
   - Xác nhận trước khi xóa

💡 TIP:
   - Dùng MD5/SHA256 cho kết quả chính xác
   - Dùng size-only cho quick scan nhanh
   - Multiprocessing giúp tăng tốc với nhiều file lớn
   - Xem preview trước khi xóa để tránh xóa nhầm

📝 VÍ DỤ:
   Thư mục: D:\\Photos
   Phương pháp: MD5 (hash)
   → Tìm thấy 5 nhóm file trùng lặp
   → Lãng phí: 450 MB
   → Chọn giữ file mới nhất, xóa các file cũ hơn
    """

