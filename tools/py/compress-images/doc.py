#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File doc.py - Hướng dẫn sử dụng tool Compress Images
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

1️⃣  Nhập đường dẫn thư mục chứa ảnh

2️⃣  Chọn chức năng:
   - 1: Nén ảnh (giảm dung lượng)
   - 2: Resize ảnh (thay đổi kích thước)
   - 3: Đổi format ảnh (.jpg → .png...)
   - 4: Nén + Resize kết hợp

3️⃣  Chức năng 1 (Nén):
   - Chất lượng nén (1-100, mặc định: 85)
   - Dung lượng tối đa (KB, Enter để bỏ qua)
   - Format đích (Enter để giữ nguyên format)

4️⃣  Chức năng 2 (Resize):
   - Nhập width (pixels) hoặc % (vd: 1920 hoặc 50%)
   - Nhập height (pixels) hoặc Enter để giữ tỷ lệ
   - Format đích (Enter để giữ nguyên)

5️⃣  Chức năng 3 (Đổi format):
   - Format đích: jpg, png, webp...
   - Chất lượng nén (nếu áp dụng)

6️⃣  Chức năng 4 (Nén + Resize):
   - Kích thước mới (width x height hoặc %)
   - Chất lượng nén (1-100)
   - Format đích

7️⃣  Chọn vị trí lưu file đã xử lý:
   - Enter: Tạo thư mục mới với timestamp
   - Nhập đường dẫn: Chỉ định thư mục

8️⃣  Chọn giữ file gốc hoặc thay thế

9️⃣  Chọn sử dụng multiprocessing? (Y/n) - Tăng tốc

💡 TIP:
   - Chất lượng 85 là cân bằng tốt
   - Resize theo % để giữ tỷ lệ
   - WEBP có tỷ lệ nén tốt nhất
   - Multiprocessing giúp xử lý nhanh với nhiều ảnh

📝 VÍ DỤ:
   Thư mục: D:\\Photos
   Chức năng: 4 (Nén + Resize)
   Kích thước: 1920 (width)
   Chất lượng: 85
   Format: jpg
   → Ảnh 5000x3000, 5MB → 1920x1152, 450KB (giảm 91%)
    """

