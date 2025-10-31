#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File doc.py - Hướng dẫn sử dụng tool Generate Tree
"""


def get_help():
    """
    Trả về hướng dẫn sử dụng cơ bản của tool
    
    Returns:
        str: Hướng dẫn sử dụng tool
    """
    return """
📋 HƯỚNG DẪN SỬ DỤNG:

1️⃣  Nhập đường dẫn thư mục (Enter để dùng thư mục hiện tại)

2️⃣  Nhập các thư mục/file cần bỏ qua:
   - Mặc định: node_modules, .git, __pycache__, .vscode, .idea...
   - Hoặc nhập danh sách riêng (cách nhau bởi dấu phẩy)

3️⃣  Nhập độ sâu tối đa:
   - Enter: Không giới hạn
   - Hoặc nhập số (ví dụ: 3 - chỉ hiển thị 3 cấp)

4️⃣  Hiển thị file/folder ẩn (bắt đầu bằng .)? (y/N)

5️⃣  Xem kết quả:
   - Hiển thị cây thư mục với icon đẹp
   - Thống kê số thư mục và file

6️⃣  Lưu kết quả ra file? (Y/n)
   - Tạo file: tree_[tên-thư-mục].txt

💡 TIP:
   - Dùng để tạo documentation cho dự án
   - Bỏ qua các thư mục không cần thiết (node_modules...)
   - Icon tự động theo loại file (.py, .js, .jpg...)
   - Hỗ trợ hiển thị file ẩn nếu cần

📝 VÍ DỤ:
   Thư mục: D:\\my-project
   Bỏ qua: node_modules, .git, __pycache__
   Độ sâu: Không giới hạn
   → Tạo cây thư mục đẹp với icon
   → Tổng: 150 thư mục, 1200 file
   → Lưu vào: tree_my-project.txt
    """

