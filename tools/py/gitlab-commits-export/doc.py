#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File doc.py - Hướng dẫn sử dụng tool GitLab Commits Export
"""


def get_help():
    """
    Trả về hướng dẫn sử dụng cơ bản của tool
    
    Returns:
        str: Hướng dẫn sử dụng tool
    """
    return """
📋 HƯỚNG DẪN SỬ DỤNG:

⚠️  YÊU CẦU: 
   - Phải chạy trong thư mục Git repository
   - Cài đặt: pip install openpyxl

1️⃣  Chạy tool trong thư mục Git repository

2️⃣  Tool sẽ yêu cầu:
   - Khoảng thời gian (since/until)
   - Tác giả (optional)
   - Branch cần export (optional)
   - Từ khóa trong commit message (optional)
   - Có bao gồm commit trong giờ làm việc không

3️⃣  Tool sẽ:
   - Lấy danh sách commits từ Git
   - Phân loại commit tăng ca (ngoài 8:00-17:30)
   - Export ra file Excel với định dạng đẹp
   - Hiển thị thống kê trên console

4️⃣  File Excel chứa:
   - Tác giả, Ngày, Thời gian
   - Mã commit, Event (merge/commit), Type
   - Branch, Nội dung commit
   - OP Link (nếu có {OP#1234} trong message)
   - Child commits (nếu là merge commit)

💡 TIP:
   - Giờ làm việc mặc định: 8:00 - 17:30
   - Commit ngoài giờ này được tính là tăng ca
   - Hỗ trợ filter theo branch và keyword

📝 VÍ DỤ:
   Thư mục: ./my-project (Git repo)
   Từ ngày: 2025-01-01
   Đến ngày: 2025-01-31
   Branch: develop
   → Xuất file: commits_20250131.xlsx
   → Hiển thị: 45 commits tăng ca, 120 commits trong giờ
    """

