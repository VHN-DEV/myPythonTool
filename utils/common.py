#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module common - Các hàm tiện ích dùng chung

Mục đích: Tập trung các hàm được sử dụng nhiều lần trong các tool
Lý do: Tránh code duplicate, dễ maintain và test
"""

import os
import sys
from pathlib import Path
from typing import List, Optional, Tuple


def format_size(size_bytes: int) -> str:
    """
    Format dung lượng file thành dạng dễ đọc
    
    Args:
        size_bytes: Dung lượng tính bằng bytes
    
    Returns:
        str: Dung lượng đã format (vd: "1.50 MB")
    
    Giải thích:
    - Chuyển đổi từ bytes sang KB, MB, GB, TB
    - Giữ 2 chữ số thập phân
    - Tự động chọn đơn vị phù hợp
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def print_header(title: str, width: int = 60) -> None:
    """
    In header đẹp cho tool
    
    Args:
        title: Tiêu đề tool
        width: Độ rộng của header
    
    Mục đích: Tạo giao diện đồng nhất cho tất cả tools
    """
    print("=" * width)
    print(f"  {title.upper()}")
    print("=" * width)
    print()


def print_separator(char: str = "=", width: int = 60) -> None:
    """
    In đường phân cách
    
    Args:
        char: Ký tự phân cách
        width: Độ rộng
    """
    print(char * width)


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


def get_file_list(directory: str, extensions: Optional[List[str]] = None, 
                  recursive: bool = True, exclude_patterns: Optional[List[str]] = None) -> List[str]:
    """
    Lấy danh sách file trong thư mục
    
    Args:
        directory: Thư mục cần quét
        extensions: Danh sách phần mở rộng cần lọc (vd: ['.jpg', '.png'])
        recursive: Có quét thư mục con không
        exclude_patterns: Danh sách pattern cần loại trừ
    
    Returns:
        list: Danh sách đường dẫn file
    
    Giải thích:
    - Quét tất cả file trong thư mục
    - Lọc theo extension nếu có
    - Loại trừ các pattern không mong muốn (node_modules, .git...)
    - Hỗ trợ cả recursive và non-recursive
    """
    file_list = []
    directory = Path(directory)
    
    if exclude_patterns is None:
        exclude_patterns = []
    
    def should_exclude(path: Path) -> bool:
        """Kiểm tra có nên loại trừ path này không"""
        path_str = str(path)
        for pattern in exclude_patterns:
            if pattern in path_str:
                return True
        return False
    
    if recursive:
        for root, dirs, files in os.walk(directory):
            # Loại bỏ các thư mục không mong muốn khỏi dirs
            dirs[:] = [d for d in dirs if not should_exclude(Path(root) / d)]
            
            for file in files:
                file_path = Path(root) / file
                
                if should_exclude(file_path):
                    continue
                
                # Kiểm tra extension
                if extensions:
                    if file_path.suffix.lower() in extensions:
                        file_list.append(str(file_path))
                else:
                    file_list.append(str(file_path))
    else:
        for item in directory.iterdir():
            if item.is_file():
                if should_exclude(item):
                    continue
                
                if extensions:
                    if item.suffix.lower() in extensions:
                        file_list.append(str(item))
                else:
                    file_list.append(str(item))
    
    return file_list


def get_folder_size(folder_path: str) -> int:
    """
    Tính tổng dung lượng của thư mục
    
    Args:
        folder_path: Đường dẫn thư mục
    
    Returns:
        int: Tổng dung lượng (bytes)
    
    Giải thích:
    - Duyệt qua tất cả file trong thư mục và thư mục con
    - Cộng dồn kích thước của từng file
    - Bỏ qua file không tồn tại hoặc không có quyền truy cập
    """
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                try:
                    if os.path.exists(file_path):
                        total_size += os.path.getsize(file_path)
                except (OSError, PermissionError):
                    # Bỏ qua file không có quyền truy cập
                    pass
    except (OSError, PermissionError):
        pass
    
    return total_size


def create_backup_name(base_name: str, extension: str = "", use_timestamp: bool = True) -> str:
    """
    Tạo tên file backup với timestamp
    
    Args:
        base_name: Tên cơ sở
        extension: Phần mở rộng file
        use_timestamp: Có thêm timestamp không
    
    Returns:
        str: Tên file backup
    
    Ví dụ:
        create_backup_name("document", ".txt") -> "document_backup_20240115_143022.txt"
    """
    if use_timestamp:
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base_name}_backup_{timestamp}{extension}"
    else:
        return f"{base_name}_backup{extension}"


def ensure_directory_exists(directory: str) -> None:
    """
    Đảm bảo thư mục tồn tại, tạo mới nếu chưa có
    
    Args:
        directory: Đường dẫn thư mục
    
    Mục đích: Tránh lỗi khi ghi file vào thư mục chưa tồn tại
    """
    Path(directory).mkdir(parents=True, exist_ok=True)


def safe_delete(path: str) -> Tuple[bool, str]:
    """
    Xóa file/folder an toàn
    
    Args:
        path: Đường dẫn cần xóa
    
    Returns:
        tuple: (success, error_message)
    
    Giải thích:
    - Xóa file hoặc thư mục
    - Bắt và xử lý exception
    - Trả về kết quả và thông báo lỗi nếu có
    """
    import shutil
    
    try:
        path_obj = Path(path)
        
        if path_obj.is_file():
            path_obj.unlink()
        elif path_obj.is_dir():
            shutil.rmtree(path)
        else:
            return False, "Đường dẫn không tồn tại"
        
        return True, ""
    except PermissionError:
        return False, "Không có quyền xóa"
    except Exception as e:
        return False, str(e)


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


def get_available_space(path: str) -> int:
    """
    Lấy dung lượng trống của ổ đĩa
    
    Args:
        path: Đường dẫn bất kỳ trên ổ đĩa
    
    Returns:
        int: Dung lượng trống (bytes)
    
    Mục đích: Kiểm tra trước khi thực hiện thao tác tốn dung lượng
    """
    import shutil
    
    try:
        stat = shutil.disk_usage(path)
        return stat.free
    except Exception:
        return 0


def pluralize(count: int, singular: str, plural: str = None) -> str:
    """
    Trả về dạng số ít hoặc số nhiều tùy theo count
    
    Args:
        count: Số lượng
        singular: Dạng số ít
        plural: Dạng số nhiều (nếu None thì thêm 's' vào singular)
    
    Returns:
        str: Chuỗi đã được pluralize
    
    Ví dụ:
        pluralize(1, "file") -> "1 file"
        pluralize(5, "file") -> "5 files"
        pluralize(2, "category", "categories") -> "2 categories"
    """
    if plural is None:
        plural = singular + 's'
    
    return f"{count} {singular if count == 1 else plural}"

