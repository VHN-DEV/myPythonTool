#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File doc.py - Hướng dẫn sử dụng tool Rename Files
"""


def get_help():
    """
    Trả về hướng dẫn sử dụng cơ bản của tool
    
    Returns:
        str: Hướng dẫn sử dụng tool
    """
    return """
📋 HƯỚNG DẪN SỬ DỤNG:

1️⃣  Nhập đường dẫn thư mục chứa file cần đổi tên

2️⃣  Chọn chức năng:
   - 1: Thêm prefix (tiền tố)
   - 2: Thêm suffix (hậu tố)
   - 3: Thay thế text trong tên file
   - 4: Đổi tên theo số thứ tự (001, 002...)
   - 5: Đổi phần mở rộng (.jpg → .png)
   - 6: Chuyển sang chữ thường
   - 7: Xóa/thay thế khoảng trắng

3️⃣  Nhập thông tin cần thiết (prefix, suffix, text...)

4️⃣  Chọn file extension cần xử lý (.jpg .png - Enter để tất cả)

💡 TIP:
   - Có thể giới hạn chỉ xử lý file có extension nhất định
   - Xem preview trước khi xác nhận
   - Hỗ trợ đổi tên hàng loạt nhanh chóng

📝 VÍ DỤ:
   Thư mục: D:\\Wedding_Photos
   Chức năng: 4 (Đổi tên theo số thứ tự)
   Tên cơ sở: wedding
   → DSC_5423.jpg → wedding_001.jpg
   → DSC_5424.jpg → wedding_002.jpg
    """

