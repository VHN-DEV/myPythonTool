# Backup Folder Tool

## Mô tả

Tool sao lưu và nén thư mục với timestamp tự động.

## Tính năng

✅ Sao lưu thư mục thành file nén
✅ Tự động thêm timestamp vào tên file
✅ Hỗ trợ nhiều định dạng: ZIP, TAR.GZ, TAR.BZ2
✅ Có thể chọn vị trí lưu file backup

## Cách sử dụng

1. Chạy tool từ menu chính
2. Nhập đường dẫn thư mục cần backup
3. Chọn định dạng nén (ZIP/TAR.GZ/TAR.BZ2)
4. Chọn vị trí lưu file backup
5. File backup sẽ được tạo với format: `backup_YYYYMMDD_HHMMSS.zip`

## Ví dụ

```
Input: D:/MyProject
Output: D:/Backups/backup_MyProject_20231030_143022.zip
```

## Lưu ý

- Thư mục nguồn phải tồn tại
- Đảm bảo có đủ dung lượng ổ đĩa
- File backup sẽ có dung lượng tùy thuộc vào định dạng nén

