#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: Đổi tên hàng loạt file theo pattern
"""

import os
import re
from pathlib import Path


def print_header():
    print("=" * 60)
    print("  TOOL ĐỔI TÊN HÀNG LOẠT FILE")
    print("=" * 60)
    print()


def rename_add_prefix(folder_path, prefix, file_extensions):
    """Thêm prefix vào đầu tên file"""
    count = 0
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            if not file_extensions or any(file.lower().endswith(ext) for ext in file_extensions):
                new_name = prefix + file
                new_path = os.path.join(folder_path, new_name)
                os.rename(file_path, new_path)
                print(f"✓ {file} → {new_name}")
                count += 1
    return count


def rename_add_suffix(folder_path, suffix, file_extensions):
    """Thêm suffix vào trước phần mở rộng"""
    count = 0
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            if not file_extensions or any(file.lower().endswith(ext) for ext in file_extensions):
                name, ext = os.path.splitext(file)
                new_name = name + suffix + ext
                new_path = os.path.join(folder_path, new_name)
                os.rename(file_path, new_path)
                print(f"✓ {file} → {new_name}")
                count += 1
    return count


def rename_replace_text(folder_path, old_text, new_text, file_extensions):
    """Thay thế text trong tên file"""
    count = 0
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            if not file_extensions or any(file.lower().endswith(ext) for ext in file_extensions):
                if old_text in file:
                    new_name = file.replace(old_text, new_text)
                    new_path = os.path.join(folder_path, new_name)
                    os.rename(file_path, new_path)
                    print(f"✓ {file} → {new_name}")
                    count += 1
    return count


def rename_sequential(folder_path, base_name, start_num, file_extensions):
    """Đổi tên file theo số thứ tự"""
    count = 0
    files = []
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            if not file_extensions or any(file.lower().endswith(ext) for ext in file_extensions):
                files.append(file)
    
    files.sort()  # Sắp xếp theo thứ tự
    
    for idx, file in enumerate(files, start=start_num):
        file_path = os.path.join(folder_path, file)
        ext = os.path.splitext(file)[1]
        new_name = f"{base_name}_{idx:03d}{ext}"
        new_path = os.path.join(folder_path, new_name)
        os.rename(file_path, new_path)
        print(f"✓ {file} → {new_name}")
        count += 1
    
    return count


def rename_change_extension(folder_path, old_ext, new_ext):
    """Đổi phần mở rộng file"""
    count = 0
    old_ext = old_ext.lower()
    if not old_ext.startswith('.'):
        old_ext = '.' + old_ext
    if not new_ext.startswith('.'):
        new_ext = '.' + new_ext
    
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path) and file.lower().endswith(old_ext):
            name = os.path.splitext(file)[0]
            new_name = name + new_ext
            new_path = os.path.join(folder_path, new_name)
            os.rename(file_path, new_path)
            print(f"✓ {file} → {new_name}")
            count += 1
    return count


def rename_to_lowercase(folder_path, file_extensions):
    """Chuyển tên file sang chữ thường"""
    count = 0
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            if not file_extensions or any(file.lower().endswith(ext) for ext in file_extensions):
                new_name = file.lower()
                if new_name != file:
                    new_path = os.path.join(folder_path, new_name)
                    os.rename(file_path, new_path)
                    print(f"✓ {file} → {new_name}")
                    count += 1
    return count


def rename_remove_spaces(folder_path, replacement, file_extensions):
    """Xóa hoặc thay thế khoảng trắng"""
    count = 0
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            if not file_extensions or any(file.lower().endswith(ext) for ext in file_extensions):
                if ' ' in file:
                    new_name = file.replace(' ', replacement)
                    new_path = os.path.join(folder_path, new_name)
                    os.rename(file_path, new_path)
                    print(f"✓ {file} → {new_name}")
                    count += 1
    return count


def main():
    print_header()
    
    # Nhập đường dẫn thư mục
    folder_input = input("Nhập đường dẫn thư mục chứa file: ").strip('"')
    if not folder_input or not os.path.isdir(folder_input):
        print("❌ Thư mục không tồn tại!")
        return
    
    # Hiển thị menu chức năng
    print("\n===== CHỌN CHỨC NĂNG =====")
    print("1. Thêm prefix (tiền tố) vào đầu tên file")
    print("2. Thêm suffix (hậu tố) vào cuối tên file")
    print("3. Thay thế text trong tên file")
    print("4. Đổi tên file theo số thứ tự")
    print("5. Đổi phần mở rộng file")
    print("6. Chuyển tất cả sang chữ thường")
    print("7. Xóa hoặc thay thế khoảng trắng")
    print("0. Thoát")
    
    choice = input("\nChọn chức năng (0-7): ").strip()
    
    if choice == "0":
        print("Thoát chương trình.")
        return
    
    # Hỏi loại file cần xử lý
    ext_input = input("\nChỉ xử lý file có đuôi (vd: .jpg .png - Enter để xử lý tất cả): ").strip()
    file_extensions = [ext.strip() for ext in ext_input.split()] if ext_input else []
    
    print(f"\n📂 Thư mục: {folder_input}")
    print("🔄 Bắt đầu đổi tên...\n")
    
    count = 0
    
    if choice == "1":
        prefix = input("Nhập prefix (tiền tố): ")
        count = rename_add_prefix(folder_input, prefix, file_extensions)
    
    elif choice == "2":
        suffix = input("Nhập suffix (hậu tố): ")
        count = rename_add_suffix(folder_input, suffix, file_extensions)
    
    elif choice == "3":
        old_text = input("Nhập text cần thay thế: ")
        new_text = input("Nhập text mới: ")
        count = rename_replace_text(folder_input, old_text, new_text, file_extensions)
    
    elif choice == "4":
        base_name = input("Nhập tên cơ sở (vd: image): ")
        start_num = int(input("Bắt đầu từ số (vd: 1): ") or "1")
        count = rename_sequential(folder_input, base_name, start_num, file_extensions)
    
    elif choice == "5":
        old_ext = input("Nhập đuôi cũ (vd: txt): ")
        new_ext = input("Nhập đuôi mới (vd: md): ")
        count = rename_change_extension(folder_input, old_ext, new_ext)
    
    elif choice == "6":
        count = rename_to_lowercase(folder_input, file_extensions)
    
    elif choice == "7":
        replacement = input("Thay khoảng trắng bằng gì? (vd: _ hoặc - , Enter để xóa): ")
        count = rename_remove_spaces(folder_input, replacement, file_extensions)
    
    else:
        print("❌ Lựa chọn không hợp lệ!")
        return
    
    print(f"\n✅ Hoàn thành! Đã đổi tên {count} file.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Đã hủy!")
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")

