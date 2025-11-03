#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module colors - Quản lý màu sắc cho terminal

Mục đích: Tập trung các hàm và class để hiển thị màu sắc trong terminal
Lý do: Tách riêng logic màu sắc để dễ maintain và tương thích cross-platform
"""

import sys
from typing import Optional

# Thử import colorama, nếu không có thì dùng ANSI codes trực tiếp
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)  # Auto reset sau mỗi print
    HAS_COLORAMA = True
except ImportError:
    # Fallback: Dùng ANSI codes trực tiếp
    class Fore:
        BLACK = '\033[30m'
        RED = '\033[31m'
        GREEN = '\033[32m'
        YELLOW = '\033[33m'
        BLUE = '\033[34m'
        MAGENTA = '\033[35m'
        CYAN = '\033[36m'
        WHITE = '\033[37m'
        RESET = '\033[0m'
        
        # Bright colors
        LIGHTBLACK_EX = '\033[90m'
        LIGHTRED_EX = '\033[91m'
        LIGHTGREEN_EX = '\033[92m'
        LIGHTYELLOW_EX = '\033[93m'
        LIGHTBLUE_EX = '\033[94m'
        LIGHTMAGENTA_EX = '\033[95m'
        LIGHTCYAN_EX = '\033[96m'
        LIGHTWHITE_EX = '\033[97m'
    
    class Back:
        BLACK = '\033[40m'
        RED = '\033[41m'
        GREEN = '\033[42m'
        YELLOW = '\033[43m'
        BLUE = '\033[44m'
        MAGENTA = '\033[45m'
        CYAN = '\033[46m'
        WHITE = '\033[47m'
        RESET = '\033[0m'
    
    class Style:
        DIM = '\033[2m'
        NORMAL = '\033[22m'
        BRIGHT = '\033[1m'
        RESET_ALL = '\033[0m'
    
    HAS_COLORAMA = False


# Kiểm tra xem terminal có hỗ trợ màu sắc không
def supports_color() -> bool:
    """
    Kiểm tra xem terminal có hỗ trợ màu sắc không
    
    Returns:
        bool: True nếu terminal hỗ trợ màu sắc
    """
    if sys.platform == 'win32':
        # Trên Windows, cần colorama hoặc console hỗ trợ ANSI
        return HAS_COLORAMA or (hasattr(sys.stdout, 'isatty') and sys.stdout.isatty())
    
    # Trên Unix/Linux/macOS, kiểm tra TERM variable
    import os
    term = os.environ.get('TERM', '')
    return (
        hasattr(sys.stdout, 'isatty') and 
        sys.stdout.isatty() and 
        term.lower() not in ('dumb', 'unknown')
    )


# Global flag để bật/tắt màu sắc
_ENABLE_COLORS = True


def enable_colors(enabled: bool = True):
    """
    Bật/tắt màu sắc
    
    Args:
        enabled: True để bật màu sắc, False để tắt
    """
    global _ENABLE_COLORS
    _ENABLE_COLORS = enabled and supports_color()


def is_color_enabled() -> bool:
    """
    Kiểm tra xem màu sắc có được bật không
    
    Returns:
        bool: True nếu màu sắc được bật
    """
    return _ENABLE_COLORS


# Khởi tạo
enable_colors(supports_color())


class Colors:
    """
    Class chứa các màu sắc và style định nghĩa sẵn
    
    Sử dụng:
        print(f"{Colors.SUCCESS}Thành công!{Colors.RESET}")
        print(Colors.info("Thông tin"))
    """
    
    # Reset
    RESET = Style.RESET_ALL if supports_color() else ''
    
    # Text colors
    BLACK = Fore.BLACK if supports_color() else ''
    RED = Fore.RED if supports_color() else ''
    GREEN = Fore.GREEN if supports_color() else ''
    YELLOW = Fore.YELLOW if supports_color() else ''
    BLUE = Fore.BLUE if supports_color() else ''
    MAGENTA = Fore.MAGENTA if supports_color() else ''
    CYAN = Fore.CYAN if supports_color() else ''
    WHITE = Fore.WHITE if supports_color() else ''
    
    # Bright colors
    BRIGHT_BLACK = Fore.LIGHTBLACK_EX if supports_color() else ''
    BRIGHT_RED = Fore.LIGHTRED_EX if supports_color() else ''
    BRIGHT_GREEN = Fore.LIGHTGREEN_EX if supports_color() else ''
    BRIGHT_YELLOW = Fore.LIGHTYELLOW_EX if supports_color() else ''
    BRIGHT_BLUE = Fore.LIGHTBLUE_EX if supports_color() else ''
    BRIGHT_MAGENTA = Fore.LIGHTMAGENTA_EX if supports_color() else ''
    BRIGHT_CYAN = Fore.LIGHTCYAN_EX if supports_color() else ''
    BRIGHT_WHITE = Fore.LIGHTWHITE_EX if supports_color() else ''
    
    # Semantic colors (cho UI/UX tốt hơn)
    SUCCESS = BRIGHT_GREEN
    ERROR = BRIGHT_RED
    WARNING = BRIGHT_YELLOW
    INFO = BRIGHT_BLUE
    PRIMARY = BRIGHT_CYAN
    SECONDARY = BRIGHT_MAGENTA
    MUTED = BRIGHT_BLACK
    
    # Styles
    BOLD = Style.BRIGHT if supports_color() else ''
    DIM = Style.DIM if supports_color() else ''
    NORMAL = Style.NORMAL if supports_color() else ''
    
    @staticmethod
    def colorize(text: str, color: str) -> str:
        """
        Thêm màu sắc vào text
        
        Args:
            text: Text cần thêm màu
            color: Màu sắc (từ Fore hoặc Colors)
        
        Returns:
            str: Text đã có màu (hoặc text gốc nếu màu bị tắt)
        """
        if not is_color_enabled():
            return text
        return f"{color}{text}{Colors.RESET}"
    
    @staticmethod
    def success(text: str) -> str:
        """Tạo text màu xanh lá (thành công)"""
        return Colors.colorize(text, Colors.SUCCESS)
    
    @staticmethod
    def error(text: str) -> str:
        """Tạo text màu đỏ (lỗi)"""
        return Colors.colorize(text, Colors.ERROR)
    
    @staticmethod
    def warning(text: str) -> str:
        """Tạo text màu vàng (cảnh báo)"""
        return Colors.colorize(text, Colors.WARNING)
    
    @staticmethod
    def info(text: str) -> str:
        """Tạo text màu xanh dương (thông tin)"""
        return Colors.colorize(text, Colors.INFO)
    
    @staticmethod
    def primary(text: str) -> str:
        """Tạo text màu cyan (primary)"""
        return Colors.colorize(text, Colors.PRIMARY)
    
    @staticmethod
    def secondary(text: str) -> str:
        """Tạo text màu magenta (secondary)"""
        return Colors.colorize(text, Colors.SECONDARY)
    
    @staticmethod
    def muted(text: str) -> str:
        """Tạo text màu xám (muted)"""
        return Colors.colorize(text, Colors.MUTED)
    
    @staticmethod
    def bold(text: str) -> str:
        """Tạo text đậm"""
        if not is_color_enabled():
            return text
        return f"{Colors.BOLD}{text}{Colors.RESET}"


def print_colored(text: str, color: str = None):
    """
    In text có màu sắc
    
    Args:
        text: Text cần in
        color: Màu sắc (từ Colors)
    """
    if color:
        print(Colors.colorize(text, color))
    else:
        print(text)


def print_success(text: str):
    """In text thành công (màu xanh lá)"""
    print(Colors.success(text))


def print_error(text: str):
    """In text lỗi (màu đỏ)"""
    print(Colors.error(text))


def print_warning(text: str):
    """In text cảnh báo (màu vàng)"""
    print(Colors.warning(text))


def print_info(text: str):
    """In text thông tin (màu xanh dương)"""
    print(Colors.info(text))


def print_primary(text: str):
    """In text primary (màu cyan)"""
    print(Colors.primary(text))


def format_box(text: str, 
               width: int = 60, 
               border_char: str = "═",
               padding: int = 1,
               title: Optional[str] = None,
               color: Optional[str] = None) -> str:
    """
    Tạo box đẹp xung quanh text
    
    Args:
        text: Nội dung bên trong box
        width: Độ rộng của box
        border_char: Ký tự border
        padding: Khoảng cách từ border đến text
        title: Tiêu đề (hiển thị trên border)
        color: Màu sắc cho box
    
    Returns:
        str: Text đã được format thành box
    """
    lines = text.split('\n')
    box_lines = []
    
    # Top border
    top_border = border_char * width
    if title:
        title_part = f" {title} "
        padding_chars = (width - len(title_part)) // 2
        top_border = (border_char * padding_chars) + title_part + (border_char * (width - padding_chars - len(title_part)))
    
    box_lines.append(top_border)
    
    # Padding top
    box_lines.append(border_char[0] + ' ' * (width - 2) + border_char[0])
    
    # Content
    for line in lines:
        # Wrap text nếu quá dài
        while len(line) > width - 4 - (padding * 2):
            box_lines.append(
                border_char[0] + 
                ' ' * padding + 
                line[:width - 4 - (padding * 2)] + 
                ' ' * padding + 
                border_char[0]
            )
            line = line[width - 4 - (padding * 2):]
        
        # Padding cho line
        padding_left = ' ' * padding
        padding_right = ' ' * (width - len(line) - (padding * 2) - 2)
        box_lines.append(
            border_char[0] + 
            padding_left + 
            line + 
            padding_right + 
            ' ' * padding + 
            border_char[0]
        )
    
    # Padding bottom
    box_lines.append(border_char[0] + ' ' * (width - 2) + border_char[0])
    
    # Bottom border
    box_lines.append(border_char * width)
    
    result = '\n'.join(box_lines)
    
    if color and is_color_enabled():
        return Colors.colorize(result, color)
    
    return result

