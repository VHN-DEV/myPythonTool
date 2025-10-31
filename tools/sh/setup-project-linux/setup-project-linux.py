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

# Lấy đường dẫn thư mục chứa shell scripts
SCRIPT_DIR = Path(__file__).parent.parent.parent / "tools" / "sh" / "setup-project-linux"


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


def run_app_sh():
    """Chạy app.sh script"""
    app_sh_path = SCRIPT_DIR / "app.sh"
    
    if not app_sh_path.exists():
        print(f"❌ Không tìm thấy file app.sh!")
        print(f"   Đường dẫn mong đợi: {app_sh_path}")
        return
    
    try:
        # Tìm bash executable
        bash_cmd = find_bash()
        
        # Trên Windows với Git Bash, cần chuyển đường dẫn sang format Unix
        if sys.platform == 'win32' and 'Git' in str(bash_cmd[0]):
            # Chuyển D:\path\to\app.sh thành /d/path/to/app.sh
            script_path_str = str(app_sh_path.resolve())
            if ':' in script_path_str:
                drive = script_path_str[0].lower()
                unix_path = script_path_str.replace('\\', '/').replace(f'{drive}:', f'/{drive}', 1)
            else:
                unix_path = script_path_str.replace('\\', '/')
            # Chạy script với đường dẫn Unix
            cmd = bash_cmd + [unix_path]
        elif sys.platform == 'win32' and bash_cmd[0] == 'wsl':
            # Với WSL, chạy script trực tiếp
            cmd = bash_cmd + [str(app_sh_path)]
        else:
            # Trên Linux/macOS, chạy trực tiếp
            cmd = bash_cmd + [str(app_sh_path)]
        
        # Đảm bảo script có quyền thực thi (chỉ trên Linux/macOS)
        if not sys.platform == 'win32':
            os.chmod(app_sh_path, 0o755)
        
        # Chạy script
        subprocess.run(cmd, check=False)
    except Exception as e:
        print(f"❌ Lỗi khi chạy script: {e}")
        print(f"   Hãy đảm bảo đã cài Git Bash hoặc WSL trên Windows")


def main():
    """Hàm chính - Chạy trực tiếp app.sh"""
    print("=" * 60)
    print("           SETUP PROJECT LINUX")
    print("=" * 60)
    print()
    
    # Kiểm tra bash có sẵn không
    bash_cmd = find_bash()
    if not shutil.which(bash_cmd[0]) and not os.path.exists(bash_cmd[0]):
        print("⚠️  Không tìm thấy bash!")
        print("   Trên Windows, cần cài Git Bash hoặc WSL")
        print("   Trên Linux/macOS, cần cài bash")
        print()
        input("Nhấn Enter để thoát...")
        return
    
    # Chạy app.sh trực tiếp
    print("🚀 Đang chạy app.sh...\n")
    run_app_sh()


if __name__ == "__main__":
    main()

