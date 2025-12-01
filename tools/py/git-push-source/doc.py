#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File doc.py - Hướng dẫn sử dụng tool Git Push Source
"""


def get_help():
    """
    Trả về hướng dẫn sử dụng cơ bản của tool
    
    Returns:
        str: Hướng dẫn sử dụng tool
    """
    return """
📋 HƯỚNG DẪN SỬ DỤNG:

1️⃣  CHUẨN BỊ:
   - Đảm bảo Git đã được cài đặt
   - Có quyền truy cập repository (Personal Access Token hoặc SSH key)

2️⃣  NHẬP THÔNG TIN:
   - Repository URL: URL của repository (mặc định: https://github.com/VHN-DEV/laravel-botble-cms)
   - Local path: Đường dẫn thư mục local chứa source code

3️⃣  CÁC CHỨC NĂNG:

   📥 Clone repository (1):
      - Clone repository từ remote về local
      - Sử dụng khi chưa có code ở local

   📦 Khởi tạo repository (2):
      - Khởi tạo Git repository mới trong thư mục local
      - Tự động thiết lập remote

   🔗 Thiết lập remote (3):
      - Thêm hoặc cập nhật remote repository
      - Mặc định: origin

   📊 Xem trạng thái (4):
      - Hiển thị files đã thay đổi
      - Hiển thị branch hiện tại

   📝 Add files và commit (5):
      - Thêm files vào staging area
      - Commit với message

   🚀 Push code (6):
      - Push code lên remote repository
      - Hỗ trợ force push (cẩn thận!)

   🌿 Tạo branch mới (7):
      - Tạo và chuyển sang branch mới

   ⚡ Thực hiện đầy đủ (8):
      - Tự động: Add → Commit → Push
      - Nhanh chóng và tiện lợi nhất

4️⃣  QUY TRÌNH ĐẦY ĐỦ:

   Bước 1: Clone hoặc khởi tạo repository
   Bước 2: Chỉnh sửa code
   Bước 3: Chọn chức năng 8 (Thực hiện đầy đủ)
   Bước 4: Nhập commit message
   Bước 5: Xác nhận push

💡 TIP:
   - Sử dụng chức năng 8 để thao tác nhanh nhất
   - Kiểm tra trạng thái trước khi commit
   - Commit message nên rõ ràng, mô tả thay đổi
   - Không nên force push lên main/master branch
   - Sử dụng branch riêng cho các tính năng mới

📝 VÍ DỤ:
   Repository: https://github.com/VHN-DEV/laravel-botble-cms
   Local path: D:\\projects\\laravel-botble-cms
   Chức năng: 8 (Thực hiện đầy đủ)
   Commit message: "Update authentication feature"
   Branch: main
   → Add files → Commit → Push thành công!

⚠️  LƯU Ý:
   - Cần có quyền write vào repository
   - Kiểm tra kỹ files trước khi commit
   - Backup code quan trọng trước khi push
   - Không commit files nhạy cảm (.env, keys, passwords)
    """

