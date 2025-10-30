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

