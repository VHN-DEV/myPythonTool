#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module validation - Các hàm xác thực và xử lý input

Mục đích: Tập trung các hàm validate và xử lý input từ người dùng
Lý do: Tách riêng logic validation để dễ maintain và test
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Optional, Tuple
from .colors import Colors


def get_user_input(prompt: str, default: Optional[str] = None, 
                   strip_quotes: bool = True) -> str:
    """
    Lấy input từ người dùng với các tùy chọn
    
    Args:
        prompt: Câu hỏi hiển thị
        default: Giá trị mặc định nếu user nhấn Enter
        strip_quotes: Có tự động xóa dấu ngoặc kép không
    
    Returns:
        str: Input từ người dùng
    
    Giải thích:
    - Hiển thị giá trị default trong prompt
    - Tự động xóa dấu ngoặc kép (khi kéo thả file vào terminal)
    - Xử lý đường dẫn Windows với backslash
    - Trả về default nếu user không nhập gì
    """
    if default:
        prompt_text = f"{prompt} (mặc định: {default}): "
    else:
        prompt_text = f"{prompt}: "
    
    user_input = input(prompt_text).strip()
    
    if strip_quotes:
        # Xóa dấu ngoặc kép và ngoặc đơn ở đầu/cuối
        user_input = user_input.strip('"').strip("'").strip()
    
    if not user_input and default:
        return default
    
    return user_input


def normalize_path(path: str) -> str:
    """
    Chuẩn hóa đường dẫn (xử lý kéo thả trên Windows)
    
    Args:
        path: Đường dẫn cần chuẩn hóa
    
    Returns:
        str: Đường dẫn đã chuẩn hóa
    
    Giải thích:
    - Xóa dấu ngoặc kép/đơn ở đầu cuối
    - Xử lý khoảng trắng thừa
    - Chuyển đổi về đường dẫn tuyệt đối
    - Xử lý backslash trên Windows
    
    Mục đích: 
    - Hỗ trợ kéo thả folder vào terminal
    - Xử lý đúng các đường dẫn có khoảng trắng
    """
    # Bước 1: Xóa khoảng trắng ở đầu cuối
    path = path.strip()
    
    # Bước 2: Xóa dấu ngoặc kép/đơn
    if (path.startswith('"') and path.endswith('"')) or \
       (path.startswith("'") and path.endswith("'")):
        path = path[1:-1]
    
    # Bước 3: Xóa khoảng trắng thừa lần nữa sau khi xóa ngoặc
    path = path.strip()
    
    # Bước 4: Chuyển về đường dẫn tuyệt đối và chuẩn hóa
    path = os.path.abspath(os.path.expanduser(path))
    
    # Bước 5: Chuẩn hóa separators (\ thành / hoặc ngược lại tùy OS)
    path = os.path.normpath(path)
    
    return path


def confirm_action(message: str, require_yes: bool = False) -> bool:
    """
    Hỏi xác nhận từ người dùng
    
    Args:
        message: Thông báo cần xác nhận
        require_yes: True = yêu cầu nhập "YES", False = chỉ cần "y" hoặc "Y"
    
    Returns:
        bool: True nếu người dùng xác nhận, False nếu từ chối
    
    Mục đích: Tránh thao tác nguy hiểm (xóa file, thay đổi hàng loạt...)
    Lý do: Bảo vệ người dùng khỏi các thao tác không mong muốn
    """
    print(f"\n⚠️  {message}")
    
    if require_yes:
        confirmation = input("Nhập 'YES' để xác nhận: ").strip()
        return confirmation == "YES"
    else:
        confirmation = input("Xác nhận? (Y/n): ").strip().lower()
        return confirmation != 'n'


