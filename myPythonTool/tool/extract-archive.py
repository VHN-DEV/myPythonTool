#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: Giải nén nhiều file nén cùng lúc
"""

import os
import zipfile
import tarfile
import shutil
from pathlib import Path


def print_header():
    print("=" * 60)
    print("  TOOL GIAI NEN FILE")
    print("=" * 60)
    print()


def format_size(size_bytes):
    """Format dung lượng"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0


def extract_zip(zip_path, extract_to):
    """Giải nén file ZIP"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        return True, None
    except Exception as e:
        return False, str(e)


def extract_tar(tar_path, extract_to):
    """Giải nén file TAR (tar, tar.gz, tar.bz2, tar.xz)"""
    try:
        with tarfile.open(tar_path, 'r:*') as tar_ref:
            tar_ref.extractall(extract_to)
        return True, None
    except Exception as e:
        return False, str(e)


def extract_archive(archive_path, extract_to):
    """
    Giải nén file dựa vào extension
    
    Returns:
        tuple: (success, error_message, extracted_size)
    """
    archive_path = Path(archive_path)
    extract_to = Path(extract_to)
    
    # Tạo thư mục đích
    extract_to.mkdir(parents=True, exist_ok=True)
    
    # Xác định loại file
    archive_ext = archive_path.suffix.lower()
    
    success = False
    error = None
    
    if archive_ext == '.zip':
        success, error = extract_zip(archive_path, extract_to)
    elif archive_ext in ['.tar', '.gz', '.bz2', '.xz', '.tgz'] or '.tar.' in archive_path.name.lower():
        success, error = extract_tar(archive_path, extract_to)
    elif archive_ext == '.7z':
        # Cần cài py7zr: pip install py7zr
        try:
            import py7zr
            with py7zr.SevenZipFile(archive_path, 'r') as archive:
                archive.extractall(extract_to)
            success = True
        except ImportError:
            error = "Can cai thu vien py7zr: pip install py7zr"
        except Exception as e:
            error = str(e)
    elif archive_ext == '.rar':
        # Cần cài rarfile: pip install rarfile (và cài WinRAR/unrar)
        try:
            import rarfile
            with rarfile.RarFile(archive_path, 'r') as rar_ref:
                rar_ref.extractall(extract_to)
            success = True
        except ImportError:
            error = "Can cai thu vien rarfile: pip install rarfile"
        except Exception as e:
            error = str(e)
    else:
        error = f"Dinh dang '{archive_ext}' chua duoc ho tro"
    
    # Tính dung lượng giải nén
    extracted_size = 0
    if success:
        for root, dirs, files in os.walk(extract_to):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.exists(file_path):
                    extracted_size += os.path.getsize(file_path)
    
    return success, error, extracted_size


def find_archives(folder_path):
    """Tìm tất cả file nén trong thư mục"""
    archive_extensions = ['.zip', '.tar', '.gz', '.bz2', '.xz', '.tgz', '.7z', '.rar']
    archives = []
    
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            if any(file.lower().endswith(ext) for ext in archive_extensions) or '.tar.' in file.lower():
                archives.append(file_path)
    
    return archives


def main():
    print_header()
    
    print("===== CHE DO =====")
    print("1. Giai nen 1 file")
    print("2. Giai nen tat ca file trong thu muc")
    
    mode = input("\nChon che do (1-2): ").strip()
    
    if mode == "1":
        # Giải nén 1 file
        archive_input = input("\nNhap duong dan file nen: ").strip('"')
        if not archive_input or not os.path.isfile(archive_input):
            print("❌ File khong ton tai!")
            return
        
        archive_path = Path(archive_input)
        
        # Hỏi thư mục đích
        extract_input = input(f"Giai nen vao thu muc (Enter de dung '{archive_path.stem}'): ").strip('"')
        if not extract_input:
            extract_to = archive_path.parent / archive_path.stem
        else:
            extract_to = Path(extract_input)
        
        print(f"\n📦 Dang giai nen: {archive_path.name}")
        
        success, error, extracted_size = extract_archive(archive_path, extract_to)
        
        if success:
            archive_size = os.path.getsize(archive_path)
            print(f"✅ Giai nen thanh cong!")
            print(f"   📁 Thu muc: {extract_to}")
            print(f"   📊 Kich thuoc nen: {format_size(archive_size)}")
            print(f"   📊 Kich thuoc giai nen: {format_size(extracted_size)}")
        else:
            print(f"❌ Loi: {error}")
    
    elif mode == "2":
        # Giải nén nhiều file
        folder_input = input("\nNhap duong dan thu muc chua file nen: ").strip('"')
        if not folder_input or not os.path.isdir(folder_input):
            print("❌ Thu muc khong ton tai!")
            return
        
        folder_path = Path(folder_input)
        
        # Tìm file nén
        archives = find_archives(folder_path)
        
        if not archives:
            print("❌ Khong tim thay file nen nao!")
            return
        
        print(f"\n📦 Tim thay {len(archives)} file nen:")
        for idx, archive in enumerate(archives, 1):
            archive_name = os.path.basename(archive)
            archive_size = os.path.getsize(archive)
            print(f"   {idx}. {archive_name} ({format_size(archive_size)})")
        
        # Hỏi thư mục đích chung
        extract_base = input(f"\nGiai nen vao thu muc (Enter de dung thu muc hien tai): ").strip('"')
        if not extract_base:
            extract_base = folder_path
        else:
            extract_base = Path(extract_base)
        
        # Xác nhận
        confirm = input(f"\nGiai nen {len(archives)} file? (Y/n): ").strip().lower()
        if confirm == 'n':
            print("❌ Da huy.")
            return
        
        print(f"\n🚀 Bat dau giai nen...\n")
        
        success_count = 0
        total_extracted = 0
        
        for archive in archives:
            archive_path = Path(archive)
            archive_name = archive_path.stem
            extract_to = extract_base / archive_name
            
            print(f"📦 {archive_path.name}...", end=" ")
            
            success, error, extracted_size = extract_archive(archive_path, extract_to)
            
            if success:
                print(f"✅ ({format_size(extracted_size)})")
                success_count += 1
                total_extracted += extracted_size
            else:
                print(f"❌ Loi: {error}")
        
        print(f"\n{'='*60}")
        print(f"✅ Hoan thanh!")
        print(f"   - Thanh cong: {success_count}/{len(archives)} file")
        print(f"   - Tong kich thuoc: {format_size(total_extracted)}")
        print(f"{'='*60}")
    
    else:
        print("❌ Lua chon khong hop le!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Da huy!")
    except Exception as e:
        print(f"\n❌ Loi: {e}")

