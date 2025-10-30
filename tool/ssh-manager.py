#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: Quản lý và kết nối SSH Server
Mục đích: Kết nối nhanh đến các SSH server đã cấu hình sẵn
"""

import subprocess
import os
from pathlib import Path


def print_header():
    """
    In header của tool
    
    Giải thích:
    - Hiển thị tiêu đề tool
    - Tạo giao diện thân thiện
    """
    print("=" * 60)
    print("  TOOL QUAN LY VA KET NOI SSH SERVER")
    print("=" * 60)
    print()


def get_servers_config():
    """
    Lấy danh sách server từ cấu hình
    
    Return:
        list: Danh sách server config
    
    Giải thích:
    - Trả về danh sách các server đã cấu hình
    - Có thể mở rộng để đọc từ file JSON
    """
    servers = [
        {
            "name": "Server DEV",
            "user": "dev",
            "host": "192.168.10.163",
            "port": 1506,
            "password": None,  # Nếu có password thì điền vào đây
            "ssh_key": None    # Nếu dùng key thì ghi đường dẫn
        },
        {
            "name": "Server TEST",
            "user": "test",
            "host": "192.168.10.200",
            "port": 22,
            "password": None,
            "ssh_key": None
        },
        {
            "name": "Server PROD (key)",
            "user": "prod",
            "host": "192.168.10.250",
            "port": 22,
            "password": None,
            "ssh_key": r"D:\IT\keys\prod_id_rsa"
        }
    ]
    return servers


def connect_server(server):
    """
    Kết nối đến SSH server
    
    Args:
        server (dict): Thông tin server cần kết nối
    
    Giải thích:
    - Bước 1: Xác định phương thức kết nối (key/password)
    - Bước 2: Tạo command SSH phù hợp
    - Bước 3: Thực thi kết nối
    """
    print(f"\n🔌 Đang kết nối đến {server['name']}...")
    print(f"   User: {server['user']}")
    print(f"   Host: {server['host']}")
    print(f"   Port: {server['port']}")
    
    # Kiểm tra SSH key có tồn tại không
    if server["ssh_key"]:
        if not os.path.exists(server["ssh_key"]):
            print(f"❌ Lỗi: Không tìm thấy SSH key tại: {server['ssh_key']}")
            return
        
        # Kết nối bằng SSH key
        print(f"   Auth: SSH Key ({server['ssh_key']})")
        cmd = [
            "ssh",
            "-i", server["ssh_key"],
            f"{server['user']}@{server['host']}",
            "-p", str(server["port"])
        ]
    elif server["password"]:
        # Kết nối bằng password (nhập thủ công trên Windows)
        print(f"   Auth: Password (nhập thủ công khi được hỏi)")
        cmd = [
            "ssh",
            f"{server['user']}@{server['host']}",
            "-p", str(server["port"])
        ]
    else:
        # Mặc định SSH (sẽ hỏi password hoặc dùng key mặc định)
        print(f"   Auth: Mặc định (key hoặc password)")
        cmd = [
            "ssh",
            f"{server['user']}@{server['host']}",
            "-p", str(server["port"])
        ]
    
    print("\n" + "=" * 60)
    
    try:
        # Thực thi lệnh SSH
        subprocess.run(cmd)
        print("\n" + "=" * 60)
        print("✅ Đã ngắt kết nối SSH")
    except FileNotFoundError:
        print("\n" + "=" * 60)
        print("❌ Lỗi: Không tìm thấy lệnh 'ssh'")
        print("💡 Cài đặt OpenSSH hoặc sử dụng Git Bash")
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ Lỗi kết nối: {e}")


def add_new_server(servers):
    """
    Thêm server mới (tính năng mở rộng)
    
    Args:
        servers (list): Danh sách server hiện tại
    
    Return:
        dict: Thông tin server mới hoặc None
    
    Giải thích:
    - Cho phép người dùng thêm server mới
    - Validate input
    - Trả về config server mới
    """
    print("\n" + "=" * 60)
    print("  THEM SERVER MOI")
    print("=" * 60)
    
    try:
        name = input("Tên server (vd: My VPS): ").strip()
        if not name:
            print("❌ Tên server không được để trống")
            return None
        
        user = input("Username SSH: ").strip()
        if not user:
            print("❌ Username không được để trống")
            return None
        
        host = input("Host/IP: ").strip()
        if not host:
            print("❌ Host không được để trống")
            return None
        
        port_input = input("Port SSH (mặc định 22): ").strip()
        port = int(port_input) if port_input else 22
        
        use_key = input("Sử dụng SSH key? (y/N): ").strip().lower()
        
        if use_key == 'y':
            ssh_key = input("Đường dẫn SSH key: ").strip()
            if not os.path.exists(ssh_key):
                print(f"⚠️  Cảnh báo: Key không tồn tại tại {ssh_key}")
            new_server = {
                "name": name,
                "user": user,
                "host": host,
                "port": port,
                "password": None,
                "ssh_key": ssh_key
            }
        else:
            new_server = {
                "name": name,
                "user": user,
                "host": host,
                "port": port,
                "password": None,
                "ssh_key": None
            }
        
        print("\n✅ Đã thêm server mới (chỉ trong phiên này)")
        return new_server
    
    except ValueError:
        print("❌ Port phải là số")
        return None
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return None


def show_help():
    """
    Hiển thị hướng dẫn sử dụng
    
    Giải thích:
    - Hướng dẫn cách cấu hình server
    - Các phương thức xác thực
    - Troubleshooting
    """
    print("\n" + "=" * 60)
    print("  HUONG DAN SU DUNG SSH MANAGER")
    print("=" * 60)
    print("""
