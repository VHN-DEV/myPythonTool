#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module helpers - Các hàm tiện ích hỗ trợ UI/UX

Mục đích: Tập trung các hàm helper cho UI/UX
"""

import difflib
from typing import List, Optional
from .colors import Colors


def highlight_keyword(text: str, keyword: str) -> str:
    """
    Highlight keyword trong text
    
    Args:
        text: Text gốc
        keyword: Keyword cần highlight
    
    Returns:
        str: Text với keyword được highlight
    """
    if not keyword:
        return text
    
    keyword_lower = keyword.lower()
    text_lower = text.lower()
    
    if keyword_lower not in text_lower:
        return text
    
    # Tìm vị trí keyword
    start = text_lower.find(keyword_lower)
    end = start + len(keyword)
    
    # Highlight
    highlighted = (
        text[:start] +
        Colors.bold(Colors.success(text[start:end])) +
        text[end:]
    )
    
    return highlighted


def suggest_command(user_input: str, valid_commands: List[str], max_suggestions: int = 3) -> List[str]:
    """
    Gợi ý command gần đúng khi user nhập sai
    
    Args:
        user_input: Input từ user
        valid_commands: Danh sách commands hợp lệ
        max_suggestions: Số lượng gợi ý tối đa
    
    Returns:
        list: Danh sách commands gợi ý
    """
    if not user_input:
        return []
    
    # Tìm commands tương tự
    suggestions = difflib.get_close_matches(
        user_input.lower(),
        [cmd.lower() for cmd in valid_commands],
        n=max_suggestions,
        cutoff=0.3
    )
    
    # Map về commands gốc
    result = []
    for sug in suggestions:
        for cmd in valid_commands:
            if cmd.lower() == sug:
                result.append(cmd)
                break
    
    return result


def format_tips() -> List[str]:
    """
    Tạo danh sách tips ngẫu nhiên
    
    Returns:
        list: Danh sách tips
    """
    tips = [
        "💡 Tip: Nhập 'h' để xem hướng dẫn đầy đủ",
        "💡 Tip: Dùng 's [keyword]' để tìm kiếm nhanh",
        "💡 Tip: Thêm tool vào favorites bằng 'f+ [số]'",
        "💡 Tip: Nhập số + 'h' (vd: '1h') để xem hướng dẫn tool",
        "💡 Tip: Dùng 'r' để xem recent tools",
        "💡 Tip: Nhập 'clear' để xóa màn hình",
        "💡 Tip: Dùng 'f' để xem tất cả favorites",
        "💡 Tip: Nhập 'set' để xem settings",
    ]
    
    return tips


def print_welcome_tip():
    """
    In một tip ngẫu nhiên khi khởi động
    """
    import random
    tips = format_tips()
    tip = random.choice(tips)
    print(Colors.muted(f"  {tip}"))


def print_command_suggestions(user_input: str, suggestions: List[str]):
    """
    In gợi ý commands khi user nhập sai
    
    Args:
        user_input: Input từ user
        suggestions: Danh sách suggestions
    """
    if not suggestions:
        return
    
    print()
    print(Colors.warning(f"⚠️  Không tìm thấy lệnh: '{user_input}'"))
    
    if len(suggestions) == 1:
        print(Colors.info(f"💡 Có phải bạn muốn: {Colors.bold(suggestions[0])}?"))
    else:
        print(Colors.info(f"💡 Gợi ý ({len(suggestions)}): {', '.join([Colors.bold(s) for s in suggestions])}"))
    
    print()

