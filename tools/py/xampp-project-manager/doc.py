#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module doc - Hướng dẫn sử dụng tool xampp-project-manager
"""

HELP_TEXT = """
============================================================
   HUONG DAN SU DUNG: QUAN LY VA CAI DAT DU AN (WINDOWS)
============================================================

📖 MỤC ĐÍCH:

Tool quản lý và cài đặt dự án trên XAMPP Windows, bao gồm:
- Quản lý dự án trong thư mục htdocs
- Quản lý hosts file (thêm/xóa/sửa)
- Chuyển đổi phiên bản PHP
- Restart XAMPP và Apache
- Mở dự án trong VSCode hoặc Cursor

⚙️  CẤU HÌNH BAN ĐẦU:

1. Chạy tool lần đầu và chọn "s" để vào Settings
2. Cấu hình các đường dẫn:
   - XAMPP path: Đường dẫn thư mục cài XAMPP (vd: C:\\xampp)
   - htdocs path: Đường dẫn thư mục htdocs (vd: C:\\xampp\\htdocs)
   - Hosts file: Đường dẫn file hosts (mặc định: C:\\Windows\\System32\\drivers\\etc\\hosts)
   - Apache path: Đường dẫn Apache httpd.exe
   - Default editor: Chọn editor mặc định (code/cursor)

📋 CÁC LỆNH QUẢN LÝ DỰ ÁN:

1. Mở dự án:
   [số]          - Mở dự án theo số thứ tự bằng editor mặc định
   o [số]        - Mở dự án và chọn editor (code/cursor)

2. Clone dự án mới:
   c             - Clone dự án từ Git repository
   - Nhập Git URL và tên dự án

3. Xóa dự án:
   d [số]        - Xóa dự án (cần xác nhận YES)

4. Đổi tên dự án:
   r [số]        - Đổi tên dự án

🌐 QUẢN LÝ HOSTS:

1. Xem danh sách hosts:
   h              - Liệt kê tất cả host entries

2. Thêm host mới:
   ha             - Thêm entry mới vào hosts file
   - Nhập domain (vd: mysite.local)
   - Nhập IP (mặc định: 127.0.0.1)

3. Xóa host:
   hd [domain]    - Xóa host entry
   Ví dụ: hd mysite.local

4. Sửa host:
   he [domain]    - Sửa host entry
   Ví dụ: he mysite.local
   - Có thể thay đổi domain hoặc IP

⚠️  LƯU Ý VỀ HOSTS FILE:
- Cần chạy tool với quyền Administrator để chỉnh sửa hosts file
- Luôn backup hosts file trước khi chỉnh sửa
- Các thay đổi sẽ có hiệu lực ngay sau khi lưu

🐘 QUẢN LÝ PHP:

php              - Xem và chuyển đổi phiên bản PHP
- Hiển thị danh sách PHP version có sẵn
- Chọn version để chuyển đổi
- Cần chỉnh sửa httpd.conf thủ công theo hướng dẫn

🔄 QUẢN LÝ XAMPP:

rx               - Restart XAMPP
- Mở XAMPP Control Panel
- Tự động restart Apache và MySQL từ Control Panel

ra               - Restart Apache
- Tự động restart Apache service
- Sử dụng apache_start.bat và apache_stop.bat

⚙️  CÀI ĐẶT:

s                - Vào menu Settings
- Cấu hình các đường dẫn XAMPP, htdocs, hosts, Apache
- Chọn editor mặc định (VSCode hoặc Cursor)

📝 VÍ DỤ SỬ DỤNG:

1. Mở dự án "myproject":
   > 1              (nếu là dự án đầu tiên trong danh sách)
   > o 1            (nếu muốn chọn editor)

2. Clone dự án mới:
   > c
   > Git URL: https://github.com/user/repo.git
   > Tên dự án: mynewproject

3. Thêm host cho dự án:
   > ha
   > Domain: myproject.local
   > IP: 127.0.0.1

4. Đổi tên dự án:
   > r 1
   > Tên mới: newprojectname

5. Xóa dự án:
   > d 1
   > Xác nhận: YES

🔧 YÊU CẦU HỆ THỐNG:

- Windows OS
- XAMPP đã cài đặt
- Git (để clone dự án) - tùy chọn
- VSCode hoặc Cursor (để mở dự án) - tùy chọn

⚠️  LƯU Ý QUAN TRỌNG:

1. Quyền Administrator:
   - Cần chạy với quyền Admin để chỉnh sửa hosts file
   - Không cần Admin để quản lý dự án trong htdocs

2. Đường dẫn:
   - Đảm bảo các đường dẫn cấu hình đúng và tồn tại
   - Tool sẽ tự động tạo config file nếu chưa có

3. Backup:
   - Luôn backup hosts file trước khi chỉnh sửa
   - Backup dự án trước khi xóa

4. Git:
   - Cần cài Git nếu muốn clone dự án
   - Git phải có trong PATH

5. Editor:
   - VSCode/Cursor phải có trong PATH
   - Hoặc cài đặt từ Microsoft Store/Website chính thức

💡 MẸO:

- Sử dụng tab để autocomplete khi nhập đường dẫn
- Luôn kiểm tra đường dẫn trước khi lưu settings
- Sử dụng "h" để xem hosts trước khi thêm/sửa/xóa
- Backup hosts file thường xuyên

============================================================
"""


def get_help():
    """
    Trả về nội dung hướng dẫn sử dụng
    
    Returns:
        str: Nội dung hướng dẫn
    """
    return HELP_TEXT

