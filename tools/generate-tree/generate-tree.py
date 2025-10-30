#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: Tạo cây thư mục của dự án (directory tree)
"""

import os
from pathlib import Path


def print_header():
    print("=" * 60)
    print("  TOOL TẠO CÂY THƯ MỤC")
    print("=" * 60)
    print()


def should_ignore(name, ignore_list):
    """Kiểm tra xem có nên bỏ qua không"""
    for pattern in ignore_list:
        if pattern in name or name == pattern:
            return True
    return False


def generate_tree(directory, prefix="", ignore_list=None, max_depth=None, current_depth=0, show_hidden=False):
    """
    Tạo cây thư mục
    
    Args:
        directory: Thư mục gốc
        prefix: Prefix cho mỗi dòng
        ignore_list: Danh sách folder/file cần bỏ qua
        max_depth: Độ sâu tối đa
        current_depth: Độ sâu hiện tại
        show_hidden: Hiển thị file/folder ẩn
    
    Returns:
        list: Danh sách các dòng cây thư mục
    """
    if ignore_list is None:
        ignore_list = []
    
    if max_depth is not None and current_depth >= max_depth:
        return []
    
    tree_lines = []
    
    try:
        entries = list(os.scandir(directory))
        entries.sort(key=lambda e: (not e.is_dir(), e.name.lower()))
        
        # Lọc entries
        if not show_hidden:
            entries = [e for e in entries if not e.name.startswith('.')]
        
        entries = [e for e in entries if not should_ignore(e.name, ignore_list)]
        
        for index, entry in enumerate(entries):
            is_last = index == len(entries) - 1
            
            # Ký tự vẽ cây
            connector = "└── " if is_last else "├── "
            extension = "    " if is_last else "│   "
            
            # Icon
            if entry.is_dir():
                icon = "📁 "
            else:
                # Icon theo loại file
                ext = os.path.splitext(entry.name)[1].lower()
                icon_map = {
                    '.py': '🐍 ',
                    '.js': '📜 ',
                    '.html': '🌐 ',
                    '.css': '🎨 ',
                    '.json': '📋 ',
                    '.txt': '📄 ',
                    '.md': '📝 ',
                    '.jpg': '🖼️ ',
                    '.jpeg': '🖼️ ',
                    '.png': '🖼️ ',
                    '.gif': '🖼️ ',
                    '.mp4': '🎬 ',
                    '.mp3': '🎵 ',
                    '.zip': '📦 ',
                    '.pdf': '📕 ',
                }
                icon = icon_map.get(ext, '📄 ')
            
            line = f"{prefix}{connector}{icon}{entry.name}"
            tree_lines.append(line)
            
            # Đệ quy vào thư mục con
            if entry.is_dir():
                sub_tree = generate_tree(
                    entry.path,
                    prefix + extension,
                    ignore_list,
                    max_depth,
                    current_depth + 1,
                    show_hidden
                )
                tree_lines.extend(sub_tree)
    
    except PermissionError:
        tree_lines.append(f"{prefix}[Không có quyền truy cập]")
    
    return tree_lines


def save_tree_to_file(tree_lines, output_file, header_info):
    """Lưu cây thư mục ra file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write(f"  CÂY THƯ MỤC: {header_info}\n")
        f.write("=" * 60 + "\n\n")
        for line in tree_lines:
            f.write(line + "\n")
        f.write("\n" + "=" * 60 + "\n")
        f.write(f"Tổng cộng: {len(tree_lines)} mục\n")


def count_stats(tree_lines):
    """Đếm thống kê"""
    folders = sum(1 for line in tree_lines if '📁' in line)
    files = len(tree_lines) - folders
    return folders, files


def main():
    print_header()
    
    # Nhập thư mục
    folder_input = input("Nhập đường dẫn thư mục (Enter để dùng thư mục hiện tại): ").strip('"')
    if not folder_input:
        folder_input = "."
    
    if not os.path.isdir(folder_input):
        print("❌ Thư mục không tồn tại!")
        return
    
    folder_path = Path(folder_input).resolve()
    
    # Tùy chọn
    ignore_input = input("\nCác thư mục/file cần bỏ qua (cách nhau bởi dấu phẩy, Enter để mặc định: node_modules, .git, __pycache__): ")
    if ignore_input.strip():
        ignore_list = [item.strip() for item in ignore_input.split(',')]
    else:
        ignore_list = ['node_modules', '.git', '__pycache__', '.vscode', '.idea', 'venv', 'env', 'dist', 'build']
    
    max_depth_input = input("Độ sâu tối đa (Enter để không giới hạn): ").strip()
    max_depth = int(max_depth_input) if max_depth_input else None
    
    show_hidden_input = input("Hiển thị file/folder ẩn (bắt đầu bằng .)? (y/N): ").strip().lower()
    show_hidden = show_hidden_input == 'y'
    
    # Tạo cây
    print(f"\n🌳 Đang tạo cây thư mục...\n")
    print("=" * 60)
    print(f"📂 {folder_path.name}/")
    print("=" * 60)
    
    tree_lines = generate_tree(
        folder_path,
        ignore_list=ignore_list,
        max_depth=max_depth,
        show_hidden=show_hidden
    )
    
    # In ra màn hình (giới hạn 100 dòng đầu)
    for line in tree_lines[:100]:
        print(line)
    
    if len(tree_lines) > 100:
        print(f"\n... và {len(tree_lines) - 100} mục khác")
    
    # Thống kê
    folders, files = count_stats(tree_lines)
    print("\n" + "=" * 60)
    print(f"📊 Tổng kết:")
    print(f"   - Thư mục: {folders}")
    print(f"   - File: {files}")
    print(f"   - Tổng cộng: {len(tree_lines)} mục")
    print("=" * 60)
    
    # Lưu ra file
    save_input = input("\nLưu kết quả ra file? (Y/n): ").strip().lower()
    if save_input != 'n':
        output_file = f"tree_{folder_path.name}.txt"
        save_tree_to_file(tree_lines, output_file, folder_path.name)
        print(f"\n✅ Đã lưu vào: {output_file}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Đã hủy!")
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")

