#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: Format đúng định dạng JSON
Mục đích: Làm đẹp, validate và sửa lỗi JSON
"""

import os
import sys
import json
from pathlib import Path


def print_header():
    """In header của tool"""
    print("=" * 60)
    print("  TOOL FORMAT ĐỊNH DẠNG JSON")
    print("=" * 60)
    print()


def format_json_string(json_string, indent=2, ensure_ascii=False, sort_keys=False):
    """
    Format chuỗi JSON
    
    Args:
        json_string: Chuỗi JSON
        indent: Số spaces cho mỗi level (2 hoặc 4)
        ensure_ascii: True = escape Unicode, False = giữ nguyên
        sort_keys: True = sắp xếp keys theo alphabet
    
    Returns:
        tuple: (formatted_json, error_message)
    """
    try:
        # Parse JSON
        data = json.loads(json_string)
        
        # Format lại
        formatted = json.dumps(
            data,
            indent=indent,
            ensure_ascii=ensure_ascii,
            sort_keys=sort_keys,
            separators=(',', ': ') if indent > 0 else (',', ':')
        )
        
        return formatted, None
        
    except json.JSONDecodeError as e:
        return None, f"Lỗi JSON: {str(e)}"
    except Exception as e:
        return None, f"Lỗi: {str(e)}"


def validate_json(json_string):
    """
    Kiểm tra tính hợp lệ của JSON
    
    Args:
        json_string: Chuỗi JSON
    
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        json.loads(json_string)
        return True, None
    except json.JSONDecodeError as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)


def minify_json(json_string):
    """
    Minify JSON (xóa spaces, xuống dòng)
    
    Args:
        json_string: Chuỗi JSON
    
    Returns:
        tuple: (minified_json, error_message)
    """
    try:
        data = json.loads(json_string)
        minified = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
        return minified, None
    except json.JSONDecodeError as e:
        return None, f"Lỗi JSON: {str(e)}"
    except Exception as e:
        return None, f"Lỗi: {str(e)}"


def fix_json_common_errors(json_string):
    """
    Sửa một số lỗi JSON thường gặp
    
    Args:
        json_string: Chuỗi JSON có thể có lỗi
    
    Returns:
        tuple: (fixed_json, error_message)
    """
    try:
        # Thử parse trước
        json.loads(json_string)
        return json_string, None
    except json.JSONDecodeError:
        pass
    
    # Sửa một số lỗi thường gặp
    fixed = json_string
    
    # Sửa trailing commas (ví dụ: { "a": 1, })
    import re
    # Loại bỏ trailing commas trong objects
    fixed = re.sub(r',(\s*[}\]])', r'\1', fixed)
    
    # Thử parse lại
    try:
        json.loads(fixed)
        return fixed, None
    except json.JSONDecodeError as e:
        # Nếu vẫn lỗi, trả về lỗi
        return None, f"Không thể tự động sửa lỗi: {str(e)}"


def format_json_file(input_path, output_path=None, indent=2, ensure_ascii=False, sort_keys=False, minify=False):
    """
    Format file JSON
    
    Args:
        input_path: File JSON input
        output_path: File JSON output (None = overwrite input)
        indent: Số spaces cho mỗi level
        ensure_ascii: True = escape Unicode
        sort_keys: True = sắp xếp keys
        minify: True = minify (bỏ qua indent)
    
    Returns:
        bool: True nếu thành công
    """
    try:
        # Đọc file
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Validate
        is_valid, error = validate_json(content)
        if not is_valid:
            print(f"⚠️  JSON không hợp lệ: {error}")
            print("\nBạn có muốn thử sửa lỗi tự động không? (y/n): ", end='')
            choice = input().strip().lower()
            
            if choice == 'y':
                fixed, fix_error = fix_json_common_errors(content)
                if fix_error:
                    print(f"❌ Không thể sửa lỗi: {fix_error}")
                    return False
                content = fixed
                print("✅ Đã sửa một số lỗi thường gặp!")
            else:
                return False
        
        # Format
        if minify:
            formatted, error = minify_json(content)
        else:
            formatted, error = format_json_string(content, indent, ensure_ascii, sort_keys)
        
        if error:
            print(f"❌ {error}")
            return False
        
        # Xác định output path
        if output_path is None:
            output_path = input_path
        
        # Ghi file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted)
        
        # So sánh kích thước
        original_size = os.path.getsize(input_path) if input_path != output_path else len(content)
        output_size = len(formatted)
        ratio = (output_size / original_size) * 100 if original_size > 0 else 0
        
        print(f"\n✅ Format thành công!")
        print(f"   📄 File: {output_path}")
        print(f"   📊 Kích thước: {format_size(output_size)} ({ratio:.1f}%)")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ File không tồn tại: {input_path}")
        return False
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False


