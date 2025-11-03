#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: Optimize Shrink PDF - Nén và tối ưu file PDF

Mục đích: Wrapper Python cho shell script optimize-shrinkpdf
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
from utils.format import print_separator

# Lấy đường dẫn thư mục chứa shell scripts
SCRIPT_DIR = Path(__file__).parent
SCRIPT_FILE = SCRIPT_DIR / "optimize-shrinkpdf.sh"


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
    """Chuyển đổi đường dẫn script sang format phù hợp với bash"""
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
        # Với WSL, chuyển D:\path\to\script.sh thành /mnt/d/path/to/script.sh
        if ':' in script_path_str:
            drive = script_path_str[0].lower()
            wsl_path = script_path_str.replace('\\', '/').replace(f'{drive}:', f'/mnt/{drive}', 1)
            return wsl_path
        else:
            return script_path_str.replace('\\', '/')
    else:
        # Trên Linux/macOS, chạy trực tiếp
        return str(script_path)


def main():
    """Hàm chính - Chạy optimize-shrinkpdf script"""
    if not SCRIPT_FILE.exists():
        print(f"\n❌ Không tìm thấy file optimize-shrinkpdf.sh!")
        print(f"   Đường dẫn mong đợi: {SCRIPT_FILE}")
        return
    
    try:
        # Tìm bash executable
        bash_cmd = find_bash()
        
        # Kiểm tra bash có sẵn không
        if len(bash_cmd) > 0 and not shutil.which(bash_cmd[0]) and not os.path.exists(bash_cmd[0]):
            print("\n⚠️  Không tìm thấy bash!")
            print("   Trên Windows, cần cài Git Bash hoặc WSL")
            print("   Trên Linux/macOS, cần cài bash")
            return
        
        # Chuyển đổi đường dẫn
        script_path_converted = convert_path_for_bash(SCRIPT_FILE, bash_cmd)
        cmd = bash_cmd + [script_path_converted]
        
        # Thêm các arguments từ command line nếu có
        if len(sys.argv) > 1:
            cmd.extend(sys.argv[1:])
        
        # Đảm bảo script có quyền thực thi (chỉ trên Linux/macOS)
        if not sys.platform == 'win32':
            os.chmod(SCRIPT_FILE, 0o755)
        
        # Chạy script
        print(f"\n🚀 Đang chạy optimize-shrinkpdf.sh...\n")
        print_separator("-")
        result = subprocess.run(cmd, check=False)
        print_separator("-")
        
        if result.returncode == 0:
            print(f"\n✅ Hoàn thành!")
        else:
            print(f"\n⚠️  Script đã kết thúc với mã lỗi: {result.returncode}")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Đã hủy bởi người dùng.")
    except Exception as e:
        print(f"\n❌ Lỗi khi chạy script: {e}")
        print(f"   Hãy đảm bảo đã cài Git Bash hoặc WSL trên Windows")


if __name__ == "__main__":
    main()

