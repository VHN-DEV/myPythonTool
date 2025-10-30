#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: Thêm watermark vào ảnh hàng loạt
Mục đích: Bảo vệ bản quyền ảnh, thêm logo/text branding
"""

import os
import datetime
from pathlib import Path


def print_header():
    """In header của tool"""
    print("=" * 60)
    print("  TOOL THEM WATERMARK VAO ANH")
    print("=" * 60)
    print()


def check_dependencies():
    """
    Kiểm tra thư viện Pillow
    
    Mục đích: Đảm bảo user đã cài Pillow
    Lý do: Pillow cần thiết cho xử lý ảnh
    """
    try:
        from PIL import Image
        return True
    except ImportError:
        print("❌ Thieu thu vien Pillow!")
        print("Cai dat: pip install Pillow")
        return False


def format_size(size_bytes):
    """Format dung lượng dễ đọc"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0


def get_position_coordinates(image_width, image_height, watermark_width, watermark_height, position, margin=10):
    """
    Tính toán tọa độ watermark theo vị trí
    
    Args:
        image_width, image_height: Kích thước ảnh gốc
        watermark_width, watermark_height: Kích thước watermark
        position: Vị trí (top-left, top-center, top-right, middle-left, center, 
                  middle-right, bottom-left, bottom-center, bottom-right)
        margin: Khoảng cách từ mép (pixels)
    
    Returns:
        tuple: (x, y) tọa độ để đặt watermark
    
    Giải thích:
    - Hỗ trợ 9 vị trí phổ biến
    - Margin để watermark không sát mép
    """
    positions = {
        'top-left': (margin, margin),
        'top-center': ((image_width - watermark_width) // 2, margin),
        'top-right': (image_width - watermark_width - margin, margin),
        
        'middle-left': (margin, (image_height - watermark_height) // 2),
        'center': ((image_width - watermark_width) // 2, (image_height - watermark_height) // 2),
        'middle-right': (image_width - watermark_width - margin, (image_height - watermark_height) // 2),
        
        'bottom-left': (margin, image_height - watermark_height - margin),
        'bottom-center': ((image_width - watermark_width) // 2, image_height - watermark_height - margin),
        'bottom-right': (image_width - watermark_width - margin, image_height - watermark_height - margin),
    }
    
    return positions.get(position, positions['bottom-right'])


def add_text_watermark(image_path, output_path, text, position='bottom-right', 
                       opacity=128, font_size=36, color=(255, 255, 255), margin=10):
    """
    Thêm text watermark vào ảnh
    
    Args:
        image_path: Đường dẫn ảnh gốc
        output_path: Đường dẫn ảnh output
        text: Text watermark
        position: Vị trí đặt watermark
        opacity: Độ trong suốt (0-255, 0=trong suốt hoàn toàn, 255=không trong suốt)
        font_size: Kích thước chữ
        color: Màu chữ RGB (255, 255, 255) = trắng
        margin: Khoảng cách từ mép
    
    Giải thích:
    - Tạo layer trong suốt cho watermark
    - Vẽ text lên layer
    - Composite layer với ảnh gốc
    - Opacity điều khiển độ mờ/đậm của watermark
    """
    from PIL import Image, ImageDraw, ImageFont
    
    try:
        # Mở ảnh gốc
        image = Image.open(image_path).convert('RGBA')
        
        # Tạo layer trong suốt cho watermark
        watermark_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark_layer)
        
        # Load font
        try:
            # Try to use TrueType font
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            try:
                # Try alternative font
                font = ImageFont.truetype("Arial.ttf", font_size)
            except:
                # Fallback to default font
                font = ImageFont.load_default()
        
        # Tính kích thước text
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Tính tọa độ đặt text
        x, y = get_position_coordinates(
            image.width, image.height,
            text_width, text_height,
            position, margin
        )
        
        # Vẽ text với màu và opacity
        text_color = color + (opacity,)
        draw.text((x, y), text, font=font, fill=text_color)
        
        # Composite watermark layer với ảnh gốc
        watermarked = Image.alpha_composite(image, watermark_layer)
        
        # Convert về RGB nếu cần (để save JPEG)
        if output_path.lower().endswith(('.jpg', '.jpeg')):
            watermarked = watermarked.convert('RGB')
        
        # Save
        watermarked.save(output_path, quality=95)
        
        return True, None
        
    except Exception as e:
        return False, str(e)


def add_image_watermark(image_path, output_path, watermark_image_path, 
                       position='bottom-right', opacity=128, scale=0.1, margin=10):
    """
    Thêm image watermark (logo) vào ảnh
    
    Args:
        image_path: Đường dẫn ảnh gốc
        output_path: Đường dẫn ảnh output
        watermark_image_path: Đường dẫn logo/watermark image
        position: Vị trí đặt watermark
        opacity: Độ trong suốt (0-255)
        scale: Tỷ lệ logo so với ảnh gốc (0.1 = 10% chiều rộng ảnh)
        margin: Khoảng cách từ mép
    
    Giải thích:
    - Load logo và resize theo tỷ lệ
    - Điều chỉnh opacity của logo
    - Đặt logo vào vị trí chỉ định
    - Composite với ảnh gốc
    """
    from PIL import Image
    
    try:
        # Mở ảnh gốc và logo
        image = Image.open(image_path).convert('RGBA')
        logo = Image.open(watermark_image_path).convert('RGBA')
        
        # Resize logo theo tỷ lệ
        logo_width = int(image.width * scale)
        logo_height = int(logo.height * (logo_width / logo.width))
        logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
        
        # Điều chỉnh opacity của logo
        if opacity < 255:
            # Tạo alpha channel mới với opacity
            alpha = logo.split()[3]
            alpha = alpha.point(lambda p: int(p * opacity / 255))
            logo.putalpha(alpha)
        
        # Tạo layer trong suốt
        watermark_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
        
        # Tính tọa độ đặt logo
        x, y = get_position_coordinates(
            image.width, image.height,
            logo_width, logo_height,
            position, margin
        )
        
        # Paste logo vào layer
        watermark_layer.paste(logo, (x, y), logo)
        
        # Composite với ảnh gốc
        watermarked = Image.alpha_composite(image, watermark_layer)
        
        # Convert về RGB nếu cần
        if output_path.lower().endswith(('.jpg', '.jpeg')):
            watermarked = watermarked.convert('RGB')
        
        # Save
        watermarked.save(output_path, quality=95)
        
        return True, None
        
    except Exception as e:
        return False, str(e)


def batch_watermark(input_folder, output_folder, watermark_config):
    """
    Thêm watermark hàng loạt
    
    Args:
        input_folder: Thư mục chứa ảnh gốc
        output_folder: Thư mục chứa ảnh đã watermark
        watermark_config: Dictionary config watermark
    
    Returns:
        tuple: (success_count, error_count)
    
    Giải thích:
    - Quét tất cả ảnh trong thư mục
    - Apply watermark cho từng ảnh
    - Đếm số ảnh thành công/lỗi
    """
    # Tạo thư mục output
    os.makedirs(output_folder, exist_ok=True)
    
    # Các định dạng ảnh hỗ trợ
    image_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.bmp']
    
    # Lấy danh sách ảnh
    image_files = [
        f for f in os.listdir(input_folder)
        if os.path.isfile(os.path.join(input_folder, f))
        and os.path.splitext(f)[1].lower() in image_extensions
    ]
    
    if not image_files:
        print("❌ Khong tim thay anh nao!")
        return 0, 0
    
    print(f"📸 Tim thay {len(image_files)} anh\n")
    
    success_count = 0
    error_count = 0
    
    watermark_type = watermark_config.get('type', 'text')
    
    for idx, filename in enumerate(image_files, 1):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        
        print(f"[{idx}/{len(image_files)}] {filename}...", end=" ")
        
        try:
            if watermark_type == 'text':
                success, error = add_text_watermark(
                    input_path, output_path,
                    text=watermark_config.get('text', 'Copyright'),
                    position=watermark_config.get('position', 'bottom-right'),
                    opacity=watermark_config.get('opacity', 128),
                    font_size=watermark_config.get('font_size', 36),
                    color=watermark_config.get('color', (255, 255, 255)),
                    margin=watermark_config.get('margin', 10)
                )
            else:  # image watermark
                success, error = add_image_watermark(
                    input_path, output_path,
                    watermark_image_path=watermark_config.get('logo_path'),
                    position=watermark_config.get('position', 'bottom-right'),
                    opacity=watermark_config.get('opacity', 128),
                    scale=watermark_config.get('scale', 0.1),
                    margin=watermark_config.get('margin', 10)
                )
            
            if success:
                size = format_size(os.path.getsize(output_path))
                print(f"✅ ({size})")
                success_count += 1
            else:
                print(f"❌ {error}")
                error_count += 1
                
        except Exception as e:
            print(f"❌ {e}")
            error_count += 1
    
    return success_count, error_count


def save_template(template_name, config):
    """
    Lưu template watermark
    
    Mục đích: Lưu cấu hình để tái sử dụng
    Lý do: Không cần nhập lại config mỗi lần
    """
    import json
    
    templates_file = 'watermark_templates.json'
    
    # Load templates hiện có
    templates = {}
    if os.path.exists(templates_file):
        try:
            with open(templates_file, 'r', encoding='utf-8') as f:
                templates = json.load(f)
        except:
            templates = {}
    
    # Thêm template mới
    templates[template_name] = config
    
    # Save
    with open(templates_file, 'w', encoding='utf-8') as f:
        json.dump(templates, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Da luu template: {template_name}")


def load_templates():
    """Load tất cả templates đã lưu"""
    import json
    
    templates_file = 'watermark_templates.json'
    
    if not os.path.exists(templates_file):
        return {}
    
    try:
        with open(templates_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}


def list_templates():
    """Hiển thị danh sách templates"""
    templates = load_templates()
    
    if not templates:
        print("Chua co template nao duoc luu.")
        return None
    
    print("\n===== TEMPLATES DA LUU =====")
    template_list = list(templates.keys())
    
    for idx, name in enumerate(template_list, 1):
        config = templates[name]
        print(f"{idx}. {name}")
        print(f"   Type: {config.get('type', 'text')}")
        if config.get('type') == 'text':
            print(f"   Text: {config.get('text', '')}")
        print(f"   Position: {config.get('position', 'bottom-right')}")
        print(f"   Opacity: {config.get('opacity', 128)}")
        print()
    
    choice = input("Chon template (Enter de bo qua): ").strip()
    
    if choice.isdigit() and 1 <= int(choice) <= len(template_list):
        template_name = template_list[int(choice) - 1]
        return templates[template_name]
    
    return None


def main():
    """
    Hàm chính - Menu watermark tool
    
    Giải thích:
    - Hiển thị menu các chức năng
    - Cho phép chọn text hoặc image watermark
    - Config chi tiết (position, opacity, size...)
    - Hỗ trợ template để tái sử dụng
    """
    print_header()
    
    # Kiểm tra dependencies
    if not check_dependencies():
        return
    
    print("===== CHE DO =====")
    print("1. Text Watermark (chu)")
    print("2. Image Watermark (logo)")
    print("3. Dung Template da luu")
    print("0. Thoat")
    
    mode = input("\nChon che do (0-3): ").strip()
    
    if mode == "0":
        print("Thoat chuong trinh.")
        return
    
    watermark_config = {}
    
    if mode == "3":
        # Load template
        config = list_templates()
        if not config:
            print("\n❌ Khong co template nao. Tao moi:")
            mode = input("Chon che do (1=Text, 2=Image): ").strip()
        else:
            watermark_config = config
            mode = None  # Skip config input
    
    # Config watermark
    if mode == "1":
        # Text watermark
        print("\n===== THIET LAP TEXT WATERMARK =====")
        
        text = input("Nhap text watermark (vd: © 2024 Your Name): ").strip()
        if not text:
            text = "© 2024"
        
        watermark_config['type'] = 'text'
        watermark_config['text'] = text
        
    elif mode == "2":
        # Image watermark
        print("\n===== THIET LAP IMAGE WATERMARK =====")
        
        logo_path = input("Nhap duong dan logo/watermark (PNG trong suot): ").strip('"')
        if not os.path.isfile(logo_path):
            print("❌ File logo khong ton tai!")
            return
        
        watermark_config['type'] = 'image'
        watermark_config['logo_path'] = logo_path
        
        scale_input = input("Kich thuoc logo (% chieu rong anh, mac dinh 10): ").strip()
        scale = float(scale_input) / 100 if scale_input else 0.1
        watermark_config['scale'] = scale
    
    # Config chung (nếu chưa có trong template)
    if 'position' not in watermark_config:
        print("\n===== VI TRI WATERMARK =====")
        print("1. Top Left       2. Top Center       3. Top Right")
        print("4. Middle Left    5. Center           6. Middle Right")
        print("7. Bottom Left    8. Bottom Center    9. Bottom Right")
        
        pos_choice = input("\nChon vi tri (1-9, mac dinh 9): ").strip()
        
        positions = {
            '1': 'top-left', '2': 'top-center', '3': 'top-right',
            '4': 'middle-left', '5': 'center', '6': 'middle-right',
            '7': 'bottom-left', '8': 'bottom-center', '9': 'bottom-right'
        }
        
        position = positions.get(pos_choice, 'bottom-right')
        watermark_config['position'] = position
    
    if 'opacity' not in watermark_config:
        opacity_input = input("\nDo trong suot (0-255, 0=trong suot, 255=dac, mac dinh 128): ").strip()
        opacity = int(opacity_input) if opacity_input.isdigit() else 128
        opacity = max(0, min(255, opacity))
        watermark_config['opacity'] = opacity
    
    if watermark_config.get('type') == 'text' and 'font_size' not in watermark_config:
        font_input = input("Kich thuoc chu (pixels, mac dinh 36): ").strip()
        font_size = int(font_input) if font_input.isdigit() else 36
        watermark_config['font_size'] = font_size
        
        color_input = input("Mau chu (white/black, mac dinh white): ").strip().lower()
        color = (0, 0, 0) if color_input == 'black' else (255, 255, 255)
        watermark_config['color'] = color
    
    if 'margin' not in watermark_config:
        watermark_config['margin'] = 10
    
    # Input/Output folders
    print("\n===== THU MUC ANH =====")
    input_folder = input("Thu muc chua anh goc: ").strip('"')
    if not os.path.isdir(input_folder):
        print("❌ Thu muc khong ton tai!")
        return
    
    output_folder = input("Thu muc output (Enter de tao 'watermarked' voi timestamp): ").strip('"')
    if not output_folder:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_folder = os.path.join(input_folder, f"watermarked_{timestamp}")
    
    # Preview config
    print("\n===== XAC NHAN CONFIG =====")
    print(f"Type: {watermark_config['type']}")
    if watermark_config['type'] == 'text':
        print(f"Text: {watermark_config['text']}")
        print(f"Font size: {watermark_config['font_size']}")
    else:
        print(f"Logo: {os.path.basename(watermark_config['logo_path'])}")
        print(f"Scale: {watermark_config['scale'] * 100:.0f}%")
    print(f"Position: {watermark_config['position']}")
    print(f"Opacity: {watermark_config['opacity']}")
    
    confirm = input("\nBat dau xu ly? (Y/n): ").strip().lower()
    if confirm == 'n':
        print("❌ Da huy.")
        return
    
    # Save template option
    save_tpl = input("\nLuu config thanh template? (y/N): ").strip().lower()
    if save_tpl == 'y':
        tpl_name = input("Nhap ten template: ").strip()
        if tpl_name:
            save_template(tpl_name, watermark_config)
    
    # Process
    print(f"\n🚀 Bat dau them watermark...\n")
    
    success, errors = batch_watermark(input_folder, output_folder, watermark_config)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"✅ Hoan thanh!")
    print(f"   - Thanh cong: {success} anh")
    print(f"   - Loi: {errors} anh")
    print(f"   - Thu muc output: {output_folder}")
    print(f"{'='*60}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Da huy!")
    except Exception as e:
        print(f"\n❌ Loi: {e}")

