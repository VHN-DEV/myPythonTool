#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: Chuyển đổi và xử lý video
Mục đích: Convert format, compress, trim, extract audio
"""

import os
import sys
import datetime
from pathlib import Path


def print_header():
    """In header của tool"""
    print("=" * 60)
    print("  TOOL CHUYỂN ĐỔI VÀ XỬ LÝ VIDEO")
    print("=" * 60)
    print()


def check_dependencies():
    """
    Kiểm tra các thư viện cần thiết
    
    Mục đích: Đảm bảo user đã cài moviepy và ffmpeg
    Lý do: moviepy cần thiết cho xử lý video, ffmpeg là backend
    """
    try:
        import moviepy.editor as mp
        print("✅ Thư viện moviepy: OK")
    except ImportError:
        print("❌ Thiếu thư viện moviepy!")
        print("Cài đặt: pip install moviepy")
        return False
    
    # Check ffmpeg
    try:
        from moviepy.config import get_setting
        ffmpeg_path = get_setting("FFMPEG_BINARY")
        print(f"✅ FFmpeg: OK ({ffmpeg_path})")
    except Exception as e:
        print("⚠️  FFmpeg chưa được cấu hình đúng!")
        print("\nHướng dẫn cài FFmpeg:")
        print("Windows: Tải tại https://www.gyan.dev/ffmpeg/builds/")
        print("        Giải nén và thêm vào PATH")
        print("Linux:   sudo apt-get install ffmpeg")
        print("macOS:   brew install ffmpeg")
        print("\nSau khi cài, chạy lại tool.")
        return False
    
    return True


def format_size(size_bytes):
    """Format dung lượng dễ đọc"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0


