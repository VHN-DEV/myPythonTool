#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File doc.py - Hướng dẫn sử dụng tool PDF Tools
"""


def get_help():
    """
    Trả về hướng dẫn sử dụng cơ bản của tool
    
    Returns:
        str: Hướng dẫn sử dụng tool
    """
    return """
📋 HƯỚNG DẪN SỬ DỤNG:

⚠️  YÊU CẦU: Cài đặt PyPDF2 và Pillow trước khi sử dụng

1️⃣  Chọn chức năng:
   - 1: Merge PDF (gộp nhiều PDF thành 1)
   - 2: Split PDF (tách PDF thành nhiều file)
   - 3: Compress PDF (nén giảm dung lượng)
   - 4: Convert PDF sang ảnh (PDF → JPG/PNG)

2️⃣  Nhập thông tin:
   - Đường dẫn file PDF hoặc thư mục chứa PDF
   - Đường dẫn output (cho merge, compress, convert)
   - Trang cần tách (cho split): 1-5, 10-15...
   - Chất lượng nén (cho compress)
   - Format ảnh đích (cho convert): jpg, png

3️⃣  Xác nhận và chờ xử lý

💡 TIP:
   - Merge: Chọn nhiều file, sắp xếp theo thứ tự cần gộp
   - Split: Tách theo trang hoặc theo số trang mỗi file
   - Compress: Cân bằng giữa dung lượng và chất lượng
   - Convert: Hỗ trợ convert toàn bộ PDF hoặc từng trang

📝 VÍ DỤ:
   Chức năng: 1 (Merge PDF)
   File: doc1.pdf, doc2.pdf, doc3.pdf
   Output: merged.pdf
   → Gộp thành công: merged.pdf (5.2 MB)
    """

