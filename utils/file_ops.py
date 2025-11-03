#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module file_ops - Các hàm thao tác với file và thư mục

Mục đích: Tập trung các thao tác file/folder operations
Lý do: Tách riêng logic file operations để dễ maintain và test
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional, Tuple


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
    - Sử dụng Path và generator để tối ưu memory
    """
    total_size = 0
    folder = Path(folder_path)
    
    if not folder.exists() or not folder.is_dir():
        return 0
    
    try:
        # Sử dụng Path.rglob() thay vì os.walk() để tối ưu hơn
        for file_path in folder.rglob('*'):
            if file_path.is_file():
                try:
                    total_size += file_path.stat().st_size
                except (OSError, PermissionError):
                    # Bỏ qua file không có quyền truy cập
                    pass
    except (OSError, PermissionError):
        pass
    
    return total_size


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


def ensure_directory_exists(directory: str) -> None:
    """
    Đảm bảo thư mục tồn tại, tạo mới nếu chưa có
    
    Args:
        directory: Đường dẫn thư mục
    
    Mục đích: Tránh lỗi khi ghi file vào thư mục chưa tồn tại
    """
    Path(directory).mkdir(parents=True, exist_ok=True)


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


def get_available_space(path: str) -> int:
    """
    Lấy dung lượng trống của ổ đĩa
    
    Args:
        path: Đường dẫn bất kỳ trên ổ đĩa
    
    Returns:
        int: Dung lượng trống (bytes)
    
    Mục đích: Kiểm tra trước khi thực hiện thao tác tốn dung lượng
    """
    try:
        stat = shutil.disk_usage(path)
        return stat.free
    except Exception:
        return 0

