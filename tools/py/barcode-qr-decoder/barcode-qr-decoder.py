#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: Giải mã mã vạch và QR code từ ảnh

Mục đích: Đọc barcode và QR code từ ảnh, hỗ trợ nhiều kỹ thuật xử lý ảnh
Lý do: Inventory, payment, document scanning
"""

import os
import sys
import time
import contextlib
import shutil
from pathlib import Path
from typing import List, Tuple, Optional

# Thêm thư mục cha vào sys.path để import utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils import (
    print_header, get_user_input, confirm_action,
    ensure_directory_exists, log_info, log_error, normalize_path
)
from utils.colors import Colors

# Kiểm tra thư viện
try:
    import cv2
    import numpy as np
    from PIL import Image
    from pyzbar.pyzbar import decode
except ImportError as e:
    print(Colors.error("❌ Thiếu thư viện cần thiết!"))
    print("Cài đặt: pip install opencv-python pyzbar pillow numpy")
    sys.exit(1)

# OCR tùy chọn
try:
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print(Colors.warning("⚠️  OCR không khả dụng (tùy chọn: pip install pytesseract)"))


def decode_safe(pil_img):
    """Giải mã barcode bằng pyzbar, ẩn cảnh báo stderr"""
    with contextlib.redirect_stderr(open(os.devnull, 'w')):
        return decode(pil_img)


def enhance_contrast_and_sharpness(img):
    """Tăng tương phản bằng CLAHE và làm nét ảnh"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    # Kernel làm nét
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(enhanced, -1, kernel)
    return sharpened


def auto_crop_barcode(image_cv):
    """Phát hiện vùng có khả năng chứa mã vạch"""
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    grad = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    grad = cv2.convertScaleAbs(grad)
    
    _, thresh = cv2.threshold(grad, 225, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 5))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    closed = cv2.erode(closed, None, iterations=4)
    closed = cv2.dilate(closed, None, iterations=4)
    
    contours, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    
    c = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)
    return image_cv[y:y + h, x:x + w]


