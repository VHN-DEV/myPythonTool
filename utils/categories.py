#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module categories - Phân loại tools theo categories

Mục đích: Tổ chức tools theo categories để dễ tìm kiếm và hiển thị
Lý do: Khi có nhiều tools, cần phân loại để UX tốt hơn
"""

from typing import Dict, List, Optional


# Mapping từ keywords trong tên tool -> category
CATEGORY_KEYWORDS = {
    'image': ['image', 'anh', 'hinh', 'photo', 'picture', 'watermark', 'compress-images'],
    'video': ['video', 'phim', 'movie', 'video-converter'],
    'file': ['file', 'folder', 'backup', 'organizer', 'rename', 'duplicate', 'copy'],
    'archive': ['archive', 'extract', 'compress', 'zip', 'rar', '7z'],
    'text': ['text', 'encoding', 'find', 'replace', 'json', 'format'],
    'pdf': ['pdf'],
    'git': ['git', 'commit', 'changed'],
    'system': ['clean', 'temp', 'setup', 'project', 'tree'],
    'network': ['ssh', 'server', 'connect', 'remote'],
}


# Category icons và colors
CATEGORY_INFO = {
    'image': {
        'icon': '🖼️',
        'name': 'Hình ảnh',
        'color': 'MAGENTA'
    },
    'video': {
        'icon': '🎬',
        'name': 'Video',
        'color': 'RED'
    },
    'file': {
        'icon': '📁',
        'name': 'File & Thư mục',
        'color': 'BLUE'
    },
    'archive': {
        'icon': '📦',
        'name': 'Nén & Giải nén',
        'color': 'CYAN'
    },
    'text': {
        'icon': '📝',
        'name': 'Text & Encoding',
        'color': 'GREEN'
    },
    'pdf': {
        'icon': '📄',
        'name': 'PDF',
        'color': 'YELLOW'
    },
    'git': {
        'icon': '🔀',
        'name': 'Git',
        'color': 'BLUE'
    },
    'system': {
        'icon': '⚙️',
        'name': 'Hệ thống',
        'color': 'WHITE'
    },
    'network': {
        'icon': '🌐',
        'name': 'Network & Server',
        'color': 'CYAN'
    },
    'other': {
        'icon': '🔧',
        'name': 'Khác',
        'color': 'MUTED'
    }
}


def detect_tool_category(tool_name: str, tool_tags: Optional[List[str]] = None) -> str:
    """
    Phát hiện category của tool dựa trên tên và tags
    
    Args:
        tool_name: Tên file tool (vd: backup-folder.py)
        tool_tags: Danh sách tags của tool (optional)
    
    Returns:
        str: Tên category (vd: 'file', 'image', 'other')
    """
    tool_lower = tool_name.lower()
    
    # Check trong tags nếu có
    if tool_tags:
        for tag in tool_tags:
            tag_lower = tag.lower()
            for category, keywords in CATEGORY_KEYWORDS.items():
                if any(kw in tag_lower for kw in keywords):
                    return category
    
    # Check trong tên file
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in tool_lower for kw in keywords):
            return category
    
    # Default: other
    return 'other'


def group_tools_by_category(tools: List[str], tool_manager) -> Dict[str, List[str]]:
    """
    Nhóm tools theo categories
    
    Args:
        tools: Danh sách tools
        tool_manager: ToolManager instance để lấy tags
    
    Returns:
        dict: Dictionary với key là category, value là list tools
    """
    grouped = {}
    
    for tool in tools:
        tags = tool_manager.get_tool_tags(tool)
        category = detect_tool_category(tool, tags)
        
        if category not in grouped:
            grouped[category] = []
        
        grouped[category].append(tool)
    
    # Sắp xếp categories theo thứ tự định sẵn
    category_order = list(CATEGORY_INFO.keys())
    sorted_grouped = {}
    
    for cat in category_order:
        if cat in grouped:
            sorted_grouped[cat] = grouped[cat]
    
    # Thêm các categories khác nếu có
    for cat, tools_list in grouped.items():
        if cat not in sorted_grouped:
            sorted_grouped[cat] = tools_list
    
    return sorted_grouped


def get_category_info(category: str) -> Dict:
    """
    Lấy thông tin category (icon, name, color)
    
    Args:
        category: Tên category
    
    Returns:
        dict: Thông tin category
    """
    return CATEGORY_INFO.get(category, CATEGORY_INFO['other'])

