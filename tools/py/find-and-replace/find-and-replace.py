#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: Tìm và thay thế text trong nhiều file
"""

import os
import re
from pathlib import Path


def print_header():
    print("=" * 60)
    print("  TOOL TÌM VÀ THAY THẾ TEXT")
    print("=" * 60)
    print()


def find_in_file(file_path, search_text, case_sensitive=True, use_regex=False):
    """
    Tìm text trong file
    
    Returns:
        list: Danh sách (line_number, line_content) chứa text tìm thấy
    """
    matches = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                if use_regex:
                    flags = 0 if case_sensitive else re.IGNORECASE
                    if re.search(search_text, line, flags):
                        matches.append((line_num, line.rstrip()))
                else:
                    line_to_check = line if case_sensitive else line.lower()
                    text_to_find = search_text if case_sensitive else search_text.lower()
                    if text_to_find in line_to_check:
                        matches.append((line_num, line.rstrip()))
    except Exception as e:
        pass
    
    return matches


def replace_in_file(file_path, search_text, replace_text, case_sensitive=True, use_regex=False):
    """
    Thay thế text trong file
    
    Returns:
        int: Số lần thay thế
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original_content = content
        
        if use_regex:
            flags = 0 if case_sensitive else re.IGNORECASE
            content, count = re.subn(search_text, replace_text, content, flags=flags)
        else:
            if case_sensitive:
                count = content.count(search_text)
                content = content.replace(search_text, replace_text)
            else:
                # Case insensitive replace (không dùng regex)
                count = content.lower().count(search_text.lower())
                pattern = re.compile(re.escape(search_text), re.IGNORECASE)
                content = pattern.sub(replace_text, content)
        
        if count > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return count
        
    except Exception as e:
        print(f"   ❌ Lỗi: {e}")
        return 0


def get_files_to_process(folder_path, file_extensions, recursive=True):
    """Lấy danh sách file cần xử lý"""
    files_list = []
    
    if recursive:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if not file_extensions or any(file.lower().endswith(ext) for ext in file_extensions):
                    files_list.append(os.path.join(root, file))
    else:
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                if not file_extensions or any(file.lower().endswith(ext) for ext in file_extensions):
                    files_list.append(file_path)
    
    return files_list


def find_mode(folder_path, search_text, file_extensions, case_sensitive, use_regex, recursive):
    """Chế độ chỉ tìm (không thay thế)"""
    print(f"\n🔍 Đang tìm kiếm...\n")
    
    files_list = get_files_to_process(folder_path, file_extensions, recursive)
    
    total_matches = 0
    files_with_matches = 0
    
    for file_path in files_list:
        matches = find_in_file(file_path, search_text, case_sensitive, use_regex)
        if matches:
            files_with_matches += 1
            total_matches += len(matches)
            print(f"\n📄 {file_path}")
            for line_num, line_content in matches[:5]:  # Hiển thị tối đa 5 dòng đầu
                print(f"   Line {line_num}: {line_content[:80]}...")
            if len(matches) > 5:
                print(f"   ... và {len(matches) - 5} kết quả khác")
    
    print(f"\n{'='*60}")
    print(f"✅ Tìm thấy {total_matches} kết quả trong {files_with_matches} file")
    print(f"{'='*60}")


def replace_mode(folder_path, search_text, replace_text, file_extensions, case_sensitive, use_regex, recursive):
    """Chế độ thay thế"""
    print(f"\n🔄 Đang thay thế...\n")
    
    files_list = get_files_to_process(folder_path, file_extensions, recursive)
    
    total_replacements = 0
    files_modified = 0
    
    for file_path in files_list:
        count = replace_in_file(file_path, search_text, replace_text, case_sensitive, use_regex)
        if count > 0:
            files_modified += 1
            total_replacements += count
            print(f"✓ {file_path} - Thay thế {count} lần")
    
    print(f"\n{'='*60}")
    print(f"✅ Đã thay thế {total_replacements} lần trong {files_modified} file")
    print(f"{'='*60}")


def main():
    print_header()
    
    # Nhập thư mục
    folder_input = input("Nhập đường dẫn thư mục: ").strip('"')
    if not folder_input or not os.path.isdir(folder_input):
        print("❌ Thư mục không tồn tại!")
        return
    
    # Chế độ đệ quy
    recursive_input = input("Tìm kiếm trong tất cả thư mục con? (Y/n, mặc định Yes): ").strip().lower()
    recursive = recursive_input != 'n'
    
    # Loại file
    ext_input = input("Chỉ xử lý file có đuôi (vd: .txt .py .js - Enter để xử lý tất cả): ").strip()
    file_extensions = [ext.strip() for ext in ext_input.split()] if ext_input else []
    
    # Text cần tìm
    search_text = input("\nNhập text cần tìm: ")
    if not search_text:
        print("❌ Bạn phải nhập text cần tìm!")
        return
    
    # Tùy chọn
    case_input = input("Phân biệt chữ hoa/thường? (y/N, mặc định No): ").strip().lower()
    case_sensitive = case_input == 'y'
    
    regex_input = input("Sử dụng Regular Expression? (y/N, mặc định No): ").strip().lower()
    use_regex = regex_input == 'y'
    
    # Chế độ: tìm hay thay thế
    print("\n===== CHẾ ĐỘ =====")
    print("1. Chỉ tìm kiếm (không thay đổi file)")
    print("2. Tìm và thay thế")
    
    mode = input("\nChọn chế độ (1-2): ").strip()
    
    if mode == "1":
        find_mode(folder_path=folder_input, 
                 search_text=search_text,
                 file_extensions=file_extensions,
                 case_sensitive=case_sensitive,
                 use_regex=use_regex,
                 recursive=recursive)
    
    elif mode == "2":
        replace_text = input("\nNhập text thay thế: ")
        
        # Xác nhận
        print(f"\n⚠️  CẢNH BÁO: Bạn sắp thay thế trong nhiều file!")
        print(f"   Tìm: '{search_text}'")
        print(f"   Thay bằng: '{replace_text}'")
        confirm = input("\nXác nhận thực hiện? (YES để xác nhận): ")
        
        if confirm == "YES":
            replace_mode(folder_path=folder_input,
                        search_text=search_text,
                        replace_text=replace_text,
                        file_extensions=file_extensions,
                        case_sensitive=case_sensitive,
                        use_regex=use_regex,
                        recursive=recursive)
        else:
            print("❌ Đã hủy thao tác.")
    
    else:
        print("❌ Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Đã hủy!")
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")

