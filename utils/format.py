#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module format - Các hàm format và hiển thị

Mục đích: Tập trung các hàm format dữ liệu và hiển thị UI
Lý do: Tách riêng logic format để dễ maintain và test
"""


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

