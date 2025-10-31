#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File doc.py - Hướng dẫn sử dụng tool SSH Manager
"""


def get_help():
    """
    Trả về hướng dẫn sử dụng cơ bản của tool
    
    Returns:
        str: Hướng dẫn sử dụng tool
    """
    return """
📋 HƯỚNG DẪN SỬ DỤNG:

1️⃣  Thêm server mới: Nhập 'a' (add)
   - Nhập tên server
   - Nhập host/IP
   - Nhập username
   - Nhập port (mặc định: 22)
   - Nhập SSH key (Enter để dùng default hoặc bỏ qua)
   
2️⃣  Kết nối server: Chọn số thứ tự từ danh sách

3️⃣  Quản lý server:
   - 'e' (edit): Sửa thông tin server
   - 'd' (delete): Xóa server
   - 'v' (view): Xem file config JSON
   - 'q' (quit): Thoát

💡 TIP:
   - Config được lưu trong: ssh_config.json
   - Có thể dùng SSH key hoặc password
   - Hỗ trợ nhiều server, dễ quản lý

📝 VÍ DỤ:
   Server: myserver
   Host: 192.168.1.100
   Username: root
   Port: 22
   → Kết nối tự động: ssh root@192.168.1.100 -p 22
    """

