# Rename Files - Doi ten file hang loat

Mo ta ngan gon: Them prefix/suffix, thay the text trong ten, danh so thu tu 001, doi phan mo rong, chuyen sang chu thuong, xu ly khoang trang.

## Cach su dung

```bash
python tools/rename-files.py
```

## Vi du 1: Doi ten theo so thu tu

```
Nhap duong dan thu muc: D:\Wedding_Photos
Chon chuc nang: 4 (Doi ten file theo so thu tu)
Chi xu ly file co duoi (.jpg .png - Enter de tat ca): .jpg
Nhap ten co so (vd: image): wedding
Bat dau tu so (vd: 1): 1
```

Ket qua mau:

```
✓ DSC_5423.jpg → wedding_001.jpg
✓ DSC_5424.jpg → wedding_002.jpg
```

## Vi du 2: Them prefix

```
Chon chuc nang: 1 (Them prefix)
Nhap prefix (tien to): [Backup]_
```

Ket qua mau:

```
✓ document.pdf → [Backup]_document.pdf
```

## Use case pho bien
- Doi ten anh tu may anh
- Them prefix cho file backup
- Xoa khoang trang ten file
- Doi extension hang loat


