#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File doc.py - Hướng dẫn sử dụng tool JSON Formatter
"""


def get_help():
    """
    Trả về hướng dẫn sử dụng cơ bản của tool
    
    Returns:
        str: Hướng dẫn sử dụng tool
    """
    return """
📋 HƯỚNG DẪN SỬ DỤNG:

1️⃣  FORMAT FILE JSON (Làm đẹp):
   - Nhập đường dẫn file JSON
   - Chọn số spaces cho mỗi level (2 hoặc 4)
   - Chọn có sắp xếp keys theo alphabet không
   - Chọn có escape Unicode không (mặc định: giữ nguyên)
   - Chọn vị trí lưu file output (hoặc ghi đè file gốc)
   - Tự động indent, xuống dòng cho dễ đọc

2️⃣  VALIDATE JSON (Kiểm tra lỗi):
   - Nhập đường dẫn file JSON
   - Kiểm tra tính hợp lệ của JSON
   - Hiển thị thông tin:
     • Loại dữ liệu (Object, Array, ...)
     • Số keys/phần tử
     • Lỗi cụ thể nếu có

3️⃣  MINIFY JSON (Giảm kích thước):
   - Nhập đường dẫn file JSON
   - Xóa tất cả spaces, xuống dòng không cần thiết
   - Giảm kích thước file đáng kể
   - Phù hợp cho production (nhưng khó đọc)

4️⃣  SỬA LỖI JSON THƯỜNG GẶP:
   - Nhập đường dẫn file JSON có lỗi
   - Tự động sửa một số lỗi:
     • Trailing commas (dấu phẩy cuối)
     • Một số lỗi format cơ bản
   - Lưu file đã sửa

5️⃣  FORMAT NHIỀU FILE JSON (Batch):
   - Nhập thư mục chứa file JSON
   - Tự động tìm tất cả file .json
   - Format tất cả cùng lúc
   - Báo cáo số file thành công/lỗi

💡 TIP:
   - Format với indent 2 hoặc 4 spaces cho dễ đọc
   - Sort keys giúp dễ so sánh giữa các file
   - Minify cho production (giảm bandwidth)
   - Validate trước khi commit code
   - Luôn backup file gốc trước khi format

📝 VÍ DỤ:
   Input: {"a":1,"b":2,"c":3}
   Format (indent 2):
   {
     "a": 1,
     "b": 2,
     "c": 3
   }
   
   Minify:
   {"a":1,"b":2,"c":3}
   
   Format + Sort keys:
   {
     "a": 1,
     "b": 2,
     "c": 3
   }

🔧 LỖI THƯỜNG GẶP:
   - Trailing comma: { "a": 1, } → { "a": 1 }
   - Missing quotes: { a: 1 } → { "a": 1 }
   - Invalid escape: { "path": "C:\path" } → { "path": "C:\\\\path" }
   - Comment không được hỗ trợ (JSON không có comment)
    """
