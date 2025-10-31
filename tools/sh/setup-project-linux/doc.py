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

1. App Management (app.sh)
   - Quản lý services (Nginx, PHP-FPM)
   - Chạy các scripts trong thư mục run/
   - Khởi động/dừng/restart services

2. SSH Connection (connect-ssh.sh)
   - Kết nối nhanh đến các SSH servers đã cấu hình
   - Quản lý danh sách kết nối trong thư mục connect/

3. Install App (install-app.sh)
   - Cài đặt ứng dụng từ file .deb, AppImage
   - Quản lý ứng dụng trong thư mục Downloads
   - Tự động thiết lập quyền thực thi

4. Installs (installs.sh)
   - Cài đặt các công cụ và môi trường phát triển
   - Bao gồm: Node.js, PHP, Nginx, MySQL, Composer, etc.

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

1. Chạy tool từ menu chính
2. Chọn chức năng cần dùng
3. Tool sẽ tự động chạy shell script tương ứng
4. Làm theo hướng dẫn trong shell script

⚠️  LƯU Ý:

- Tool có thể chạy trên Windows thông qua Git Bash hoặc WSL
- Trên Linux: Một số thao tác cần quyền sudo
- Các shell scripts phải có quyền thực thi (chmod +x)
- Tool tự động cấp quyền thực thi khi chạy (trên Linux/macOS)
- Trên Windows, Git Bash tự xử lý quyền thực thi

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

