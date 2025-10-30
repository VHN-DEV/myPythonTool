#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: Quản lý và kết nối SSH Server
Mục đích: Kết nối nhanh đến các SSH server đã cấu hình sẵn
"""

import subprocess
import os
import json
import sys
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass


def get_default_ssh_key():
    """
    Lấy đường dẫn SSH key mặc định
    
    Return:
        str: Đường dẫn key mặc định hoặc None
    
    Giải thích:
    - Kiểm tra đường dẫn key mặc định có tồn tại không
    - Trả về path nếu tồn tại, None nếu không
    """
    default_key = r"C:\Users\Asus\.ssh\id_rsa"
    
    if os.path.exists(default_key):
        return default_key
    return None


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


def get_config_file():
    """
    Lấy đường dẫn file config
    
    Return:
        Path: Đường dẫn file ssh_config.json
    
    Giải thích:
    - File config lưu trong thư mục gốc project
    - Tự động tạo nếu chưa có
    """
    config_file = Path("ssh_config.json")
    return config_file


def load_servers():
    """
    Load danh sách server từ file config
    
    Return:
        list: Danh sách server config
    
    Giải thích:
    - Bước 1: Kiểm tra file config có tồn tại không
    - Bước 2: Đọc và parse JSON
    - Bước 3: Trả về danh sách server hoặc mẫu mặc định
    """
    config_file = get_config_file()
    
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('servers', [])
        except Exception as e:
            print(f"[!] Loi doc config: {e}")
            return get_default_servers()
    else:
        # Tạo config mặc định
        default = get_default_servers()
        save_servers(default)
        return default


def save_servers(servers):
    """
    Lưu danh sách server vào file config
    
    Args:
        servers (list): Danh sách server cần lưu
    
    Return:
        bool: True nếu lưu thành công
    
    Giải thích:
    - Bước 1: Tạo dict config với metadata
    - Bước 2: Ghi ra file JSON với format đẹp
    - Bước 3: Xử lý lỗi nếu có
    """
    config_file = get_config_file()
    
    try:
        data = {
            'version': '1.0',
            'servers': servers
        }
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[X] Loi luu config: {e}")
        return False


def get_default_servers():
    """
    Lấy danh sách server mẫu mặc định
    
    Return:
        list: Danh sách server mẫu
    
    Giải thích:
    - Cung cấp ví dụ cấu hình cho người dùng
    - Người dùng có thể sửa hoặc xóa
    """
    servers = [
        {
            "name": "Server DEV (Mẫu)",
            "user": "dev",
            "host": "192.168.10.163",
            "port": 1506,
            "password": None,
            "ssh_key": None,
            "description": "Server development - Ví dụ cấu hình"
        },
        {
            "name": "Server TEST (Mẫu)",
            "user": "test",
            "host": "192.168.10.200",
            "port": 22,
            "password": None,
            "ssh_key": None,
            "description": "Server testing - Có thể xóa"
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
    print(f"\n[>] Dang ket noi den {server['name']}...")
    print(f"   User: {server['user']}")
    print(f"   Host: {server['host']}")
    print(f"   Port: {server['port']}")
    
    # Kiểm tra SSH key có tồn tại không
    if server.get("ssh_key"):
        if not os.path.exists(server["ssh_key"]):
            print(f"[X] Loi: Khong tim thay SSH key tai: {server['ssh_key']}")
            return
        
        # Kết nối bằng SSH key
        print(f"   Auth: SSH Key ({server['ssh_key']})")
        cmd = [
            "ssh",
            "-i", server["ssh_key"],
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
        print("[OK] Da ngat ket noi SSH")
    except FileNotFoundError:
        print("\n" + "=" * 60)
        print("[X] Loi: Khong tim thay lenh 'ssh'")
        print("[i] Cai dat OpenSSH hoac su dung Git Bash")
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"[X] Loi ket noi: {e}")


def add_new_server(servers):
    """
    Thêm server mới
    
    Args:
        servers (list): Danh sách server hiện tại
    
    Return:
        bool: True nếu thêm thành công
    
    Giải thích:
    - Thu thập thông tin server từ người dùng
    - Validate input
    - Thêm vào danh sách và lưu vào file
    """
    print("\n" + "=" * 60)
    print("  THEM SERVER MOI")
    print("=" * 60)
    
    try:
        name = input("\nTên server (vd: My VPS): ").strip()
        if not name:
            print("[X] Ten server khong duoc de trong")
            return False
        
        user = input("Username SSH: ").strip()
        if not user:
            print("[X] Username khong duoc de trong")
            return False
        
        host = input("Host/IP: ").strip()
        if not host:
            print("[X] Host khong duoc de trong")
            return False
        
        port_input = input("Port SSH (mặc định 22): ").strip()
        port = int(port_input) if port_input else 22
        
        description = input("Mô tả (tùy chọn): ").strip()
        
        use_key = input("Sử dụng SSH key? (y/N): ").strip().lower()
        
        ssh_key = None
        if use_key == 'y':
            # Hiển thị đường dẫn mặc định nếu có
            default_key = get_default_ssh_key()
            if default_key:
                print(f"[i] Key mac dinh: {default_key}")
                key_path = input(f"Duong dan SSH key (Enter = mac dinh): ").strip()
                if not key_path:
                    key_path = default_key
            else:
                key_path = input("Đường dẫn SSH key: ").strip()
            
            if key_path:
                if not os.path.exists(key_path):
                    print(f"[!] Canh bao: Key khong ton tai tai {key_path}")
                    confirm = input("Vẫn muốn lưu? (y/N): ").strip().lower()
                    if confirm != 'y':
                        return False
                ssh_key = key_path
        
        new_server = {
            "name": name,
            "user": user,
            "host": host,
            "port": port,
            "password": None,
            "ssh_key": ssh_key,
            "description": description
        }
        
        servers.append(new_server)
        
        if save_servers(servers):
            print("\n[OK] Da them va luu server moi!")
            return True
        else:
            print("\n[X] Loi luu server")
            servers.pop()  # Rollback
            return False
    
    except ValueError:
        print("[X] Port phai la so")
        return False
    except Exception as e:
        print(f"[X] Loi: {e}")
        return False


def delete_server(servers):
    """
    Xóa server
    
    Args:
        servers (list): Danh sách server hiện tại
    
    Return:
        bool: True nếu xóa thành công
    
    Giải thích:
    - Hiển thị danh sách server
    - Cho phép người dùng chọn server cần xóa
    - Xác nhận trước khi xóa
    - Lưu lại config sau khi xóa
    """
    if not servers:
        print("\n[X] Khong co server nao de xoa")
        return False
    
    print("\n" + "=" * 60)
    print("  XOA SERVER")
    print("=" * 60)
    
    # Hiển thị danh sách
    for idx, server in enumerate(servers, start=1):
        auth = "[Key]" if server.get("ssh_key") else "[Pass]"
        desc = f" - {server.get('description', '')}" if server.get('description') else ""
        print(f"{idx}. {auth} {server['name']}{desc}")
        print(f"   {server['user']}@{server['host']}:{server['port']}")
    
    print("\n0. Hủy bỏ")
    
    try:
        choice = input("\nChọn server cần xóa (số): ").strip()
        
        if choice == '0':
            print("Đã hủy")
            return False
        
        idx = int(choice)
        if 1 <= idx <= len(servers):
            server = servers[idx - 1]
            
            # Xác nhận
            print(f"\n[!] BAN SAP XOA SERVER: {server['name']}")
            confirm = input("Xác nhận xóa? (YES để xác nhận): ").strip()
            
            if confirm == "YES":
                servers.pop(idx - 1)
                if save_servers(servers):
                    print(f"\n[OK] Da xoa server: {server['name']}")
                    return True
                else:
                    print("\n❌ Lỗi lưu config")
                    return False
            else:
                print("Đã hủy")
                return False
        else:
            print("[X] Lua chon khong hop le")
            return False
    
    except ValueError:
        print("[X] Vui long nhap so")
        return False
    except Exception as e:
        print(f"[X] Loi: {e}")
        return False


def edit_server(servers):
    """
    Chỉnh sửa server
    
    Args:
        servers (list): Danh sách server hiện tại
    
    Return:
        bool: True nếu sửa thành công
    
    Giải thích:
    - Cho phép sửa thông tin server
    - Giữ nguyên giá trị cũ nếu người dùng không nhập
    - Lưu lại config sau khi sửa
    """
    if not servers:
        print("\n[X] Khong co server nao de sua")
        return False
    
    print("\n" + "=" * 60)
    print("  CHINH SUA SERVER")
    print("=" * 60)
    
    # Hiển thị danh sách
    for idx, server in enumerate(servers, start=1):
        auth = "[Key]" if server.get("ssh_key") else "[Pass]"
        print(f"{idx}. {auth} {server['name']}")
        print(f"   {server['user']}@{server['host']}:{server['port']}")
    
    print("\n0. Hủy bỏ")
    
    try:
        choice = input("\nChọn server cần sửa (số): ").strip()
        
        if choice == '0':
            print("Đã hủy")
            return False
        
        idx = int(choice)
        if 1 <= idx <= len(servers):
            server = servers[idx - 1]
            
            print(f"\n[*] Dang sua: {server['name']}")
            print("(Nhấn Enter để giữ nguyên giá trị cũ)\n")
            
            # Tên
            new_name = input(f"Tên [{server['name']}]: ").strip()
            if new_name:
                server['name'] = new_name
            
            # User
            new_user = input(f"User [{server['user']}]: ").strip()
            if new_user:
                server['user'] = new_user
            
            # Host
            new_host = input(f"Host [{server['host']}]: ").strip()
            if new_host:
                server['host'] = new_host
            
            # Port
            new_port = input(f"Port [{server['port']}]: ").strip()
            if new_port:
                server['port'] = int(new_port)
            
            # Description
            current_desc = server.get('description', '')
            new_desc = input(f"Mô tả [{current_desc}]: ").strip()
            if new_desc:
                server['description'] = new_desc
            
            # SSH Key
            current_key = server.get('ssh_key', 'None')
            print(f"\nSSH Key hiện tại: {current_key}")
            change_key = input("Thay đổi SSH key? (y/N): ").strip().lower()
            if change_key == 'y':
                # Hiển thị đường dẫn mặc định nếu có
                default_key = get_default_ssh_key()
                if default_key:
                    print(f"[i] Key mac dinh: {default_key}")
                    new_key = input("Duong dan key moi (Enter = mac dinh, 'none' = xoa): ").strip()
                    if not new_key:
                        new_key = default_key
                else:
                    new_key = input("Đường dẫn key mới (hoặc 'none' để xóa): ").strip()
                
                if new_key.lower() == 'none':
                    server['ssh_key'] = None
                elif new_key:
                    if not os.path.exists(new_key):
                        print(f"[!] Canh bao: Key không tồn tại")
                    server['ssh_key'] = new_key
            
            if save_servers(servers):
                print(f"\n[OK] Da luu thay doi!")
                return True
            else:
                print("\n[X] Loi lưu config")
                return False
        else:
            print("[X] Lua chon khong hop le")
            return False
    
    except ValueError:
        print("[X] Vui long nhap so hop le")
        return False
    except Exception as e:
        print(f"[X] Loi: {e}")
        return False


def show_help():
    """
    Hiển thị hướng dẫn sử dụng
    
    Giải thích:
    - Hướng dẫn cấu hình server
    - Các phương thức xác thực
    - Troubleshooting
    """
    print("\n" + "=" * 60)
    print("  HUONG DAN SU DUNG SSH MANAGER")
    print("=" * 60)
    
    # Hiển thị key mặc định nếu có
    default_key = get_default_ssh_key()
    key_info = ""
    if default_key:
        key_info = f"\n[i] Key mac dinh duoc phat hien: {default_key}"
    
    print(f"""
