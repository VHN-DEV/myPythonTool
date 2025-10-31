#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File doc.py - Hướng dẫn sử dụng tool Font Generator
"""


def get_help():
    """
    Trả về hướng dẫn sử dụng cơ bản của tool
    
    Returns:
        str: Hướng dẫn sử dụng tool
    """
    return """
📋 HƯỚNG DẪN SỬ DỤNG:

⚠️  YÊU CẦU: Cài đặt fonttools và brotli trước khi sử dụng

1️⃣  CHUYỂN ĐỔI ĐỊNH DẠNG FONT:
   - Nhập đường dẫn file font gốc (TTF hoặc OTF)
   - Chọn định dạng output:
     • WOFF: Web Open Font Format (cho web)
     • WOFF2: Phiên bản nén tốt hơn WOFF
     • TTF: TrueType Font
     • OTF: OpenType Font
   - Chọn vị trí lưu file output
   - Tự động hiển thị thông tin font trước khi convert

2️⃣  XEM THÔNG TIN FONT:
   - Nhập đường dẫn file font
   - Xem thông tin:
     • Family name (tên font)
     • Style (Regular, Bold, Italic...)
     • Version
     • Số lượng glyphs (ký tự)
     • Copyright
     • Kích thước file

3️⃣  TẠO FONT SUBSET:
   - Nhập đường dẫn file font gốc
   - Chọn phương thức:
     • Nhập danh sách ký tự: 'Hello World', 'abc123'...
     • Nhập Unicode ranges: 'U+0020-007F,U+0100-017F'
   - Tạo font mới chỉ chứa các ký tự được chọn
   - Giảm kích thước file đáng kể

💡 TIP:
   - WOFF/WOFF2 phù hợp cho web (nén tốt, tải nhanh)
   - TTF/OTF phù hợp cho desktop (chất lượng cao)
   - Font subset giúp giảm dung lượng khi chỉ cần một số ký tự
   - Unicode ranges hữu ích cho các ngôn ngữ cụ thể
     • U+0020-007F: ASCII cơ bản
     • U+0100-017F: Latin Extended-A
     • U+1E00-1EFF: Latin Extended Additional

📝 VÍ DỤ:
   Font: Arial.ttf (500 KB)
   → Convert sang WOFF2 → Arial.woff2 (200 KB)
   
   Font: CustomFont.ttf
   Ký tự: 'Hello World 123'
   → Tạo subset → CustomFont_subset.ttf (50 KB)
   (Giảm 90% kích thước!)

🔤 UNICODE RANGES PHỔ BIẾN:
   - U+0020-007F: ASCII (32-127)
   - U+0100-017F: Latin Extended-A
   - U+0180-024F: Latin Extended-B
   - U+0300-036F: Combining Diacritical Marks
   - U+1E00-1EFF: Latin Extended Additional
   - U+2000-206F: General Punctuation
   - U+20A0-20CF: Currency Symbols
   - U+2100-214F: Letterlike Symbols
    """
