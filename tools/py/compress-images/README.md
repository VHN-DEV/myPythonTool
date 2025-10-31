# Compress Images - Nen va chinh sua anh

Mo ta ngan gon: Nen anh, resize, doi dinh dang (JPG, PNG, WEBP), gioi han dung luong toi da, toi uu tu dong, tao thu muc output kem timestamp.

## Chuc nang
- Nen anh voi quality tuy chinh (1-100)
- Resize theo width/height hoac giu ti le
- Chuyen doi dinh dang (JPG, PNG, WEBP)
- Gioi han dung luong toi da (KB)
- Tu dong toi uu hoa
- Tao thu muc output voi timestamp

## Cach su dung

```bash
python tools/compress-images.py
```

## Vi du thuc te

```
Nhap duong dan thu muc chua anh: D:\Photos
Nhap duong dan thu muc dau ra (Enter de mac dinh): [Enter]
Nhap quality (mac dinh 70): 80
Co bat optimize khong? (Y/n): Y
Muon doi sang dinh dang nao? (jpg, png, webp): webp
Nhap dung luong toi da moi anh (KB, Enter de bo qua): 500
Nhap chieu rong (px, Enter de bo qua): 1920
Nhap chieu cao (px, Enter de bo qua): [Enter]
```

Ket qua mau:

```
✅ photo1.jpg | 2500.0KB → 450.2KB (q=80)
✅ photo2.png | 1800.5KB → 480.8KB (q=80)
✅ photo3.jpg | 3200.0KB → 495.5KB (q=75)

🎉 Hoan thanh nen anh! Anh da duoc luu tai: D:\Photos\compressed_20241029_143022
```

## Dinh dang ho tro
JPG, JPEG, PNG, WEBP

## Use case pho bien
- Toi uu anh cho website
- Resize anh de upload
- Chuyen PNG sang WEBP
- Giam dung luong album anh

# Compress Images Tool

## Mô tả

Tool nén và chỉnh sửa ảnh hàng loạt (resize, đổi format, nén dung lượng).

## Tính năng

✅ Nén ảnh giảm dung lượng
✅ Resize ảnh (theo width/height/percent)
✅ Chuyển đổi format (JPG, PNG, WEBP, GIF)
✅ Xử lý hàng loạt nhiều ảnh
✅ Giữ nguyên ảnh gốc hoặc ghi đè

## Cách sử dụng

1. Chạy tool từ menu chính
2. Chọn chế độ:
   - Nén ảnh
   - Resize ảnh
   - Chuyển đổi format
3. Chọn thư mục chứa ảnh hoặc file ảnh cụ thể
4. Nhập tham số (quality, size, format...)
5. Chọn thư mục output hoặc ghi đè

## Ví dụ

### Nén ảnh
```
Input: photo.jpg (2.5MB)
Quality: 70%
Output: photo.jpg (800KB)
```

### Resize
```
Input: image.png (1920x1080)
Width: 800
Output: image.png (800x450)
```

### Chuyển format
```
Input: photo.jpg
Format: WEBP
Output: photo.webp (giảm 30-50% dung lượng)
```

## Lưu ý

- Format WEBP cho kết quả tốt nhất (nhỏ gọn, chất lượng cao)
- Quality 70-85% là lý tưởng cho web
- Resize giữ nguyên aspect ratio mặc định