def enhance_image(img):
    """Làm nét ảnh mạnh hơn"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    
    blurred = cv2.GaussianBlur(resized, (9, 9), 10.0)
    unsharp = cv2.addWeighted(resized, 1.5, blurred, -0.5, 0)
    denoised = cv2.fastNlMeansDenoising(unsharp, None, h=15, templateWindowSize=7, searchWindowSize=21)
    
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)


def try_decode_with_rotation(pil_img, angle_list=[90, 180, 270]):
    """Thử xoay ảnh ở các góc và decode lại"""
    for angle in angle_list:
        rotated = pil_img.rotate(angle, expand=True)
        barcodes = decode_safe(rotated)
        if barcodes:
            return barcodes
    return []


def decode_with_ocr(image_path):
    """Dùng OCR để đọc text từ ảnh (nếu có pytesseract)"""
    if not OCR_AVAILABLE:
        return []
    
    try:
        ocr_text = pytesseract.image_to_string(Image.open(image_path))
        # Lọc các chuỗi có thể là barcode (8-20 ký tự alphanumeric)
        import re
        text = ocr_text.upper().replace('\n', ' ').replace('\r', ' ').strip()
        text = re.sub(r'[^A-Z0-9]', ' ', text)
        candidates = re.findall(r'\b[A-Z0-9]{8,20}\b', text)
        return list(set(candidates))
    except Exception:
        return []


def process_image(image_path: Path) -> Tuple[List, Optional[str], str]:
    """
    Xử lý từng ảnh để giải mã barcode/QR code
    
    Returns:
        tuple: (barcodes, method, status_message)
    """
    try:
        # 1. Thử decode ảnh gốc
        image_pil = Image.open(image_path)
        barcodes = decode_safe(image_pil)
        if barcodes and any(b.data.strip() for b in barcodes):
            return barcodes, "pyzbar", "Thành công từ ảnh gốc"
        
        # 2. Auto crop → enhance → decode
        image_cv = cv2.imread(str(image_path))
        if image_cv is None:
            return [], None, "Không thể đọc ảnh"
        
        cropped = auto_crop_barcode(image_cv)
        if cropped is not None:
            enhanced = enhance_contrast_and_sharpness(cropped)
            temp_path = str(image_path) + ".temp.jpg"
            cv2.imwrite(temp_path, enhanced)
            
            try:
                image_pil_cropped = Image.open(temp_path)
                barcodes = decode_safe(image_pil_cropped)
                if barcodes:
                    os.remove(temp_path)
                    return barcodes, "pyzbar", "Thành công sau crop + enhance"
                
                # Thử xoay
                barcodes = try_decode_with_rotation(image_pil_cropped)
                if barcodes:
                    os.remove(temp_path)
                    return barcodes, "pyzbar", "Thành công sau xoay"
                
                # Enhance mạnh hơn
                enhanced_strong = enhance_image(cropped)
                cv2.imwrite(temp_path, enhanced_strong)
                image_pil_fallback = Image.open(temp_path)
                barcodes = decode_safe(image_pil_fallback)
                if barcodes:
                    os.remove(temp_path)
                    return barcodes, "pyzbar", "Thành công sau enhance mạnh"
                
                os.remove(temp_path)
            except Exception:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
        
        # 3. Thử xoay ảnh gốc
        barcodes = try_decode_with_rotation(image_pil)
        if barcodes:
            return barcodes, "pyzbar", "Thành công sau xoay ảnh gốc"
        
        # 4. OCR (nếu có)
        if OCR_AVAILABLE:
            ocr_result = decode_with_ocr(image_path)
            if ocr_result:
                class DummyBarcode:
                    def __init__(self, data): 
                        self.data = data.encode('utf-8') if isinstance(data, str) else data
                return [DummyBarcode(data) for data in ocr_result], "ocr", "Đọc được bằng OCR"
        
        return [], None, "Không tìm thấy barcode"
        
    except Exception as e:
        return [], None, f"Lỗi: {e}"


def process_directory(directory: Path, move_success: bool = True):
    """Xử lý toàn bộ thư mục"""
    start_time = time.time()
    total_ok = 0
    total_nok = 0
    total_files = 0
    
    # Đếm file
    extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    for ext in extensions:
        total_files += len(list(directory.rglob(f'*{ext}')))
        total_files += len(list(directory.rglob(f'*{ext.upper()}')))
    
    if total_files == 0:
        print(Colors.warning("⚠️  Không tìm thấy file ảnh nào!"))
        return
    
    # Tạo thư mục ok nếu move_success
    ok_dir = directory / 'ok'
    if move_success:
        ok_dir.mkdir(exist_ok=True)
    
    # File log
    log_path = directory / 'result.txt'
    summary_path = directory / 'results.txt'
    
    with open(log_path, 'w', encoding='utf-8') as log_file, \
         open(summary_path, 'w', encoding='utf-8') as summary_file:
        
        summary_file.write(f"Kết quả quét barcode/QR code\n")
        summary_file.write(f"{'='*70}\n\n")
        
        # Quét từng file
        for ext in extensions:
            for file_path in directory.rglob(f'*{ext}'):
                # Bỏ qua thư mục ok và file temp
                if 'ok' in str(file_path) or '.temp' in str(file_path):
                    continue
                
                print(f"\r{Colors.muted(f'Đang xử lý: {file_path.name:<50}')}", end='', flush=True)
                
                barcodes, method, status = process_image(file_path)
                
                if barcodes:
                    decoded_data = ", ".join([b.data.decode('utf-8', errors='ignore') for b in barcodes])
                    log_line = f"{file_path.name} → OK | {decoded_data} | Method: {method}"
                    
                    log_file.write(log_line + "\n")
                    summary_file.write(log_line + "\n")
                    
                    if move_success:
                        try:
                            shutil.move(str(file_path), str(ok_dir / file_path.name))
                        except Exception:
                            pass
                    
                    total_ok += 1
                    print(f"\r{Colors.success('✓')} {file_path.name}")
                else:
                    log_line = f"{file_path.name} → NOK | {status}"
                    log_file.write(log_line + "\n")
                    total_nok += 1
        
        # Tổng kết
        total = total_ok + total_nok
        percent_ok = round((total_ok / total * 100), 2) if total > 0 else 0
        elapsed = round(time.time() - start_time, 2)
        
        summary = f"""
{'='*70}
Tổng kết:
  - Tổng số ảnh: {total}
  - Thành công: {total_ok} ({percent_ok}%)
  - Thất bại: {total_nok} ({100 - percent_ok:.2f}%)
  - Thời gian: {elapsed} giây
{'='*70}
"""
        summary_file.write(summary)
        log_file.write(summary)
        
        print(summary)


def main():
    """Hàm main"""
    print_header("Tool Giải mã Mã vạch và QR Code", width=70)
    print(Colors.primary("  📷 TOOL GIẢI MÃ MÃ VẠCH VÀ QR CODE"))
    print()
    
    # Bước 1: Nhập đường dẫn
    while True:
        directory = get_user_input("Nhập đường dẫn thư mục chứa ảnh: ")
        if directory:
            break
        print(Colors.error("❌ Vui lòng nhập đường dẫn thư mục!"))
    directory = normalize_path(directory)
    directory_path = Path(directory)
    
    if not directory_path.exists():
        print(Colors.error(f"❌ Thư mục không tồn tại: {directory}"))
        return 1
    
    if not directory_path.is_dir():
        print(Colors.error(f"❌ Đường dẫn không phải thư mục: {directory}"))
        return 1
    
    # Bước 2: Tùy chọn
    print("\n⚙️  Tùy chọn:")
    move_success = confirm_action("Di chuyển ảnh thành công vào thư mục 'ok'?", default=True)
    
    # Bước 3: Xác nhận
    print(f"\n📁 Thư mục: {directory}")
    if not confirm_action("Bắt đầu quét?"):
        print("❌ Đã hủy!")
        return 0
    
    # Bước 4: Quét
    print(f"\n🔍 Đang quét...")
    print(Colors.muted("=" * 70))
    
    process_directory(directory_path, move_success)
    
    print()
    print(Colors.success("✅ Hoàn tất! Xem kết quả trong result.txt và results.txt"))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(Colors.warning("\n⚠️  Đã hủy bởi người dùng!"))
        sys.exit(130)
    except Exception as e:
        log_error(f"❌ Lỗi không mong muốn: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

