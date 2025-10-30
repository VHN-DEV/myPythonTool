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
    print("  TOOL DOI TEN HANG LOAT FILE")
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
    folder_input = input("Nhap duong dan thu muc chua file: ").strip('"')
    if not folder_input or not os.path.isdir(folder_input):
        print("❌ Thu muc khong ton tai!")
        return
    
    # Hiển thị menu chức năng
    print("\n===== CHON CHUC NANG =====")
    print("1. Them prefix (tien to) vao dau ten file")
    print("2. Them suffix (hau to) vao cuoi ten file")
    print("3. Thay the text trong ten file")
    print("4. Doi ten file theo so thu tu")
    print("5. Doi phan mo rong file")
    print("6. Chuyen tat ca sang chu thuong")
    print("7. Xoa hoac thay the khoang trang")
    print("0. Thoat")
    
    choice = input("\nChon chuc nang (0-7): ").strip()
    
    if choice == "0":
        print("Thoat chuong trinh.")
        return
    
    # Hỏi loại file cần xử lý
    ext_input = input("\nChi xu ly file co duoi (vd: .jpg .png - Enter de xu ly tat ca): ").strip()
    file_extensions = [ext.strip() for ext in ext_input.split()] if ext_input else []
    
    print(f"\n📂 Thu muc: {folder_input}")
    print("🔄 Bat dau doi ten...\n")
    
    count = 0
    
    if choice == "1":
        prefix = input("Nhap prefix (tien to): ")
        count = rename_add_prefix(folder_input, prefix, file_extensions)
    
    elif choice == "2":
        suffix = input("Nhap suffix (hau to): ")
        count = rename_add_suffix(folder_input, suffix, file_extensions)
    
    elif choice == "3":
        old_text = input("Nhap text can thay the: ")
        new_text = input("Nhap text moi: ")
        count = rename_replace_text(folder_input, old_text, new_text, file_extensions)
    
    elif choice == "4":
        base_name = input("Nhap ten co so (vd: image): ")
        start_num = int(input("Bat dau tu so (vd: 1): ") or "1")
        count = rename_sequential(folder_input, base_name, start_num, file_extensions)
    
    elif choice == "5":
        old_ext = input("Nhap duoi cu (vd: txt): ")
        new_ext = input("Nhap duoi moi (vd: md): ")
        count = rename_change_extension(folder_input, old_ext, new_ext)
    
    elif choice == "6":
        count = rename_to_lowercase(folder_input, file_extensions)
    
    elif choice == "7":
        replacement = input("Thay khoang trang bang gi? (vd: _ hoac - , Enter de xoa): ")
        count = rename_remove_spaces(folder_input, replacement, file_extensions)
    
    else:
        print("❌ Lua chon khong hop le!")
        return
    
    print(f"\n✅ Hoan thanh! Da doi ten {count} file.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Da huy!")
    except Exception as e:
        print(f"\n❌ Loi: {e}")

