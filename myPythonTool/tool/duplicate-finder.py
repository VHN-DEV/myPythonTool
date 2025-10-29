#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: Tìm file trùng lặp dựa trên hash (MD5/SHA256)
"""

import os
import hashlib
from pathlib import Path
from collections import defaultdict


def print_header():
    print("=" * 60)
    print("  TOOL TIM FILE TRUNG LAP")
    print("=" * 60)
    print()


def format_size(size_bytes):
    """Format dung lượng"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0


def get_file_hash(file_path, hash_algo='md5', chunk_size=8192):
    """
    Tính hash của file
    
    Args:
        file_path: Đường dẫn file
        hash_algo: Thuật toán hash (md5, sha1, sha256)
        chunk_size: Kích thước chunk đọc file
    
    Returns:
        str: Hash string
    """
    if hash_algo == 'md5':
        hasher = hashlib.md5()
    elif hash_algo == 'sha1':
        hasher = hashlib.sha1()
    elif hash_algo == 'sha256':
        hasher = hashlib.sha256()
    else:
        hasher = hashlib.md5()
    
    try:
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        return None


def find_duplicates_by_hash(folder_path, recursive=True, min_size=0, hash_algo='md5'):
    """
    Tìm file trùng lặp bằng hash
    
    Returns:
        dict: {hash: [file_paths]}
    """
    hash_dict = defaultdict(list)
    file_count = 0
    
    print("🔍 Dang quet file va tinh hash...\n")
    
    if recursive:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    size = os.path.getsize(file_path)
                    
                    # Bỏ qua file nhỏ hơn min_size
                    if size < min_size:
                        continue
                    
                    file_count += 1
                    if file_count % 50 == 0:
                        print(f"   Da quet {file_count} file...", end='\r')
                    
                    file_hash = get_file_hash(file_path, hash_algo)
                    if file_hash:
                        hash_dict[file_hash].append((file_path, size))
                
                except Exception as e:
                    pass
    else:
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                try:
                    size = os.path.getsize(file_path)
                    
                    if size < min_size:
                        continue
                    
                    file_count += 1
                    if file_count % 50 == 0:
                        print(f"   Da quet {file_count} file...", end='\r')
                    
                    file_hash = get_file_hash(file_path, hash_algo)
                    if file_hash:
                        hash_dict[file_hash].append((file_path, size))
                
                except Exception as e:
                    pass
    
    print(f"   Da quet {file_count} file.       ")
    
    # Lọc chỉ lấy hash có nhiều hơn 1 file (trùng lặp)
    duplicates = {h: files for h, files in hash_dict.items() if len(files) > 1}
    
    return duplicates


def find_duplicates_by_size(folder_path, recursive=True, min_size=0):
    """
    Tìm file trùng lặp nhanh bằng size (không chính xác 100%)
    """
    size_dict = defaultdict(list)
    file_count = 0
    
    print("🔍 Dang quet file theo kich thuoc...\n")
    
    if recursive:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    size = os.path.getsize(file_path)
                    
                    if size < min_size:
                        continue
                    
                    file_count += 1
                    if file_count % 100 == 0:
                        print(f"   Da quet {file_count} file...", end='\r')
                    
                    size_dict[size].append(file_path)
                
                except Exception:
                    pass
    else:
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                try:
                    size = os.path.getsize(file_path)
                    
                    if size < min_size:
                        continue
                    
                    file_count += 1
                    size_dict[size].append(file_path)
                
                except Exception:
                    pass
    
    print(f"   Da quet {file_count} file.       ")
    
    # Lọc chỉ lấy size có nhiều hơn 1 file
    duplicates = {s: files for s, files in size_dict.items() if len(files) > 1}
    
    return duplicates


def display_duplicates(duplicates, by_hash=True):
    """Hiển thị danh sách file trùng lặp"""
    if not duplicates:
        print("\n✅ Khong tim thay file trung lap!")
        return 0, 0
    
    duplicate_groups = len(duplicates)
    total_duplicates = sum(len(files) - 1 for files in duplicates.values())
    wasted_space = 0
    
    print(f"\n{'='*60}")
    print(f"📊 Tim thay {duplicate_groups} nhom file trung lap")
    print(f"{'='*60}\n")
    
    for idx, (key, files) in enumerate(duplicates.items(), 1):
        if by_hash:
            # files là list của tuple (path, size)
            file_size = files[0][1]
            file_paths = [f[0] for f in files]
        else:
            # files là list của path, key là size
            file_size = key
            file_paths = files
        
        group_waste = file_size * (len(file_paths) - 1)
        wasted_space += group_waste
        
        print(f"Nhom {idx}: {len(file_paths)} file ({format_size(file_size)}) - Lang phi: {format_size(group_waste)}")
        
        if by_hash:
            print(f"   Hash: {key[:16]}...")
        
        for file_path in file_paths:
            print(f"   - {file_path}")
        
        print()
        
        # Chỉ hiển thị 10 nhóm đầu
        if idx >= 10 and len(duplicates) > 10:
            remaining = len(duplicates) - 10
            print(f"... va {remaining} nhom khac")
            break
    
    return total_duplicates, wasted_space


