# Backup Folder - Sao luu va nen thu muc

Mo ta ngan gon: Backup voi ten file kem timestamp, nen ZIP/TAR/TAR.GZ, exclude pattern, hien thi ty le nen va dung luong truoc/sau.

## Cach su dung

```bash
python tools/backup-folder.py
```

## Vi du

```
Nhap duong dan thu muc can backup: D:\my-project
Nhap vi tri luu backup (Enter de luu tai thu muc hien tai): D:\Backups

===== CHE DO BACKUP =====
1. Backup toan bo
2. Backup co loai tru (exclude)

Chon che do (1-2): 2
Nhap cac pattern loai tru (cach nhau boi dau phay): node_modules,.git,__pycache__
```

Ket qua mau:

```
✅ Backup thanh cong!
   💾 File backup: D:\Backups\my-project_backup_20241029_153045.zip
   📊 Kich thuoc: 45.20 MB
```

## Use case pho bien
- Backup truoc khi refactor
- Snapshot dinh ky
- Backup truoc khi xoa file cu
- Nen folder de gui/ upload

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

