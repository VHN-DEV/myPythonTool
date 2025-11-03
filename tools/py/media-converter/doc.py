#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File doc.py - Hướng dẫn sử dụng tool Media Converter
"""


def get_help():
    """
    Trả về hướng dẫn sử dụng cơ bản của tool
    
    Returns:
        str: Hướng dẫn sử dụng tool
    """
    return """
📋 HƯỚNG DẪN SỬ DỤNG:

⚠️  YÊU CẦU: Cài đặt pydub, moviepy và FFmpeg trước khi sử dụng

1️⃣  CHUYỂN ĐỔI AUDIO (mp3, wav, aac, flac, ogg):
   - Nhập đường dẫn file audio
   - Chọn định dạng output (MP3, WAV, AAC, FLAC, OGG)
   - Chọn bitrate (128k, 192k, 320k)
   - Chọn vị trí lưu file output

2️⃣  CHUYỂN ĐỔI VIDEO (mp4, avi, mkv, webm, mov):
   - Nhập đường dẫn file video
   - Chọn định dạng output (MP4, AVI, MKV, WEBM, MOV)
   - Chọn preset (ultrafast, fast, medium, slow)
   - Chọn vị trí lưu file output

3️⃣  AUDIO → VIDEO:
   - Nhập đường dẫn file audio
   - Chọn hình ảnh background (hoặc Enter để dùng màu đen)
   - Chọn định dạng video (MP4, AVI, WEBM)
   - Chọn bitrate audio
   - Tạo video từ audio + hình ảnh

4️⃣  VIDEO → AUDIO:
   - Nhập đường dẫn file video
   - Chọn định dạng audio output (MP3, WAV, AAC)
   - Chọn bitrate
   - Trích xuất audio track từ video

💡 TIP:
   - Format phổ biến: MP3 cho audio, MP4 cho video
   - Bitrate cao hơn = chất lượng tốt hơn nhưng file lớn hơn
   - MP3 192k là cân bằng tốt giữa chất lượng và dung lượng
   - WAV/FLAC không nén, chất lượng cao nhất nhưng file rất lớn

📝 VÍ DỤ:
   Audio: music.wav (50 MB)
   → Convert sang MP3 192k → music.mp3 (5 MB)
   
   Video: clip.avi (200 MB)
   → Convert sang MP4 → clip.mp4 (180 MB)
   
   Audio: song.mp3
   + Image: cover.jpg
   → Tạo video song.mp4 (video tĩnh với audio)
    """
