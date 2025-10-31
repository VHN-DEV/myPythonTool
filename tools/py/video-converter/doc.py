#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File doc.py - Hướng dẫn sử dụng tool Video Converter
"""


def get_help():
    """
    Trả về hướng dẫn sử dụng cơ bản của tool
    
    Returns:
        str: Hướng dẫn sử dụng tool
    """
    return """
📋 HƯỚNG DẪN SỬ DỤNG:

⚠️  YÊU CẦU: Cài đặt moviepy và FFmpeg trước khi sử dụng

1️⃣  Nhập đường dẫn file video hoặc thư mục chứa video

2️⃣  Chọn chức năng:
   - 1: Convert format (.mp4, .avi, .mov...)
   - 2: Nén video (giảm dung lượng)
   - 3: Trim video (cắt đoạn)
   - 4: Extract audio (trích xuất âm thanh)

3️⃣  Nhập thông tin:
   - Format đích (mp4, avi, mov...)
   - Chất lượng/bitrate (cho nén)
   - Thời gian bắt đầu/kết thúc (cho trim)

4️⃣  Chọn vị trí lưu file output

💡 TIP:
   - Xem thông tin video (duration, resolution, size) trước
   - Nén video có thể mất chất lượng
   - FFmpeg cần được cài đặt và cấu hình đúng

📝 VÍ DỤ:
   File: video.mp4 (100 MB)
   Chức năng: 2 (Nén)
   Bitrate: 2000k
   → Output: video_compressed.mp4 (25 MB)
    """

