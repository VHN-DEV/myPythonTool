#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: Setup Project Linux - Quản lý và cài đặt môi trường Linux

Mục đích: Wrapper Python cho các shell scripts quản lý Linux server
Lý do: Tích hợp vào menu Python tool, chạy trên Windows (Git Bash/WSL) hoặc Linux
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Thêm thư mục gốc vào path để import utils
_root_dir = Path(__file__).parent.parent.parent.parent
if str(_root_dir) not in sys.path:
    sys.path.insert(0, str(_root_dir))
from utils import print_header, print_separator

# Lấy đường dẫn thư mục chứa shell scripts
SCRIPT_DIR = Path(__file__).parent


# Định nghĩa các script chính và mô tả
SCRIPTS = {
    '1': {
        'name': 'App Management',
        'file': 'app.sh',
        'description': 'Quản lý services (Nginx, PHP-FPM) và chạy các scripts trong thư mục run/'
    },
    '2': {
        'name': 'SSH Connection',
        'file': 'connect-ssh.sh',
        'description': 'Kết nối nhanh đến các SSH servers đã cấu hình'
    },
    '3': {
        'name': 'Install Application',
        'file': 'install-app.sh',
        'description': 'Cài đặt ứng dụng từ file .deb, AppImage'
    },
    '4': {
        'name': 'Install Environment',
        'file': 'installs.sh',
        'description': 'Cài đặt các công cụ và môi trường phát triển (Node.js, PHP, Nginx, MySQL, etc.)'
    }
}


def find_bash():
    """Tìm bash executable (Git Bash hoặc WSL trên Windows, bash mặc định trên Linux)"""
    # Trên Linux/macOS, dùng bash mặc định
    if sys.platform.startswith('linux') or sys.platform == 'darwin':
        bash_path = shutil.which('bash')
        if bash_path:
            return ['bash']
    
    # Trên Windows, thử tìm Git Bash hoặc WSL
    if sys.platform == 'win32':
        # Thử Git Bash (thường có trong Program Files)
        git_bash_paths = [
            r"C:\Program Files\Git\bin\bash.exe",
            r"C:\Program Files (x86)\Git\bin\bash.exe",
            os.path.expanduser(r"~\AppData\Local\Programs\Git\bin\bash.exe")
        ]
        
        for bash_path in git_bash_paths:
            if os.path.exists(bash_path):
                return [bash_path]
        
        # Thử WSL
        wsl_path = shutil.which('wsl')
        if wsl_path:
            return ['wsl', 'bash']
        
        # Thử bash.exe trực tiếp (có thể trong PATH)
        bash_exe = shutil.which('bash.exe')
        if bash_exe:
            return [bash_exe]
    
    # Fallback: thử bash mặc định
    return ['bash']


def convert_path_for_bash(script_path: Path, bash_cmd: list) -> str:
    """
    Chuyển đổi đường dẫn script sang format phù hợp với bash
    
    Args:
        script_path: Đường dẫn script (Path object)
        bash_cmd: Lệnh bash được sử dụng
        
    Returns:
        str: Đường dẫn đã được chuyển đổi
    """
    script_path_str = str(script_path.resolve())
    
    # Trên Windows với Git Bash, cần chuyển đường dẫn sang format Unix
    if sys.platform == 'win32' and 'Git' in str(bash_cmd[0]):
        # Chuyển D:\path\to\script.sh thành /d/path/to/script.sh
        if ':' in script_path_str:
            drive = script_path_str[0].lower()
            unix_path = script_path_str.replace('\\', '/').replace(f'{drive}:', f'/{drive}', 1)
            return unix_path
        else:
            return script_path_str.replace('\\', '/')
    elif sys.platform == 'win32' and bash_cmd[0] == 'wsl':
        # Với WSL, có thể cần chuyển đổi đường dẫn
        # Chuyển D:\path\to\script.sh thành /mnt/d/path/to/script.sh
        if ':' in script_path_str:
            drive = script_path_str[0].lower()
            wsl_path = script_path_str.replace('\\', '/').replace(f'{drive}:', f'/mnt/{drive}', 1)
            return wsl_path
        else:
            return script_path_str.replace('\\', '/')
    else:
        # Trên Linux/macOS, chạy trực tiếp
        return str(script_path)


