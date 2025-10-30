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
    print("  TOOL DON DEP FILE TAM VA CACHE")
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
            
            print(f"✓ Xoa: {item_path} ({format_size(size)})")
            deleted_count += 1
            freed_space += size
        except Exception as e:
            print(f"✗ Loi khi xoa {item_path}: {e}")
    
    return deleted_count, freed_space


def main():
    print_header()
    
    # Nhập thư mục
    folder_input = input("Nhap duong dan thu muc can don dep (Enter de dung thu muc hien tai): ").strip('"')
    if not folder_input:
        folder_input = "."
    
    if not os.path.isdir(folder_input):
        print("❌ Thu muc khong ton tai!")
        return
    
    folder_path = Path(folder_input).resolve()
    
    print(f"\n📂 Thu muc: {folder_path}")
    print("\n===== TIM KIEM FILE RAC =====")
    
    # Menu chọn
    print("\n1. File tam (.tmp, .log, .bak, ...)")
    print("2. Thu muc cache (__pycache__, node_modules, ...)")
    print("3. File lon (>10MB)")
    print("4. Thu muc rong")
    print("5. Tat ca cac loai tren")
    
    choice = input("\nChon loai can don dep (1-5): ").strip()
    
    items_to_clean = []
    
    print(f"\n🔍 Dang quet...\n")
    
    if choice in ["1", "5"]:
        temp_files = find_temp_files(folder_path)
        items_to_clean.extend(temp_files)
        total_size = sum(size for _, size in temp_files)
        print(f"📄 Tim thay {len(temp_files)} file tam ({format_size(total_size)})")
    
    if choice in ["2", "5"]:
        cache_folders = find_cache_folders(folder_path)
        items_to_clean.extend(cache_folders)
        total_size = sum(size for _, size in cache_folders)
        print(f"📁 Tim thay {len(cache_folders)} thu muc cache ({format_size(total_size)})")
    
    if choice in ["3", "5"]:
        min_size = input("Kich thuoc toi thieu (MB, mac dinh 10): ").strip()
        min_size = int(min_size) if min_size else 10
        large_files = find_large_files(folder_path, min_size)
        items_to_clean.extend(large_files)
        total_size = sum(size for _, size in large_files)
        print(f"💾 Tim thay {len(large_files)} file lon (>{min_size}MB) ({format_size(total_size)})")
    
    if choice in ["4", "5"]:
        empty_folders = find_empty_folders(folder_path)
        items_to_clean.extend([(path, 0) for path in empty_folders])
        print(f"📂 Tim thay {len(empty_folders)} thu muc rong")
    
    if not items_to_clean:
        print("\n✅ Khong tim thay gi can don dep!")
        return
    
    # Tính tổng
    total_items = len(items_to_clean)
    total_size = sum(size for _, size in items_to_clean)
    
    print(f"\n{'='*60}")
    print(f"📊 Tong ket:")
    print(f"   - So luong: {total_items} muc")
    print(f"   - Dung luong: {format_size(total_size)}")
    print(f"{'='*60}")
    
    # Hiển thị danh sách (10 mục đầu)
    print(f"\n📋 Danh sach (10 muc dau):")
    for item_path, size in items_to_clean[:10]:
        print(f"   - {item_path} ({format_size(size)})")
    
    if len(items_to_clean) > 10:
        print(f"   ... va {len(items_to_clean) - 10} muc khac")
    
    # Xác nhận xóa
    print(f"\n⚠️  CANH BAO: Ban sap xoa {total_items} muc!")
    confirm = input("\nXac nhan xoa? (YES de xac nhan): ")
    
    if confirm == "YES":
        print(f"\n🗑️  Dang xoa...\n")
        deleted_count, freed_space = delete_items(items_to_clean)
        
        print(f"\n{'='*60}")
        print(f"✅ Hoan thanh!")
        print(f"   - Da xoa: {deleted_count}/{total_items} muc")
        print(f"   - Giai phong: {format_size(freed_space)}")
        print(f"{'='*60}")
    else:
        print("❌ Da huy.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Da huy!")
    except Exception as e:
        print(f"\n❌ Loi: {e}")