def validate_path(path: str, must_exist: bool = True, 
                  must_be_dir: bool = False, 
                  must_be_file: bool = False) -> Tuple[bool, str]:
    """
    Kiểm tra tính hợp lệ của đường dẫn
    
    Args:
        path: Đường dẫn cần kiểm tra
        must_exist: Path phải tồn tại
        must_be_dir: Path phải là thư mục
        must_be_file: Path phải là file
    
    Returns:
        tuple: (is_valid, error_message)
    
    Giải thích:
    - Kiểm tra path có tồn tại không
    - Kiểm tra path có phải là thư mục/file không
    - Trả về thông báo lỗi chi tiết nếu không hợp lệ
    """
    if not path:
        return False, "Đường dẫn không được để trống"
    
    path_obj = Path(path)
    
    if must_exist and not path_obj.exists():
        return False, f"Đường dẫn không tồn tại: {path}"
    
    if must_be_dir and must_exist and not path_obj.is_dir():
        return False, f"Đường dẫn không phải là thư mục: {path}"
    
    if must_be_file and must_exist and not path_obj.is_file():
        return False, f"Đường dẫn không phải là file: {path}"
    
    return True, ""


def parse_size_string(size_str: str) -> int:
    """
    Parse chuỗi kích thước thành bytes
    
    Args:
        size_str: Chuỗi kích thước (vd: "10MB", "1.5GB", "500KB")
    
    Returns:
        int: Kích thước tính bằng bytes
    
    Ví dụ:
        parse_size_string("10MB") -> 10485760
        parse_size_string("1.5GB") -> 1610612736
    """
    size_str = size_str.upper().strip()
    
    units = {
        'B': 1,
        'KB': 1024,
        'MB': 1024**2,
        'GB': 1024**3,
        'TB': 1024**4
    }
    
    for unit, multiplier in units.items():
        if size_str.endswith(unit):
            try:
                number = float(size_str[:-len(unit)])
                return int(number * multiplier)
            except ValueError:
                return 0
    
    # Nếu không có đơn vị, coi như là bytes
    try:
        return int(size_str)
    except ValueError:
        return 0


def install_library(package_name: str, install_command: str, 
                    library_display_name: Optional[str] = None) -> bool:
    """
    Cài đặt thư viện tự động khi thiếu
    
    Args:
        package_name: Tên package (vd: "qrcode[pil]")
        install_command: Lệnh cài đặt (vd: "pip install qrcode[pil]")
        library_display_name: Tên hiển thị của thư viện (mặc định: package_name)
    
    Returns:
        bool: True nếu cài đặt thành công, False nếu không
    
    Giải thích:
    - Hiển thị thông báo thiếu thư viện
    - Hỏi người dùng có muốn cài đặt tự động không
    - Nếu có, chạy pip install
    - Trả về True nếu thành công, False nếu không
    
    Mục đích: 
    - Tự động hóa việc cài đặt thư viện
    - Cải thiện UX khi thiếu dependencies
    """
    display_name = library_display_name or package_name
    
    print(Colors.error(f"❌ Thiếu thư viện {display_name}!"))
    print(f"Cài đặt: {install_command}")
    print()
    
    choice = get_user_input(
        f"Bạn có muốn cài đặt tự động không? (y/n, mặc định: y): ",
        default="y"
    ).strip().lower()
    
    if choice and choice not in ['y', 'yes']:
        return False
    
    try:
        print()
        print(Colors.info(f"📦 Đang cài đặt {display_name}..."))
        
        # Tách install_command để lấy package names
        # Xử lý các trường hợp: "pip install package", "package", etc.
        install_parts = install_command.split()
        
        # Tìm phần "install" để lấy các package sau đó
        if "install" in install_parts:
            install_idx = install_parts.index("install")
            packages = install_parts[install_idx + 1:]
        else:
            # Nếu không có "install", coi toàn bộ là packages
            packages = install_parts
        
        # Tạo command với sys.executable -m pip install
        args = [sys.executable, "-m", "pip", "install"] + packages
        
        # Chạy lệnh cài đặt
        result = subprocess.run(
            args,
            check=True,
            capture_output=True,
            text=True
        )
        
        print(Colors.success(f"✅ Đã cài đặt {display_name} thành công!"))
        print(Colors.warning("💡 Tool cần restart để nhận package mới."))
        print()
        return True
        
    except subprocess.CalledProcessError as e:
        print(Colors.error(f"❌ Lỗi khi cài đặt: {e}"))
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        print()
        return False
    except Exception as e:
        print(Colors.error(f"❌ Lỗi không mong muốn: {e}"))
        print()
        return False