def format_size(size_bytes):
    """Format dung lượng dễ đọc"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def main():
    """Hàm chính - Menu JSON formatter"""
    print_header()
    
    print("\n===== CHỨC NĂNG =====")
    print("1. Format file JSON (làm đẹp)")
    print("2. Validate JSON (kiểm tra lỗi)")
    print("3. Minify JSON (giảm kích thước)")
    print("4. Sửa lỗi JSON thường gặp")
    print("5. Format nhiều file JSON (batch)")
    print("0. Thoát")
    
    choice = input("\nChọn chức năng (0-5): ").strip()
    
    if choice == "0":
        print("Thoát chương trình.")
        return
    
    elif choice == "1":
        # Format file JSON
        print("\n===== FORMAT FILE JSON =====")
        
        input_file = input("Nhập đường dẫn file JSON: ").strip('"')
        if not os.path.isfile(input_file):
            print("❌ File không tồn tại!")
            return
        
        output_file = input("Tên file output (Enter để ghi đè file gốc): ").strip('"')
        if not output_file:
            output_file = None
        
        print("\nSố spaces cho mỗi level:")
        print("1. 2 spaces (mặc định)")
        print("2. 4 spaces")
        
        indent_choice = input("\nChọn (1-2, mặc định 1): ").strip()
        indent = 4 if indent_choice == "2" else 2
        
        sort_input = input("Sắp xếp keys theo alphabet? (y/n, mặc định n): ").strip().lower()
        sort_keys = sort_input == 'y'
        
        ensure_ascii_input = input("Escape Unicode? (y/n, mặc định n): ").strip().lower()
        ensure_ascii = ensure_ascii_input == 'y'
        
        format_json_file(input_file, output_file, indent, ensure_ascii, sort_keys)
    
    elif choice == "2":
        # Validate JSON
        print("\n===== VALIDATE JSON =====")
        
        input_file = input("Nhập đường dẫn file JSON: ").strip('"')
        if not os.path.isfile(input_file):
            print("❌ File không tồn tại!")
            return
        
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            is_valid, error = validate_json(content)
            
            if is_valid:
                print(f"\n✅ JSON hợp lệ!")
                
                # Hiển thị thông tin
                try:
                    data = json.loads(content)
                    if isinstance(data, dict):
                        print(f"   Loại: Object")
                        print(f"   Số keys: {len(data)}")
                    elif isinstance(data, list):
                        print(f"   Loại: Array")
                        print(f"   Số phần tử: {len(data)}")
                    else:
                        print(f"   Loại: {type(data).__name__}")
                except:
                    pass
            else:
                print(f"\n❌ JSON không hợp lệ!")
                print(f"   Lỗi: {error}")
        
        except FileNotFoundError:
            print(f"❌ File không tồn tại!")
        except Exception as e:
            print(f"❌ Lỗi: {e}")
    
    elif choice == "3":
        # Minify JSON
        print("\n===== MINIFY JSON =====")
        
        input_file = input("Nhập đường dẫn file JSON: ").strip('"')
        if not os.path.isfile(input_file):
            print("❌ File không tồn tại!")
            return
        
        output_file = input("Tên file output (Enter để tự động): ").strip('"')
        if not output_file:
            base = Path(input_file).stem
            output_file = os.path.join(
                os.path.dirname(input_file),
                f"{base}.min.json"
            )
        
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            minified, error = minify_json(content)
            
            if error:
                print(f"❌ {error}")
            else:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(minified)
                
                original_size = os.path.getsize(input_file)
                output_size = len(minified)
                reduction = ((original_size - output_size) / original_size) * 100
                
                print(f"\n✅ Minify thành công!")
                print(f"   📄 File gốc: {format_size(original_size)}")
                print(f"   📄 File minify: {format_size(output_size)}")
                print(f"   💯 Giảm: {reduction:.1f}%")
        
        except Exception as e:
            print(f"❌ Lỗi: {e}")
    
    elif choice == "4":
        # Fix JSON errors
        print("\n===== SỬA LỖI JSON =====")
        
        input_file = input("Nhập đường dẫn file JSON: ").strip('"')
        if not os.path.isfile(input_file):
            print("❌ File không tồn tại!")
            return
        
        output_file = input("Tên file output (Enter để tự động): ").strip('"')
        if not output_file:
            base = Path(input_file).stem
            output_file = os.path.join(
                os.path.dirname(input_file),
                f"{base}_fixed.json"
            )
        
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            fixed, error = fix_json_common_errors(content)
            
            if error:
                print(f"❌ {error}")
            else:
                if fixed == content:
                    print("\n✅ JSON không có lỗi cần sửa!")
                else:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(fixed)
                    
                    print(f"\n✅ Đã sửa lỗi thành công!")
                    print(f"   📄 File output: {output_file}")
        
        except Exception as e:
            print(f"❌ Lỗi: {e}")
    
    elif choice == "5":
        # Batch format
        print("\n===== FORMAT NHIỀU FILE JSON =====")
        
        input_folder = input("Nhập thư mục chứa file JSON: ").strip('"')
        if not os.path.isdir(input_folder):
            print("❌ Thư mục không tồn tại!")
            return
        
        # Tìm tất cả file JSON
        json_files = []
        for file in os.listdir(input_folder):
            if file.lower().endswith('.json'):
                json_files.append(os.path.join(input_folder, file))
        
        if not json_files:
            print("❌ Không tìm thấy file JSON nào!")
            return
        
        print(f"\nTìm thấy {len(json_files)} file JSON")
        
        indent_choice = input("\nSố spaces (2 hoặc 4, mặc định 2): ").strip()
        indent = 4 if indent_choice == "4" else 2
        
        sort_input = input("Sắp xếp keys? (y/n, mặc định n): ").strip().lower()
        sort_keys = sort_input == 'y'
        
        success_count = 0
        error_count = 0
        
        for idx, json_file in enumerate(json_files, 1):
            print(f"\n[{idx}/{len(json_files)}] {os.path.basename(json_file)}")
            print("-" * 60)
            
            if format_json_file(json_file, None, indent, False, sort_keys):
                success_count += 1
            else:
                error_count += 1
        
        print(f"\n{'='*60}")
        print(f"✅ Hoàn thành!")
        print(f"   - Thành công: {success_count} file")
        print(f"   - Lỗi: {error_count} file")
        print(f"{'='*60}")
    
    else:
        print("❌ Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Đã hủy!")
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
