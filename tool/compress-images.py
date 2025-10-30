import os
import datetime
from PIL import Image

def compress_image(input_path, output_path, quality=70, optimize=True, max_size_kb=None, convert_format=None, resize_width=None, resize_height=None):
    try:
        img = Image.open(input_path)

        # Resize nếu có nhập
        if resize_width or resize_height:
            orig_w, orig_h = img.size
            if resize_width and resize_height:
                # Resize theo đúng width & height nhập vào
                new_size = (resize_width, resize_height)
            elif resize_width:
                # Resize theo width, scale chiều cao theo tỉ lệ
                ratio = resize_width / orig_w
                new_size = (resize_width, int(orig_h * ratio))
            elif resize_height:
                # Resize theo height, scale chiều rộng theo tỉ lệ
                ratio = resize_height / orig_h
                new_size = (int(orig_w * ratio), resize_height)

            img = img.resize(new_size, Image.LANCZOS)

        # Nếu muốn đổi định dạng
        if convert_format:
            convert_format = convert_format.lower()
            if convert_format == "jpg":
                convert_format = "jpeg"
            img = img.convert("RGB") if convert_format in ["jpeg", "jpg"] else img
        else:
            convert_format = img.format

        # Đảm bảo thư mục tồn tại
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Nén ban đầu
        img.save(output_path, format=convert_format, quality=quality, optimize=optimize)

        # Nếu có max_size_kb thì giảm dần quality cho đến khi đạt
        if max_size_kb:
            while os.path.getsize(output_path) > max_size_kb * 1024 and quality > 10:
                quality -= 5
                img.save(output_path, format=convert_format, quality=quality, optimize=optimize)

        old_size = os.path.getsize(input_path) / 1024
        new_size = os.path.getsize(output_path) / 1024
        print(f"✅ {os.path.basename(input_path)} | {old_size:.1f}KB → {new_size:.1f}KB (q={quality})")

    except Exception as e:
        print(f"❌ Lỗi với {os.path.basename(input_path)}: {e}")


# ======================= CHẠY =======================
input_dir = input("Nhập đường dẫn thư mục chứa ảnh: ").strip('"')

output_dir = input("Nhập đường dẫn thư mục đầu ra (Enter để mặc định 'compressed' trong thư mục input): ").strip('"')
if not output_dir:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(input_dir, f"compressed_{timestamp}")

os.makedirs(output_dir, exist_ok=True)

quality_input = input("Nhập quality (mặc định 70, Enter để bỏ qua): ")
quality = int(quality_input) if quality_input else 70

optimize_input = input("Có bật optimize không? (Y/n, mặc định Yes): ")
optimize = False if optimize_input.lower() == "n" else True

convert_format = input("Muốn đổi sang định dạng nào? (vd: jpg, png, webp - Enter để giữ nguyên): ").strip()
convert_format = convert_format if convert_format else None

max_size_input = input("Nhập dung lượng tối đa mỗi ảnh (KB, Enter để bỏ qua): ")
max_size_kb = int(max_size_input) if max_size_input else None

resize_w_input = input("Nhập chiều rộng (px, Enter để bỏ qua): ")
resize_width = int(resize_w_input) if resize_w_input else None

resize_h_input = input("Nhập chiều cao (px, Enter để bỏ qua): ")
resize_height = int(resize_h_input) if resize_h_input else None

for filename in os.listdir(input_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        # Nếu đổi định dạng thì đổi luôn phần mở rộng file
        if convert_format:
            ext = convert_format.lower()
            if ext == "jpeg":
                ext = "jpg"
            output_path = os.path.splitext(output_path)[0] + "." + ext

        compress_image(input_path, output_path, quality, optimize, max_size_kb, convert_format, resize_width, resize_height)

print(f"\n🎉 Hoàn thành nén ảnh! Ảnh đã được lưu tại: {output_dir}")
