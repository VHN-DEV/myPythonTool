#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: Chuyển đổi encoding của file text
"""

import os
import chardet
from pathlib import Path


def print_header():
    print("=" * 60)
    print("  TOOL CHUYEN DOI ENCODING")
    print("=" * 60)
    print()


def detect_encoding(file_path):
    """
    Phát hiện encoding của file
    
    Returns:
        tuple: (encoding, confidence)
    """
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            return result['encoding'], result['confidence']
    except Exception as e:
        return None, 0


def convert_encoding(file_path, source_encoding, target_encoding, backup=True):
    """
    Chuyển đổi encoding của file
    
    Args:
        file_path: Đường dẫn file
        source_encoding: Encoding nguồn
        target_encoding: Encoding đích
        backup: Có backup file gốc không
    
    Returns:
        bool: Thành công hay không
    """
    try:
        # Đọc file với encoding nguồn
        with open(file_path, 'r', encoding=source_encoding, errors='ignore') as f:
            content = f.read()
        
        # Backup nếu cần
        if backup:
            backup_path = str(file_path) + '.bak'
            with open(backup_path, 'w', encoding=source_encoding) as f:
                with open(file_path, 'r', encoding=source_encoding, errors='ignore') as original:
                    f.write(original.read())
        
        # Ghi lại với encoding đích
        with open(file_path, 'w', encoding=target_encoding, newline='\n') as f:
            f.write(content)
        
        return True
    
    except Exception as e:
        print(f"   ❌ Loi: {e}")
        return False


def convert_folder(folder_path, source_encoding, target_encoding, file_extensions, recursive=True, backup=True):
    """Chuyển đổi tất cả file trong thư mục"""
    
    converted_count = 0
    skipped_count = 0
    error_count = 0
    
    print(f"\n🔄 Bat dau chuyen doi...\n")
    
    if recursive:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if not file_extensions or any(file.lower().endswith(ext) for ext in file_extensions):
                    file_path = os.path.join(root, file)
                    
                    # Detect encoding nếu source là 'auto'
                    if source_encoding.lower() == 'auto':
                        detected, confidence = detect_encoding(file_path)
                        if detected and confidence > 0.7:
                            actual_source = detected
                            print(f"📄 {file} (detect: {detected}, {confidence:.0%})")
                        else:
                            print(f"⚠️  {file} - Khong phat hien duoc encoding, bo qua")
                            skipped_count += 1
                            continue
                    else:
                        actual_source = source_encoding
                        print(f"📄 {file}")
                    
                    # Convert
                    success = convert_encoding(file_path, actual_source, target_encoding, backup)
                    
                    if success:
                        print(f"   ✓ {actual_source} → {target_encoding}")
                        converted_count += 1
                    else:
                        error_count += 1
    else:
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        
        for file in files:
            if not file_extensions or any(file.lower().endswith(ext) for ext in file_extensions):
                file_path = os.path.join(folder_path, file)
                
                if source_encoding.lower() == 'auto':
                    detected, confidence = detect_encoding(file_path)
                    if detected and confidence > 0.7:
                        actual_source = detected
                        print(f"📄 {file} (detect: {detected}, {confidence:.0%})")
                    else:
                        print(f"⚠️  {file} - Khong phat hien duoc encoding, bo qua")
                        skipped_count += 1
                        continue
                else:
                    actual_source = source_encoding
                    print(f"📄 {file}")
                
                success = convert_encoding(file_path, actual_source, target_encoding, backup)
                
                if success:
                    print(f"   ✓ {actual_source} → {target_encoding}")
                    converted_count += 1
                else:
                    error_count += 1
    
    return converted_count, skipped_count, error_count


def detect_mode(folder_path, file_extensions, recursive=True):
    """Chế độ chỉ phát hiện encoding"""
    
    print(f"\n🔍 Dang phat hien encoding...\n")
    
    encoding_stats = {}
    
    if recursive:
        files_to_check = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if not file_extensions or any(file.lower().endswith(ext) for ext in file_extensions):
                    files_to_check.append(os.path.join(root, file))
    else:
        files_to_check = [
            os.path.join(folder_path, f) 
            for f in os.listdir(folder_path) 
            if os.path.isfile(os.path.join(folder_path, f))
            and (not file_extensions or any(f.lower().endswith(ext) for ext in file_extensions))
        ]
    
    for file_path in files_to_check:
        encoding, confidence = detect_encoding(file_path)
        
        if encoding:
            print(f"📄 {os.path.basename(file_path)}")
            print(f"   Encoding: {encoding} (confidence: {confidence:.0%})")
            
            if encoding not in encoding_stats:
                encoding_stats[encoding] = 0
            encoding_stats[encoding] += 1
        else:
            print(f"⚠️  {os.path.basename(file_path)} - Khong phat hien duoc")
    
    # Thống kê
    print(f"\n{'='*60}")
    print(f"📊 Thong ke encoding:")
    for enc, count in sorted(encoding_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"   {enc}: {count} file")
    print(f"{'='*60}")


def main():
    print_header()
    
    # Kiểm tra thư viện chardet
    try:
        import chardet
    except ImportError:
        print("❌ Can cai thu vien chardet: pip install chardet")
        return
    
    # Nhập thư mục
    folder_input = input("Nhap duong dan thu muc: ").strip('"')
    if not folder_input or not os.path.isdir(folder_input):
        print("❌ Thu muc khong ton tai!")
        return
    
    # Loại file
    ext_input = input("Chi xu ly file co duoi (vd: .txt .py .js - Enter de xu ly tat ca): ").strip()
    file_extensions = [ext.strip() for ext in ext_input.split()] if ext_input else []
    
    # Đệ quy
    recursive_input = input("Xu ly tat ca thu muc con? (Y/n): ").strip().lower()
    recursive = recursive_input != 'n'
    
    # Chế độ
    print("\n===== CHE DO =====")
    print("1. Phat hien encoding (khong thay doi file)")
    print("2. Chuyen doi encoding")
    
    mode = input("\nChon che do (1-2): ").strip()
    
    if mode == "1":
        detect_mode(folder_input, file_extensions, recursive)
    
    elif mode == "2":
        print("\n===== ENCODING NGUON =====")
        print("Nhap encoding nguon (vd: utf-8, windows-1252, iso-8859-1)")
        print("Hoac nhap 'auto' de tu dong phat hien")
        source_enc = input("\nEncoding nguon: ").strip() or "auto"
        
        print("\n===== ENCODING DICH =====")
        print("Cac encoding pho bien:")
        print("  - utf-8 (khuyên dùng)")
        print("  - utf-16")
        print("  - windows-1252 (Windows Western)")
        print("  - iso-8859-1 (Latin-1)")
        target_enc = input("\nEncoding dich: ").strip() or "utf-8"
        
        # Backup
        backup_input = input("\nTao backup file goc (.bak)? (Y/n): ").strip().lower()
        backup = backup_input != 'n'
        
        # Xác nhận
        print(f"\n⚠️  CANH BAO: Ban sap thay doi encoding cua nhieu file!")
        print(f"   Tu: {source_enc}")
        print(f"   Sang: {target_enc}")
        if backup:
            print(f"   Backup: Co")
        
        confirm = input("\nXac nhan? (YES de xac nhan): ")
        
        if confirm == "YES":
            converted, skipped, errors = convert_folder(
                folder_input, 
                source_enc, 
                target_enc, 
                file_extensions, 
                recursive, 
                backup
            )
            
            print(f"\n{'='*60}")
            print(f"✅ Hoan thanh!")
            print(f"   - Chuyen doi thanh cong: {converted} file")
            print(f"   - Bo qua: {skipped} file")
            print(f"   - Loi: {errors} file")
            print(f"{'='*60}")
        else:
            print("❌ Da huy.")
    
    else:
        print("❌ Lua chon khong hop le!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Da huy!")
    except Exception as e:
        print(f"\n❌ Loi: {e}")

