#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: Dọn dẹp file tạm, cache, file rác
"""

import os
import shutil
from pathlib import Path


def print_header():
    print("=" * 60)
    print("  TOOL DỌN DẸP FILE TẠM VÀ CACHE")
    print("=" * 60)
    print()


def format_size(size_bytes):
    """Format dung lượng"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0


def get_size(path):
    """Tính dung lượng file hoặc folder"""
    if os.path.isfile(path):
        return os.path.getsize(path)
    
    total = 0
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                if os.path.exists(file_path):
                    total += os.path.getsize(file_path)
    except Exception:
        pass
    return total


def find_temp_files(directory):
    """Tìm file tạm"""
    temp_patterns = [
        '.tmp', '.temp', '.log', '.bak', '.old', '.cache',
        '~', '.swp', '.swo', '.DS_Store', 'Thumbs.db', 'desktop.ini'
    ]
    
    temp_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(pattern) or file == pattern for pattern in temp_patterns):
                file_path = os.path.join(root, file)
                try:
                    size = os.path.getsize(file_path)
                    temp_files.append((file_path, size))
                except Exception:
                    pass
    
    return temp_files


def find_cache_folders(directory):
    """Tìm thư mục cache"""
    cache_names = [
        '__pycache__', '.pytest_cache', '.mypy_cache', 
        'node_modules', '.next', '.nuxt',
        'vendor', 'composer.lock',
        '.cache', 'cache', 'Cache',
        'temp', 'tmp'
    ]
    
    cache_folders = []
    
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            if dir_name in cache_names:
                folder_path = os.path.join(root, dir_name)
                try:
                    size = get_size(folder_path)
                    cache_folders.append((folder_path, size))
                except Exception:
                    pass
    
    return cache_folders


def find_large_files(directory, min_size_mb=10):
    """Tìm file lớn"""
    large_files = []
    min_size_bytes = min_size_mb * 1024 * 1024
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)
                if size >= min_size_bytes:
                    large_files.append((file_path, size))
            except Exception:
                pass
    
    return large_files


def find_empty_folders(directory):
    """Tìm thư mục rỗng"""
    empty_folders = []
    
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir_name in dirs:
            folder_path = os.path.join(root, dir_name)
            try:
                if not os.listdir(folder_path):
                    empty_folders.append(folder_path)
            except Exception:
                pass
    
    return empty_folders


def delete_items(items, item_type="file"):
    """Xóa danh sách file/folder"""
    deleted_count = 0
    freed_space = 0
    
    for item_path, size in items:
        try:
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
            
            print(f"✓ Xóa: {item_path} ({format_size(size)})")
            deleted_count += 1
            freed_space += size
        except Exception as e:
            print(f"✗ Lỗi khi xóa {item_path}: {e}")
    
    return deleted_count, freed_space


def main():
    print_header()
    
    # Nhập thư mục
    folder_input = input("Nhập đường dẫn thư mục cần dọn dẹp (Enter để dùng thư mục hiện tại): ").strip('"')
    if not folder_input:
        folder_input = "."
    
    if not os.path.isdir(folder_input):
        print("❌ Thư mục không tồn tại!")
        return
    
    folder_path = Path(folder_input).resolve()
    
    print(f"\n📂 Thư mục: {folder_path}")
    print("\n===== TÌM KIẾM FILE RÁC =====")
    
    # Menu chọn
    print("\n1. File tạm (.tmp, .log, .bak, ...)")
    print("2. Thư mục cache (__pycache__, node_modules, ...)")
    print("3. File lớn (>10MB)")
    print("4. Thư mục rỗng")
    print("5. Tất cả các loại trên")
    
    choice = input("\nChọn loại cần dọn dẹp (1-5): ").strip()
    
    items_to_clean = []
    
    print(f"\n🔍 Đang quét...\n")
    
    if choice in ["1", "5"]:
        temp_files = find_temp_files(folder_path)
        items_to_clean.extend(temp_files)
        total_size = sum(size for _, size in temp_files)
        print(f"📄 Tìm thấy {len(temp_files)} file tạm ({format_size(total_size)})")
    
    if choice in ["2", "5"]:
        cache_folders = find_cache_folders(folder_path)
        items_to_clean.extend(cache_folders)
        total_size = sum(size for _, size in cache_folders)
        print(f"📁 Tìm thấy {len(cache_folders)} thư mục cache ({format_size(total_size)})")
    
    if choice in ["3", "5"]:
        min_size = input("Kích thước tối thiểu (MB, mặc định 10): ").strip()
        min_size = int(min_size) if min_size else 10
        large_files = find_large_files(folder_path, min_size)
        items_to_clean.extend(large_files)
        total_size = sum(size for _, size in large_files)
        print(f"💾 Tìm thấy {len(large_files)} file lớn (>{min_size}MB) ({format_size(total_size)})")
    
    if choice in ["4", "5"]:
        empty_folders = find_empty_folders(folder_path)
        items_to_clean.extend([(path, 0) for path in empty_folders])
        print(f"📂 Tìm thấy {len(empty_folders)} thư mục rỗng")
    
    if not items_to_clean:
        print("\n✅ Không tìm thấy gì cần dọn dẹp!")
        return
    
    # Tính tổng
    total_items = len(items_to_clean)
    total_size = sum(size for _, size in items_to_clean)
    
    print(f"\n{'='*60}")
    print(f"📊 Tổng kết:")
    print(f"   - Số lượng: {total_items} mục")
    print(f"   - Dung lượng: {format_size(total_size)}")
    print(f"{'='*60}")
    
    # Hiển thị danh sách (10 mục đầu)
    print(f"\n📋 Danh sách (10 mục đầu):")
    for item_path, size in items_to_clean[:10]:
        print(f"   - {item_path} ({format_size(size)})")
    
    if len(items_to_clean) > 10:
        print(f"   ... và {len(items_to_clean) - 10} mục khác")
    
    # Xác nhận xóa
    print(f"\n⚠️  CẢNH BÁO: Bạn sắp xóa {total_items} mục!")
    confirm = input("\nXác nhận xóa? (YES để xác nhận): ")
    
    if confirm == "YES":
        print(f"\n🗑️  Đang xóa...\n")
        deleted_count, freed_space = delete_items(items_to_clean)
        
        print(f"\n{'='*60}")
        print(f"✅ Hoàn thành!")
        print(f"   - Đã xóa: {deleted_count}/{total_items} mục")
        print(f"   - Giải phóng: {format_size(freed_space)}")
        print(f"{'='*60}")
    else:
        print("❌ Đã hủy.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Đã hủy!")
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")