def format_time(seconds):
    """Format thời gian dễ đọc (HH:MM:SS)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


def get_video_info(video_path):
    """
    Lấy thông tin video
    
    Returns:
        dict: Thông tin video (duration, fps, resolution, size...)
    
    Giải thích:
    - Dùng moviepy để đọc metadata
    - Hiển thị info cơ bản để user biết
    """
    import moviepy.editor as mp
    
    try:
        clip = mp.VideoFileClip(video_path)
        
        info = {
            'duration': clip.duration,
            'fps': clip.fps,
            'size': clip.size,  # (width, height)
            'file_size': os.path.getsize(video_path),
            'audio': clip.audio is not None
        }
        
        clip.close()
        return info
        
    except Exception as e:
        print(f"❌ Loi khi doc video: {e}")
        return None


def display_video_info(video_path):
    """Hiển thị thông tin video"""
    print(f"\n📹 Video: {os.path.basename(video_path)}")
    print("=" * 60)
    
    info = get_video_info(video_path)
    
    if not info:
        return
    
    width, height = info['size']
    
    print(f"Thoi luong: {format_time(info['duration'])}")
    print(f"Do phan giai: {width}x{height}")
    print(f"FPS: {info['fps']:.2f}")
    print(f"Audio: {'Co' if info['audio'] else 'Khong'}")
    print(f"Kich thuoc: {format_size(info['file_size'])}")
    print("=" * 60)


def convert_video_format(input_path, output_path, output_format='mp4', 
                        codec='libx264', audio_codec='aac', bitrate=None,
                        fps=None, preset='medium'):
    """
    Chuyển đổi định dạng video
    
    Args:
        input_path: Video gốc
        output_path: Video output
        output_format: Format đích (mp4, avi, mkv, webm, mov)
        codec: Video codec (libx264, libx265, mpeg4, libvpx)
        audio_codec: Audio codec (aac, mp3, libvorbis)
        bitrate: Bitrate (None = auto)
        fps: FPS mới (None = giữ nguyên)
        preset: Preset encode (ultrafast, fast, medium, slow, veryslow)
    
    Giải thích:
    - Load video với moviepy
    - Convert sang format mới với codec chỉ định
    - Preset ảnh hưởng tốc độ/chất lượng
      + ultrafast: Nhanh nhưng file lớn
      + slow: Chậm nhưng file nhỏ, chất lượng tốt
    """
    import moviepy.editor as mp
    
    try:
        print(f"\n🎬 Dang chuyen doi...")
        print(f"   Format: {output_format.upper()}")
        print(f"   Codec: {codec}")
        print(f"   Preset: {preset}\n")
        
        # Load video
        clip = mp.VideoFileClip(input_path)
        
        # Điều chỉnh FPS nếu có
        if fps and fps != clip.fps:
            clip = clip.set_fps(fps)
            print(f"   ✓ Dieu chinh FPS: {clip.fps} → {fps}")
        
        # Write video
        clip.write_videofile(
            output_path,
            codec=codec,
            audio_codec=audio_codec,
            bitrate=bitrate,
            preset=preset,
            verbose=False,
            logger=None
        )
        
        clip.close()
        
        # So sánh kích thước
        original_size = os.path.getsize(input_path)
        output_size = os.path.getsize(output_path)
        ratio = (output_size / original_size) * 100
        
        print(f"\n✅ Chuyen doi thanh cong!")
        print(f"   📄 File goc: {format_size(original_size)}")
        print(f"   📄 File moi: {format_size(output_size)} ({ratio:.1f}%)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Loi khi chuyen doi: {e}")
        return False


def compress_video(input_path, output_path, target_size_mb=None, 
                   quality='medium', resolution_scale=1.0):
    """
    Nén video giảm dung lượng
    
    Args:
        input_path: Video gốc
        output_path: Video nén
        target_size_mb: Dung lượng mục tiêu (MB)
        quality: Chất lượng (low, medium, high)
        resolution_scale: Tỷ lệ giảm resolution (0.5 = giảm 50%)
    
    Giải thích:
    - Giảm resolution nếu cần
    - Điều chỉnh bitrate theo target size
    - Nén với preset phù hợp
    """
    import moviepy.editor as mp
    
    try:
        print(f"\n📦 Dang nen video...")
        print(f"   Quality: {quality}")
        
        # Load video
        clip = mp.VideoFileClip(input_path)
        
        # Resize nếu cần
        if resolution_scale < 1.0:
            new_width = int(clip.w * resolution_scale)
            new_height = int(clip.h * resolution_scale)
            # Đảm bảo width/height là số chẵn (yêu cầu của codec)
            new_width = new_width if new_width % 2 == 0 else new_width - 1
            new_height = new_height if new_height % 2 == 0 else new_height - 1
            
            clip = clip.resize((new_width, new_height))
            print(f"   ✓ Resize: {clip.w}x{clip.h} → {new_width}x{new_height}")
        
        # Tính bitrate dựa trên target size
        bitrate = None
        if target_size_mb:
            # Tính bitrate cần thiết (kbps)
            target_size_bits = target_size_mb * 8 * 1024 * 1024
            duration = clip.duration
            bitrate = f"{int(target_size_bits / duration / 1000)}k"
            print(f"   ✓ Target size: {target_size_mb}MB → Bitrate: {bitrate}")
        
        # Preset theo quality
        presets = {
            'low': 'ultrafast',
            'medium': 'fast',
            'high': 'slow'
        }
        preset = presets.get(quality, 'fast')
        
        # Write
        clip.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            bitrate=bitrate,
            preset=preset,
            verbose=False,
            logger=None
        )
        
        clip.close()
        
        # Kết quả
        original_size = os.path.getsize(input_path)
        compressed_size = os.path.getsize(output_path)
        reduction = ((original_size - compressed_size) / original_size) * 100
        
        print(f"\n✅ Nen thanh cong!")
        print(f"   📄 File goc: {format_size(original_size)}")
        print(f"   📄 File nen: {format_size(compressed_size)}")
        print(f"   💯 Giam: {reduction:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Loi khi nen video: {e}")
        return False


def trim_video(input_path, output_path, start_time, end_time):
    """
    Cắt video
    
    Args:
        input_path: Video gốc
        output_path: Video đã cắt
        start_time: Thời điểm bắt đầu (giây hoặc "MM:SS" hoặc "HH:MM:SS")
        end_time: Thời điểm kết thúc
    
    Giải thích:
    - Cắt video từ start_time đến end_time
    - Giữ nguyên codec và quality
    """
    import moviepy.editor as mp
    
    try:
        # Parse time string to seconds
        def parse_time(time_str):
            if isinstance(time_str, (int, float)):
                return time_str
            
            parts = time_str.split(':')
            if len(parts) == 2:  # MM:SS
                return int(parts[0]) * 60 + int(parts[1])
            elif len(parts) == 3:  # HH:MM:SS
                return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            else:
                return float(time_str)
        
        start = parse_time(start_time)
        end = parse_time(end_time)
        
        print(f"\n✂️  Dang cat video...")
        print(f"   Tu: {format_time(start)}")
        print(f"   Den: {format_time(end)}")
        print(f"   Thoi luong: {format_time(end - start)}\n")
        
        # Load và cắt
        clip = mp.VideoFileClip(input_path).subclip(start, end)
        
        # Write
        clip.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )
        
        clip.close()
        
        print(f"\n✅ Cat thanh cong!")
        print(f"   📄 File output: {output_path}")
        print(f"   📊 Kich thuoc: {format_size(os.path.getsize(output_path))}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Loi khi cat video: {e}")
        return False


def extract_audio(input_path, output_path, audio_format='mp3', bitrate='192k'):
    """
    Trích xuất audio từ video
    
    Args:
        input_path: Video gốc
        output_path: File audio output
        audio_format: Format audio (mp3, wav, aac)
        bitrate: Bitrate audio (128k, 192k, 320k)
    
    Giải thích:
    - Extract audio track từ video
    - Convert sang format mong muốn
    """
    import moviepy.editor as mp
    
    try:
        print(f"\n🎵 Dang trich xuat audio...")
        print(f"   Format: {audio_format.upper()}")
        print(f"   Bitrate: {bitrate}\n")
        
        # Load video
        clip = mp.VideoFileClip(input_path)
        
        if not clip.audio:
            print("❌ Video khong co audio!")
            clip.close()
            return False
        
        # Extract audio
        audio = clip.audio
        audio.write_audiofile(
            output_path,
            bitrate=bitrate,
            verbose=False,
            logger=None
        )
        
        audio.close()
        clip.close()
        
        print(f"\n✅ Trich xuat thanh cong!")
        print(f"   📄 File audio: {output_path}")
        print(f"   📊 Kich thuoc: {format_size(os.path.getsize(output_path))}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Loi khi trich xuat audio: {e}")
        return False


def change_resolution(input_path, output_path, width=None, height=None, keep_aspect=True):
    """
    Thay đổi resolution video
    
    Args:
        input_path: Video gốc
        output_path: Video mới
        width: Chiều rộng mới
        height: Chiều cao mới
        keep_aspect: Giữ tỷ lệ khung hình
    
    Giải thích:
    - Resize video về resolution mới
    - Nếu keep_aspect=True, tự tính height/width để giữ tỷ lệ
    """
    import moviepy.editor as mp
    
    try:
        print(f"\n🖼️  Dang thay doi resolution...")
        
        # Load video
        clip = mp.VideoFileClip(input_path)
        
        original_width, original_height = clip.size
        
        # Tính new size
        if keep_aspect:
            if width and not height:
                # Tính height dựa trên width
                aspect_ratio = original_height / original_width
                height = int(width * aspect_ratio)
            elif height and not width:
                # Tính width dựa trên height
                aspect_ratio = original_width / original_height
                width = int(height * aspect_ratio)
        
        # Đảm bảo width/height chẵn
        if width:
            width = width if width % 2 == 0 else width - 1
        if height:
            height = height if height % 2 == 0 else height - 1
        
        print(f"   Resolution: {original_width}x{original_height} → {width}x{height}\n")
        
        # Resize
        clip_resized = clip.resize((width, height))
        
        # Write
        clip_resized.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )
        
        clip_resized.close()
        clip.close()
        
        print(f"\n✅ Thay doi thanh cong!")
        print(f"   📄 File output: {output_path}")
        print(f"   📊 Kich thuoc: {format_size(os.path.getsize(output_path))}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Loi khi thay doi resolution: {e}")
        return False


def batch_convert(input_folder, output_folder, output_format='mp4', preset='medium'):
    """
    Convert hàng loạt video
    
    Giải thích:
    - Quét tất cả video trong thư mục
    - Convert từng video sang format mới
    """
    import moviepy.editor as mp
    
    # Các format video hỗ trợ
    video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg']
    
    # Tìm video files
    video_files = [
        f for f in os.listdir(input_folder)
        if os.path.isfile(os.path.join(input_folder, f))
        and os.path.splitext(f)[1].lower() in video_extensions
    ]
    
    if not video_files:
        print("❌ Khong tim thay video nao!")
        return 0, 0
    
    print(f"🎬 Tim thay {len(video_files)} video\n")
    
    # Tạo output folder
    os.makedirs(output_folder, exist_ok=True)
    
    success_count = 0
    error_count = 0
    
    for idx, filename in enumerate(video_files, 1):
        input_path = os.path.join(input_folder, filename)
        
        # Output filename với extension mới
        base_name = Path(filename).stem
        output_filename = f"{base_name}.{output_format}"
        output_path = os.path.join(output_folder, output_filename)
        
        print(f"\n[{idx}/{len(video_files)}] {filename}")
        print("-" * 60)
        
        try:
            clip = mp.VideoFileClip(input_path)
            
            clip.write_videofile(
                output_path,
                codec='libx264' if output_format == 'mp4' else 'mpeg4',
                audio_codec='aac',
                preset=preset,
                verbose=False,
                logger=None
            )
            
            clip.close()
            
            output_size = format_size(os.path.getsize(output_path))
            print(f"✅ Thanh cong! ({output_size})")
            success_count += 1
            
        except Exception as e:
            print(f"❌ Loi: {e}")
            error_count += 1
    
    return success_count, error_count


def main():
    """
    Hàm chính - Menu video tools
    
    Giải thích:
    - Hiển thị menu các chức năng
    - Xử lý input từ user
    - Gọi hàm tương ứng
    """
    print_header()
    
    # Kiểm tra dependencies
    if not check_dependencies():
        print("\n💡 Sau khi cài đặt, chạy lại tool.")
        return
    
    print("\n===== CHỨC NĂNG =====")
    print("1. Chuyển đổi định dạng (Convert Format)")
    print("2. Nén video (Compress)")
    print("3. Cắt video (Trim)")
    print("4. Trích xuất audio (Extract Audio)")
    print("5. Thay đổi resolution")
    print("6. Xem thông tin video")
    print("7. Chuyển đổi hàng loạt (Batch Convert)")
    print("0. Thoát")
    
    choice = input("\nChọn chức năng (0-7): ").strip()
    
    if choice == "0":
        print("Thoát chương trình.")
        return
    
    elif choice == "1":
        # Convert format
        print("\n===== CHUYEN DOI DINH DANG =====")
        
        input_file = input("Nhap duong dan video: ").strip('"')
        if not os.path.isfile(input_file):
            print("❌ File khong ton tai!")
            return
        
        display_video_info(input_file)
        
        print("\nDinh dang output:")
        print("1. MP4 (pho bien nhat)")
        print("2. AVI")
        print("3. MKV (chat luong cao)")
        print("4. WEBM (cho web)")
        print("5. MOV (Apple)")
        
        format_choice = input("\nChon dinh dang (1-5): ").strip()
        formats = {'1': 'mp4', '2': 'avi', '3': 'mkv', '4': 'webm', '5': 'mov'}
        output_format = formats.get(format_choice, 'mp4')
        
        output_file = input("Ten file output (Enter de tu dong): ").strip('"')
        if not output_file:
            base = Path(input_file).stem
            output_file = os.path.join(
                os.path.dirname(input_file),
                f"{base}_converted.{output_format}"
            )
        
        print("\nPreset (toc do/chat luong):")
        print("1. ultrafast (nhanh nhat)")
        print("2. fast")
        print("3. medium (can bang)")
        print("4. slow (chat luong tot)")
        
        preset_choice = input("\nChon preset (1-4, mac dinh 3): ").strip()
        presets = {'1': 'ultrafast', '2': 'fast', '3': 'medium', '4': 'slow'}
        preset = presets.get(preset_choice, 'medium')
        
        convert_video_format(input_file, output_file, output_format, preset=preset)
    
    elif choice == "2":
        # Compress
        print("\n===== NEN VIDEO =====")
        
        input_file = input("Nhap duong dan video: ").strip('"')
        if not os.path.isfile(input_file):
            print("❌ File khong ton tai!")
            return
        
        display_video_info(input_file)
        
        output_file = input("\nTen file output (Enter de tu dong): ").strip('"')
        if not output_file:
            base = Path(input_file).stem
            ext = Path(input_file).suffix
            output_file = os.path.join(
                os.path.dirname(input_file),
                f"{base}_compressed{ext}"
            )
        
        print("\nChat luong:")
        print("1. Low (nen manh, kich thuoc nho)")
        print("2. Medium (can bang)")
        print("3. High (nen nhe, chat luong tot)")
        
        quality_choice = input("\nChon chat luong (1-3, mac dinh 2): ").strip()
        qualities = {'1': 'low', '2': 'medium', '3': 'high'}
        quality = qualities.get(quality_choice, 'medium')
        
        resolution_input = input("\nGiam resolution? (%, 100=giu nguyen, 50=giam 50%): ").strip()
        resolution_scale = float(resolution_input) / 100 if resolution_input else 1.0
        
        target_size = input("\nDung luong muc tieu (MB, Enter de bo qua): ").strip()
        target_size_mb = int(target_size) if target_size else None
        
        compress_video(input_file, output_file, target_size_mb, quality, resolution_scale)
    
    elif choice == "3":
        # Trim
        print("\n===== CAT VIDEO =====")
        
        input_file = input("Nhap duong dan video: ").strip('"')
        if not os.path.isfile(input_file):
            print("❌ File khong ton tai!")
            return
        
        display_video_info(input_file)
        
        print("\nNhap thoi gian (dinh dang: MM:SS hoac HH:MM:SS hoac giay)")
        start_time = input("Bat dau tu (vd: 00:30 hoac 30): ").strip()
        end_time = input("Ket thuc tai (vd: 02:15 hoac 135): ").strip()
        
        output_file = input("\nTen file output (Enter de tu dong): ").strip('"')
        if not output_file:
            base = Path(input_file).stem
            ext = Path(input_file).suffix
            output_file = os.path.join(
                os.path.dirname(input_file),
                f"{base}_trimmed{ext}"
            )
        
        trim_video(input_file, output_file, start_time, end_time)
    
    elif choice == "4":
        # Extract audio
        print("\n===== TRICH XUAT AUDIO =====")
        
        input_file = input("Nhap duong dan video: ").strip('"')
        if not os.path.isfile(input_file):
            print("❌ File khong ton tai!")
            return
        
        display_video_info(input_file)
        
        print("\nDinh dang audio:")
        print("1. MP3 (pho bien)")
        print("2. WAV (khong mat du lieu)")
        print("3. AAC (chat luong tot)")
        
        format_choice = input("\nChon dinh dang (1-3, mac dinh 1): ").strip()
        formats = {'1': 'mp3', '2': 'wav', '3': 'aac'}
        audio_format = formats.get(format_choice, 'mp3')
        
        bitrate_input = input("Bitrate (128k/192k/320k, mac dinh 192k): ").strip()
        bitrate = bitrate_input if bitrate_input else '192k'
        
        output_file = input("\nTen file output (Enter de tu dong): ").strip('"')
        if not output_file:
            base = Path(input_file).stem
            output_file = os.path.join(
                os.path.dirname(input_file),
                f"{base}.{audio_format}"
            )
        
        extract_audio(input_file, output_file, audio_format, bitrate)
    
    elif choice == "5":
        # Change resolution
        print("\n===== THAY DOI RESOLUTION =====")
        
        input_file = input("Nhap duong dan video: ").strip('"')
        if not os.path.isfile(input_file):
            print("❌ File khong ton tai!")
            return
        
        display_video_info(input_file)
        
        print("\nPreset resolution:")
        print("1. 1920x1080 (Full HD)")
        print("2. 1280x720 (HD)")
        print("3. 854x480 (SD)")
        print("4. 640x360 (Low)")
        print("5. Custom")
        
        res_choice = input("\nChon (1-5): ").strip()
        
        if res_choice == "5":
            width = int(input("Chieu rong (width): "))
            height = int(input("Chieu cao (height, Enter de giu ty le): ").strip() or 0)
        else:
            resolutions = {
                '1': (1920, 1080),
                '2': (1280, 720),
                '3': (854, 480),
                '4': (640, 360)
            }
            width, height = resolutions.get(res_choice, (1280, 720))
        
        output_file = input("\nTen file output (Enter de tu dong): ").strip('"')
        if not output_file:
            base = Path(input_file).stem
            ext = Path(input_file).suffix
            output_file = os.path.join(
                os.path.dirname(input_file),
                f"{base}_{width}x{height if height else 'auto'}{ext}"
            )
        
        change_resolution(input_file, output_file, width, height if height else None)
    
    elif choice == "6":
        # Video info
        print("\n===== THONG TIN VIDEO =====")
        
        input_file = input("Nhap duong dan video: ").strip('"')
        if not os.path.isfile(input_file):
            print("❌ File khong ton tai!")
            return
        
        display_video_info(input_file)
    
    elif choice == "7":
        # Batch convert
        print("\n===== CHUYEN DOI HANG LOAT =====")
        
        input_folder = input("Thu muc chua video: ").strip('"')
        if not os.path.isdir(input_folder):
            print("❌ Thu muc khong ton tai!")
            return
        
        output_folder = input("Thu muc output (Enter de tao 'converted'): ").strip('"')
        if not output_folder:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_folder = os.path.join(input_folder, f"converted_{timestamp}")
        
        format_choice = input("\nDinh dang output (mp4/avi/mkv, mac dinh mp4): ").strip()
        output_format = format_choice if format_choice else 'mp4'
        
        preset_choice = input("Preset (ultrafast/fast/medium/slow, mac dinh medium): ").strip()
        preset = preset_choice if preset_choice else 'medium'
        
        success, errors = batch_convert(input_folder, output_folder, output_format, preset)
        
        print(f"\n{'='*60}")
        print(f"✅ Hoan thanh!")
        print(f"   - Thanh cong: {success} video")
        print(f"   - Loi: {errors} video")
        print(f"   - Thu muc output: {output_folder}")
        print(f"{'='*60}")
    
    else:
        print("❌ Lua chon khong hop le!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Đã hủy!")
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")

