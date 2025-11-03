#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module format - Các hàm format và hiển thị

Mục đích: Tập trung các hàm format dữ liệu và hiển thị UI
Lý do: Tách riêng logic format để dễ maintain và test
"""

from .colors import Colors, print_colored, print_success, print_error, print_warning, print_info


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


def print_header(title: str, width: int = 60, color: str = None) -> None:
    """
    In header đẹp cho tool
    
    Args:
        title: Tiêu đề tool
        width: Độ rộng của header
        color: Màu sắc cho header (từ Colors)
    
    Mục đích: Tạo giao diện đồng nhất cho tất cả tools
    """
    separator = "═" * width
    title_line = f"  {title.upper()}"
    
    if color:
        print_colored(separator, color)
        print_colored(title_line, color)
        print_colored(separator, color)
    else:
        print(separator)
        print(title_line)
        print(separator)
    print()


def print_separator(char: str = "=", width: int = 60, color: str = None) -> None:
    """
    In đường phân cách
    
    Args:
        char: Ký tự phân cách
        width: Độ rộng
        color: Màu sắc cho separator (từ Colors)
    """
    separator = char * width
    if color:
        print_colored(separator, color)
    else:
        print(separator)


def print_section(title: str, width: int = 60, color: str = Colors.PRIMARY) -> None:
    """
    In section header đẹp
    
    Args:
        title: Tiêu đề section
        width: Độ rộng
        color: Màu sắc
    """
    print()
    print_separator("─", width, color)
    print_colored(f"  {title}", color)
    print_separator("─", width, color)
    print()


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

