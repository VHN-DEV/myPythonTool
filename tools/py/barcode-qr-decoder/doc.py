#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File doc.py - Hướng dẫn sử dụng tool Barcode QR Decoder
"""


def get_help():
    """
    Trả về hướng dẫn sử dụng cơ bản của tool
    
    Returns:
        str: Hướng dẫn sử dụng tool
    """
    return """
📋 HƯỚNG DẪN SỬ DỤNG:

⚠️  YÊU CẦU: Cài đặt các thư viện trước khi sử dụng:
   pip install opencv-python pyzbar pillow

1️⃣  Nhập đường dẫn thư mục chứa ảnh cần giải mã

2️⃣  Tool sẽ tự động:
   - Quét bằng pyzbar từ ảnh gốc
   - Nếu lỗi → crop vùng barcode → tăng cường ảnh → thử lại
   - Nếu vẫn lỗi → thử xoay ảnh ở các góc (90°, 180°, 270°)
   - Nếu vẫn lỗi → OCR (Tesseract) để đọc text

3️⃣  Kết quả được lưu vào:
   - File result.txt trong mỗi thư mục con
   - File results.txt ở thư mục gốc (tổng hợp)
   - File ảnh thành công được di chuyển vào thư mục ok/

4️⃣  Hỗ trợ các loại mã:
   - Barcode 1D: Code 128, Code 39, EAN, UPC, ITF
   - Barcode 2D: QR Code, Data Matrix, Aztec

💡 TIP:
   - Ảnh càng rõ, tỷ lệ thành công càng cao
   - Tool tự động xử lý ảnh mờ, nghiêng, thiếu sáng
   - Có thể xử lý nhiều ảnh cùng lúc

📝 VÍ DỤ:
   Thư mục: ./images/barcodes
   → Quét tất cả ảnh .jpg, .png, .jpeg
   → Tìm thấy 150/200 ảnh có mã vạch
   → Tỷ lệ thành công: 75%
    """

