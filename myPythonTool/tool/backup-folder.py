#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: Backup thư mục với timestamp
"""

import os
import shutil
import datetime
from pathlib import Path


def print_header():
    print("=" * 60)
    print("  TOOL BACKUP THU MUC")
    print("=" * 60)
    print()


def get_folder_size(folder_path):
    """Tính dung lượng thư mục"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.exists(file_path):
                total_size += os.path.getsize(file_path)
    return total_size


def format_size(size_bytes):
    """Format dung lượng dễ đọc"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0


def backup_folder(source_folder, backup_location, compression_format='zip'):
    """
    Backup thư mục với timestamp
    
    Args:
        source_folder: Thư mục nguồn cần backup
        backup_location: Vị trí lưu backup
        compression_format: Định dạng nén (zip, tar, gztar, bztar, xztar)
    """
    try:
        source_path = Path(source_folder).resolve()
        
        if not source_path.exists():
            print(f"❌ Thu muc nguon khong ton tai: {source_folder}")
            return False
        
        # Tạo tên backup với timestamp
        folder_name = source_path.name
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{folder_name}_backup_{timestamp}"
        
        # Tạo thư mục backup nếu chưa có
        backup_path = Path(backup_location)
        backup_path.mkdir(parents=True, exist_ok=True)
        
        # Đường dẫn file backup (không bao gồm extension, shutil sẽ tự thêm)
        backup_file_base = backup_path / backup_name
        
        # Tính dung lượng
        print(f"📊 Dang tinh dung luong...")
        total_size = get_folder_size(source_path)
        print(f"   Dung luong: {format_size(total_size)}")
        
        # Backup
        print(f"📦 Dang nen va backup...")
        backup_file = shutil.make_archive(
            str(backup_file_base),
            compression_format,
            source_path.parent,
            source_path.name
        )
        
        backup_size = os.path.getsize(backup_file)
        
        print(f"\n✅ Backup thanh cong!")
        print(f"   📁 Thu muc nguon: {source_path}")
        print(f"   💾 File backup: {backup_file}")
        print(f"   📊 Kich thuoc goc: {format_size(total_size)}")
        print(f"   📊 Kich thuoc nen: {format_size(backup_size)}")
        print(f"   💯 Ty le nen: {backup_size/total_size*100:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Loi khi backup: {e}")
        return False


def backup_with_exclude(source_folder, backup_location, exclude_patterns):
    """
    Backup thư mục có loại trừ một số file/folder
    
    Args:
        source_folder: Thư mục nguồn
        backup_location: Vị trí backup
        exclude_patterns: Danh sách pattern cần loại trừ
    """
    try:
        source_path = Path(source_folder).resolve()
        
        if not source_path.exists():
            print(f"❌ Thu muc nguon khong ton tai: {source_folder}")
            return False
        
        folder_name = source_path.name
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{folder_name}_backup_{timestamp}"
        
        backup_path = Path(backup_location)
        backup_path.mkdir(parents=True, exist_ok=True)
        
        temp_folder = backup_path / f"temp_{backup_name}"
        
        # Copy với ignore
        def ignore_patterns(directory, contents):
            ignored = []
            for pattern in exclude_patterns:
                for item in contents:
                    if pattern in item:
                        ignored.append(item)
            return set(ignored)
        
        print(f"📦 Dang copy file...")
        shutil.copytree(source_path, temp_folder, ignore=ignore_patterns)
        
        print(f"📦 Dang nen...")
        backup_file = shutil.make_archive(
            str(backup_path / backup_name),
            'zip',
            temp_folder.parent,
            temp_folder.name
        )
        
        # Xóa thư mục tạm
        shutil.rmtree(temp_folder)
        
        backup_size = os.path.getsize(backup_file)
        
        print(f"\n✅ Backup thanh cong!")
        print(f"   💾 File backup: {backup_file}")
        print(f"   📊 Kich thuoc: {format_size(backup_size)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Loi khi backup: {e}")
        return False


def main():
    print_header()
    
    # Nhập thư mục cần backup
    source_input = input("Nhap duong dan thu muc can backup: ").strip('"')
    if not source_input or not os.path.isdir(source_input):
        print("❌ Thu muc khong ton tai!")
        return
    
    # Nhập vị trí lưu backup
    backup_input = input("Nhap vi tri luu backup (Enter de luu tai thu muc hien tai): ").strip('"')
    if not backup_input:
        backup_input = "."
    
    # Chọn chế độ
    print("\n===== CHE DO BACKUP =====")
    print("1. Backup toan bo")
    print("2. Backup co loai tru (exclude)")
    
    mode = input("\nChon che do (1-2): ").strip()
    
    if mode == "1":
        # Chọn định dạng nén
        print("\n===== DINH DANG NEN =====")
        print("1. ZIP (pho bien, nhanh)")
        print("2. TAR")
        print("3. TAR.GZ (nen cao hon)")
        
        format_choice = input("\nChon dinh dang (1-3, Enter de mac dinh ZIP): ").strip()
        
        format_map = {
            "1": "zip",
            "2": "tar",
            "3": "gztar",
            "": "zip"
        }
        
        compression = format_map.get(format_choice, "zip")
        
        print(f"\n🚀 Bat dau backup...\n")
        backup_folder(source_input, backup_input, compression)
    
    elif mode == "2":
        exclude_input = input("\nNhap cac pattern can loai tru (cach nhau boi dau phay, vd: node_modules,.git,__pycache__): ")
        exclude_patterns = [p.strip() for p in exclude_input.split(',') if p.strip()]
        
        if exclude_patterns:
            print(f"\n🚫 Loai tru: {', '.join(exclude_patterns)}")
        
        print(f"\n🚀 Bat dau backup...\n")
        backup_with_exclude(source_input, backup_input, exclude_patterns)
    
    else:
        print("❌ Lua chon khong hop le!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Da huy!")
    except Exception as e:
        print(f"\n❌ Loi: {e}")