def run_script(script_name: str):
    """
    Chạy một bash script
    
    Args:
        script_name: Tên file script (ví dụ: 'app.sh')
    """
    script_path = SCRIPT_DIR / script_name
    
    if not script_path.exists():
        print(f"\n❌ Không tìm thấy file {script_name}!")
        print(f"   Đường dẫn mong đợi: {script_path}")
        return False
    
    try:
        # Tìm bash executable
        bash_cmd = find_bash()
        
        # Kiểm tra bash có sẵn không
        if len(bash_cmd) > 0 and not shutil.which(bash_cmd[0]) and not os.path.exists(bash_cmd[0]):
            print("\n⚠️  Không tìm thấy bash!")
            print("   Trên Windows, cần cài Git Bash hoặc WSL")
            print("   Trên Linux/macOS, cần cài bash")
            return False
        
        # Chuyển đổi đường dẫn
        script_path_converted = convert_path_for_bash(script_path, bash_cmd)
        cmd = bash_cmd + [script_path_converted]
        
        # Đảm bảo script có quyền thực thi (chỉ trên Linux/macOS)
        if not sys.platform == 'win32':
            os.chmod(script_path, 0o755)
        
        # Chạy script
        print(f"\n🚀 Đang chạy {script_name}...\n")
        print_separator("-")
        result = subprocess.run(cmd, check=False)
        print_separator("-")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"\n❌ Lỗi khi chạy script: {e}")
        print(f"   Hãy đảm bảo đã cài Git Bash hoặc WSL trên Windows")
        return False


def show_menu():
    """Hiển thị menu chọn script"""
    print_header("Setup Project Linux")
    
    print("📋 CHỌN CHỨC NĂNG:\n")
    
    for key, script in SCRIPTS.items():
        print(f"  [{key}] {script['name']}")
        print(f"      {script['description']}\n")
    
    print("  [0] Thoát\n")
    print_separator("-")


def get_user_choice():
    """Lấy lựa chọn từ người dùng"""
    while True:
        try:
            choice = input("👉 Nhập lựa chọn của bạn: ").strip()
            
            if choice == '0':
                return None
            
            if choice in SCRIPTS:
                return choice
            
            print("❌ Lựa chọn không hợp lệ! Vui lòng nhập số từ 0-4.\n")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Đã hủy bởi người dùng.")
            return None
        except EOFError:
            print("\n\n⚠️  Đã hủy bởi người dùng.")
            return None


def check_bash_available():
    """Kiểm tra bash có sẵn không"""
    bash_cmd = find_bash()
    
    if len(bash_cmd) > 0:
        # Kiểm tra bash có tồn tại không
        if shutil.which(bash_cmd[0]) or os.path.exists(bash_cmd[0]):
            return True
    
    return False


def main():
    """Hàm chính - Menu tương tác để chọn script"""
    # Kiểm tra bash có sẵn không
    if not check_bash_available():
        print_header("Setup Project Linux")
        print("❌ Không tìm thấy bash!")
        print("\n📝 Yêu cầu:")
        print("   - Trên Windows: Cần cài Git Bash hoặc WSL")
        print("   - Trên Linux/macOS: Cần cài bash")
        print()
        input("Nhấn Enter để thoát...")
        return
    
    # Hiển thị menu và lấy lựa chọn
    while True:
        show_menu()
        choice = get_user_choice()
        
        if choice is None:
            print("\n👋 Tạm biệt!\n")
            break
        
        # Chạy script đã chọn
        script_info = SCRIPTS[choice]
        success = run_script(script_info['file'])
        
        if success:
            print(f"\n✅ Hoàn thành {script_info['name']}!")
        else:
            print(f"\n⚠️  Có lỗi xảy ra khi chạy {script_info['name']}!")
        
        # Hỏi có muốn tiếp tục không
        print()
        try:
            continue_choice = input("🔄 Bạn có muốn tiếp tục? (y/n): ").strip().lower()
            if continue_choice not in ['y', 'yes', '']:
                print("\n👋 Tạm biệt!\n")
                break
            print()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Tạm biệt!\n")
            break


if __name__ == "__main__":
    main()