def save_duplicates_report(duplicates, output_file, by_hash=True):
    """Lưu báo cáo file trùng lặp"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("  BAO CAO FILE TRUNG LAP\n")
        f.write("=" * 60 + "\n\n")
        
        duplicate_groups = len(duplicates)
        total_duplicates = sum(len(files) - 1 for files in duplicates.values())
        
        f.write(f"Tong so nhom trung lap: {duplicate_groups}\n")
        f.write(f"Tong so file trung lap: {total_duplicates}\n\n")
        
        for idx, (key, files) in enumerate(duplicates.items(), 1):
            if by_hash:
                file_size = files[0][1]
                file_paths = [f[0] for f in files]
            else:
                file_size = key
                file_paths = files
            
            group_waste = file_size * (len(file_paths) - 1)
            
            f.write(f"\nNhom {idx}: {len(file_paths)} file ({format_size(file_size)})\n")
            if by_hash:
                f.write(f"Hash: {key}\n")
            
            for file_path in file_paths:
                f.write(f"  - {file_path}\n")


def delete_duplicates_interactive(duplicates, by_hash=True):
    """Xóa file trùng lặp với tương tác"""
    print("\n===== CHE DO XOA TRUNG LAP =====")
    print("1. Giu file dau tien, xoa cac file con lai")
    print("2. Chon thu cong tung file")
    print("0. Khong xoa")
    
    choice = input("\nChon (0-2): ").strip()
    
    if choice == "0":
        return
    
    elif choice == "1":
        files_to_delete = []
        
        for key, files in duplicates.items():
            if by_hash:
                file_paths = [f[0] for f in files]
            else:
                file_paths = files
            
            # Giữ file đầu tiên, xóa các file còn lại
            files_to_delete.extend(file_paths[1:])
        
        print(f"\n⚠️  CANH BAO: Ban sap xoa {len(files_to_delete)} file trung lap!")
        confirm = input("Xac nhan? (YES de xac nhan): ")
        
        if confirm == "YES":
            deleted = 0
            for file_path in files_to_delete:
                try:
                    os.remove(file_path)
                    print(f"✓ Xoa: {file_path}")
                    deleted += 1
                except Exception as e:
                    print(f"✗ Loi: {file_path} - {e}")
            
            print(f"\n✅ Da xoa {deleted}/{len(files_to_delete)} file")
        else:
            print("❌ Da huy")
    
    elif choice == "2":
        print("\n(Chuc nang nay se duoc them vao phien ban sau)")


def main():
    print_header()
    
    # Nhập thư mục
    folder_input = input("Nhap duong dan thu muc: ").strip('"')
    if not folder_input or not os.path.isdir(folder_input):
        print("❌ Thu muc khong ton tai!")
        return
    
    folder_path = Path(folder_input).resolve()
    
    # Tùy chọn
    recursive_input = input("Tim trong tat ca thu muc con? (Y/n): ").strip().lower()
    recursive = recursive_input != 'n'
    
    min_size_input = input("Kich thuoc file toi thieu (KB, Enter de bo qua): ").strip()
    min_size = int(min_size_input) * 1024 if min_size_input else 0
    
    # Chọn phương pháp
    print("\n===== PHUONG PHAP TIM =====")
    print("1. Theo hash (MD5) - Chinh xac nhung cham")
    print("2. Theo hash (SHA256) - Chinh xac hon MD5")
    print("3. Theo kich thuoc - Nhanh nhung khong chinh xac")
    
    method = input("\nChon phuong phap (1-3): ").strip()
    
    if method == "1":
        duplicates = find_duplicates_by_hash(folder_path, recursive, min_size, 'md5')
        total_duplicates, wasted_space = display_duplicates(duplicates, by_hash=True)
        
        if duplicates:
            print(f"{'='*60}")
            print(f"💾 Tong dung luong lang phi: {format_size(wasted_space)}")
            print(f"{'='*60}")
    
    elif method == "2":
        duplicates = find_duplicates_by_hash(folder_path, recursive, min_size, 'sha256')
        total_duplicates, wasted_space = display_duplicates(duplicates, by_hash=True)
        
        if duplicates:
            print(f"{'='*60}")
            print(f"💾 Tong dung luong lang phi: {format_size(wasted_space)}")
            print(f"{'='*60}")
    
    elif method == "3":
        duplicates = find_duplicates_by_size(folder_path, recursive, min_size)
        total_duplicates, wasted_space = display_duplicates(duplicates, by_hash=False)
        
        if duplicates:
            print(f"{'='*60}")
            print(f"💾 Uoc tinh dung luong lang phi: {format_size(wasted_space)}")
            print(f"⚠️  Luu y: Phuong phap nay chi dua tren kich thuoc, co the khong chinh xac 100%")
            print(f"{'='*60}")
    
    else:
        print("❌ Lua chon khong hop le!")
        return
    
    if not duplicates:
        return
    
    # Lưu báo cáo
    save_input = input("\nLuu bao cao ra file? (y/N): ").strip().lower()
    if save_input == 'y':
        output_file = "duplicate_report.txt"
        save_duplicates_report(duplicates, output_file, by_hash=(method in ["1", "2"]))
        print(f"✅ Da luu bao cao: {output_file}")
    
    # Xóa file trùng lặp
    delete_input = input("\nXoa file trung lap? (y/N): ").strip().lower()
    if delete_input == 'y':
        delete_duplicates_interactive(duplicates, by_hash=(method in ["1", "2"]))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Da huy!")
    except Exception as e:
        print(f"\n❌ Loi: {e}")

