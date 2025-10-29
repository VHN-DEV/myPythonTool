#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: Tạo cây thư mục của dự án (directory tree)
"""

import os
from pathlib import Path


def print_header():
    print("=" * 60)
    print("  TOOL TAO CAY THU MUC")
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
        tree_lines.append(f"{prefix}[Khong co quyen truy cap]")
    
    return tree_lines


def save_tree_to_file(tree_lines, output_file, header_info):
    """Lưu cây thư mục ra file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write(f"  CAY THU MUC: {header_info}\n")
        f.write("=" * 60 + "\n\n")
        for line in tree_lines:
            f.write(line + "\n")
        f.write("\n" + "=" * 60 + "\n")
        f.write(f"Tong cong: {len(tree_lines)} muc\n")


def count_stats(tree_lines):
    """Đếm thống kê"""
    folders = sum(1 for line in tree_lines if '📁' in line)
    files = len(tree_lines) - folders
    return folders, files


def main():
    print_header()
    
    # Nhập thư mục
    folder_input = input("Nhap duong dan thu muc (Enter de dung thu muc hien tai): ").strip('"')
    if not folder_input:
        folder_input = "."
    
    if not os.path.isdir(folder_input):
        print("❌ Thu muc khong ton tai!")
        return
    
    folder_path = Path(folder_input).resolve()
    
    # Tùy chọn
    ignore_input = input("\nCac thu muc/file can bo qua (cach nhau boi dau phay, Enter de mac dinh: node_modules, .git, __pycache__): ")
    if ignore_input.strip():
        ignore_list = [item.strip() for item in ignore_input.split(',')]
    else:
        ignore_list = ['node_modules', '.git', '__pycache__', '.vscode', '.idea', 'venv', 'env', 'dist', 'build']
    
    max_depth_input = input("Do sau toi da (Enter de khong gioi han): ").strip()
    max_depth = int(max_depth_input) if max_depth_input else None
    
    show_hidden_input = input("Hien thi file/folder an (bat dau bang .)? (y/N): ").strip().lower()
    show_hidden = show_hidden_input == 'y'
    
    # Tạo cây
    print(f"\n🌳 Dang tao cay thu muc...\n")
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
        print(f"\n... va {len(tree_lines) - 100} muc khac")
    
    # Thống kê
    folders, files = count_stats(tree_lines)
    print("\n" + "=" * 60)
    print(f"📊 Tong ket:")
    print(f"   - Thu muc: {folders}")
    print(f"   - File: {files}")
    print(f"   - Tong cong: {len(tree_lines)} muc")
    print("=" * 60)
    
    # Lưu ra file
    save_input = input("\nLuu ket qua ra file? (Y/n): ").strip().lower()
    if save_input != 'n':
        output_file = f"tree_{folder_path.name}.txt"
        save_tree_to_file(tree_lines, output_file, folder_path.name)
        print(f"\n✅ Da luu vao: {output_file}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Da huy!")
    except Exception as e:
        print(f"\n❌ Loi: {e}")