📖 CÁCH CẤU HÌNH SERVER:

1. Mở file: tool/ssh-manager.py
2. Tìm hàm get_servers_config()
3. Thêm server mới vào danh sách:

   {
       "name": "Tên server",
       "user": "username",
       "host": "192.168.1.100",  # IP hoặc domain
       "port": 22,               # Port SSH
       "password": None,         # Password (nếu có)
       "ssh_key": None           # Đường dẫn key (nếu có)
   }

🔐 PHƯƠNG THỨC XÁC THỰC:

1. SSH Key (khuyến nghị):
   - ssh_key: r"C:\\Users\\You\\.ssh\\id_rsa"
   - password: None

2. Password (nhập thủ công):
   - ssh_key: None
   - password: None (sẽ hỏi khi kết nối)

3. Mặc định:
   - Cả hai đều None
   - SSH sẽ tự động xử lý

⚠️  LƯU Ý BẢO MẬT:

- KHÔNG lưu password trong code
- Sử dụng SSH key thay vì password
- Bảo vệ file config (chmod 600)
- Thêm vào .gitignore nếu có thông tin nhạy cảm

🛠️ YÊU CẦU:

- Windows: Cài OpenSSH hoặc dùng Git Bash
- Linux/Mac: SSH có sẵn

Kiểm tra: ssh -V
""")
    input("\nNhấn Enter để quay lại menu...")


def main():
    """
    Hàm chính của tool
    
    Giải thích:
    - Bước 1: Hiển thị header
    - Bước 2: Lấy danh sách server
    - Bước 3: Hiển thị menu và xử lý lựa chọn
    - Bước 4: Kết nối đến server được chọn
    """
    print_header()
    
    # Lấy danh sách server
    servers = get_servers_config()
    
    while True:
        print("\n" + "=" * 60)
        print("  DANH SACH SSH SERVER")
        print("=" * 60)
        
        # Hiển thị danh sách server
        for idx, server in enumerate(servers, start=1):
            auth_method = "🔑 Key" if server["ssh_key"] else "🔐 Pass"
            print(f"{idx}. [{auth_method}] {server['name']}")
            print(f"   → {server['user']}@{server['host']}:{server['port']}")
        
        print("\n" + "-" * 60)
        print("a. Thêm server mới (tạm thời)")
        print("h. Hướng dẫn cấu hình")
        print("0. Quay lại menu chính")
        print("=" * 60)
        
        choice = input("\nChọn số để SSH: ").strip().lower()
        
        # Xử lý lựa chọn
        if choice == '0':
            print("\n👋 Thoát SSH Manager")
            break
        elif choice == 'h':
            show_help()
        elif choice == 'a':
            new_server = add_new_server(servers)
            if new_server:
                servers.append(new_server)
        else:
            try:
                idx = int(choice)
                if 1 <= idx <= len(servers):
                    connect_server(servers[idx - 1])
                else:
                    print("❌ Lựa chọn không hợp lệ")
            except ValueError:
                print("❌ Vui lòng nhập số hoặc lệnh hợp lệ")
            except KeyboardInterrupt:
                print("\n\n⚠️  Đã hủy kết nối")
            except Exception as e:
                print(f"❌ Lỗi: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Đã hủy!")
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")

