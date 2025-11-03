#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hướng dẫn sử dụng tool: setup-project-linux
"""

HELP_TEXT = """
============================================================
     HƯỚNG DẪN SỬ DỤNG: SETUP PROJECT LINUX
============================================================

📋 MÔ TẢ:
   Tool quản lý và cài đặt môi trường Linux server thông qua
   các shell scripts được tổ chức sẵn.

⚠️  YÊU CẦU:
   - Trên Windows: Cần cài Git Bash hoặc WSL để chạy bash scripts
   - Trên Linux/macOS: Cần bash (thường có sẵn)
   - Cần quyền sudo cho một số thao tác (trên Linux)
   - Các shell scripts phải có trong thư mục tools/sh/setup-project-linux/

🔧 CHỨC NĂNG CHÍNH:

Tool cung cấp menu tương tác để chọn một trong 4 chức năng chính:

1. App Management (app.sh)
   - Quản lý services (Nginx, PHP-FPM)
   - Chạy các scripts trong thư mục run/
   - Khởi động/dừng/restart services
   - Kiểm tra trạng thái services
   - Quản lý virtual hosts Nginx

2. SSH Connection (connect-ssh.sh)
   - Kết nối nhanh đến các SSH servers đã cấu hình
   - Quản lý danh sách kết nối trong thư mục connect/
   - Tự động liệt kê các kết nối SSH có sẵn
   - Hỗ trợ sshpass cho kết nối tự động

3. Install Application (install-app.sh)
   - Cài đặt ứng dụng từ file .deb, AppImage
   - Quản lý ứng dụng trong thư mục Downloads và add-app/
   - Tự động thiết lập quyền thực thi
   - Tạo desktop entries cho AppImage
   - Tự động fix dependencies cho .deb packages

4. Install Environment (installs.sh)
   - Cài đặt các công cụ và môi trường phát triển
   - Bao gồm: Node.js, PHP, Nginx, MySQL, Composer, Git, etc.
   - Tổ chức scripts cài đặt trong thư mục run-install/
   - Dễ dàng mở rộng với scripts cài đặt mới

📁 CẤU TRÚC THƯ MỤC:

tools/sh/setup-project-linux/
├── app.sh              # Menu quản lý chính
├── connect-ssh.sh      # Kết nối SSH
├── install-app.sh      # Cài đặt ứng dụng
├── installs.sh         # Cài đặt môi trường
├── run/                # Scripts chạy services
│   ├── main.sh
│   ├── create-nginx-site.sh
│   ├── switch-php.sh
│   └── ...
├── connect/            # Cấu hình SSH connections
│   ├── monglau.sh
│   └── ...
├── run-install/        # Scripts cài đặt
│   ├── install-nginx.sh
│   ├── install-php.sh
│   └── ...
└── add-app/            # Thư mục ứng dụng

💡 CÁCH SỬ DỤNG:

1. Chạy tool từ menu chính:
   ```bash
   python tools/sh/setup-project-linux/setup-project-linux.py
   ```

2. Chọn chức năng từ menu:
   - [1] App Management - Quản lý services và scripts
   - [2] SSH Connection - Kết nối SSH servers
   - [3] Install Application - Cài đặt ứng dụng
   - [4] Install Environment - Cài đặt môi trường phát triển
   - [0] Thoát

3. Tool sẽ tự động chạy shell script tương ứng
4. Làm theo hướng dẫn trong shell script
5. Sau khi hoàn thành, có thể chọn tiếp tục hoặc thoát

✨ TÍNH NĂNG MỚI:

- ✅ Menu tương tác đẹp mắt và dễ sử dụng
- ✅ Tự động phát hiện và chuyển đổi đường dẫn cho Windows (Git Bash/WSL)
- ✅ Validation và error handling tốt hơn
- ✅ Hỗ trợ cả Git Bash, WSL và bash native trên Linux/macOS
- ✅ Kiểm tra bash availability trước khi chạy
- ✅ Cho phép tiếp tục hoặc thoát sau mỗi thao tác

⚠️  LƯU Ý:

- Tool có thể chạy trên Windows thông qua Git Bash hoặc WSL
- Trên Linux: Một số thao tác cần quyền sudo
- Các shell scripts phải có quyền thực thi (chmod +x)
- Tool tự động cấp quyền thực thi khi chạy (trên Linux/macOS)
- Trên Windows, Git Bash tự xử lý quyền thực thi
- Đường dẫn Windows sẽ tự động chuyển đổi sang format Unix khi cần

📚 LIÊN KẾT:

- Thư mục scripts: tools/sh/setup-project-linux/
- README: Xem trong thư mục scripts (nếu có)

============================================================
"""


def get_help():
    """Trả về hướng dẫn sử dụng"""
    return HELP_TEXT


if __name__ == "__main__":
    print(get_help())