📖 QUẢN LÝ CẤU HÌNH:

Tool lưu cấu hình trong file: ssh_config.json

Các lệnh quản lý:
  a - Thêm server mới
  d - Xóa server
  e - Sửa server
  v - Xem file config

🔐 PHƯƠNG THỨC XÁC THỰC:

1. SSH Key (khuyen nghi):
   - An toan, khong can nhap password
   - Nhan Enter de dung key mac dinh khi duoc hoi{key_info}

2. Password (nhap thu cong):
   - SSH se tu dong hoi khi ket noi
   - Khong luu password trong config (an toan)

[!] LUU Y BAO MAT:

- KHONG bao gio luu password trong config
- Su dung SSH key thay vi password
- Bao ve file ssh_config.json (chmod 600)
- Them ssh_config.json vao .gitignore

[*] YEU CAU:

- Windows: OpenSSH hoặc Git Bash
- Linux/Mac: SSH có sẵn

Kiem tra: ssh -V

[*] MEO:

- Tao SSH key: ssh-keygen -t rsa -b 4096
- Copy key len server: ssh-copy-id user@host
- Test ket noi: ssh user@host
""")
    input("\nNhấn Enter để quay lại menu...")


def view_config():
    """
    Xem nội dung file config
    
    Giải thích:
    - Hiển thị đường dẫn file config
    - Hiển thị nội dung JSON
    - Hữu ích cho debug
    """
    config_file = get_config_file()
    
    print("\n" + "=" * 60)
    print("  FILE CONFIG")
    print("=" * 60)
    print(f"\nĐường dẫn: {config_file.absolute()}")
    
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
            print("\nNội dung:")
            print("-" * 60)
            print(content)
            print("-" * 60)
        except Exception as e:
            print(f"\n[X] Loi doc file: {e}")
    else:
        print("\n[!] File config chua ton tai")
    
    input("\nNhấn Enter để quay lại menu...")


def main():
    """
    Hàm chính của tool
    
    Giải thích:
    - Bước 1: Hiển thị header
    - Bước 2: Load danh sách server từ config
    - Bước 3: Hiển thị menu và xử lý lựa chọn
    - Bước 4: Thực hiện hành động (kết nối/thêm/xóa/sửa)
    """
    print_header()
    
    while True:
        # Load danh sách server (refresh mỗi lần loop)
        servers = load_servers()
        
        print("\n" + "=" * 60)
        print("  DANH SACH SSH SERVER")
        print("=" * 60)
        
        if servers:
            # Hiển thị danh sách server
            for idx, server in enumerate(servers, start=1):
                auth_method = "[Key]" if server.get("ssh_key") else "[Pass]"
                desc = f" - {server.get('description', '')}" if server.get('description') else ""
                print(f"{idx}. {auth_method} {server['name']}{desc}")
                print(f"   -> {server['user']}@{server['host']}:{server['port']}")
        else:
            print("\n[!] Chua co server nao. Hay them server moi!")
        
        print("\n" + "-" * 60)
        print("QUẢN LÝ:")
        print("  a - Thêm server mới")
        print("  d - Xóa server")
        print("  e - Sửa server")
        print("  v - Xem file config")
        print("  h - Hướng dẫn chi tiết")
        print("  0 - Quay lại menu chính")
        print("=" * 60)
        
        choice = input("\nChọn số để SSH hoặc lệnh: ").strip().lower()
        
        # Xử lý lựa chọn
        if choice == '0':
            print("\n[*] Thoat SSH Manager")
            break
        elif choice == 'h':
            show_help()
        elif choice == 'a':
            add_new_server(servers)
        elif choice == 'd':
            delete_server(servers)
        elif choice == 'e':
            edit_server(servers)
        elif choice == 'v':
            view_config()
        else:
            try:
                idx = int(choice)
                if 1 <= idx <= len(servers):
                    connect_server(servers[idx - 1])
                else:
                    print("[X] Lua chon khong hop le")
            except ValueError:
                print("[X] Vui long nhap so hoac lenh hop le")
            except KeyboardInterrupt:
                print("\n\n[!] Da huy ket noi")
            except Exception as e:
                print(f"[X] Loi: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[X] Da huy!")
    except Exception as e:
        print(f"\n[X] Loi: {e}")
