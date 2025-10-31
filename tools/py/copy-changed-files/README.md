# Copy Changed Files - Sao chep file thay doi theo Git

Mo ta ngan gon: Copy file theo commit range, giu nguyen cau truc thu muc, bo qua file da xoa, tao danh sach file da copy, verify commit truoc khi thuc hien.

## Cach su dung

```bash
python tools/copy-changed-files.py
```

## Vi du

```
Nhap duong dan du an: C:\xampp\htdocs\my-ecommerce
Nhap commit ID bat dau (vd: 9d172f6): 9d172f6
Nhap commit ID ket thuc (Enter = HEAD): [Enter]
```

Ket qua mau:

```
🔍 Kiem tra commit ID...
✓ Commit ID hop le!

📂 Dang lay danh sach file thay doi tu commit 9d172f6 den HEAD...
✓ Tim thay 15 file da thay doi

📋 Dang copy file...
✓ [OK] src/components/Header.jsx
✓ [OK] src/styles/main.css
✓ [OK] public/index.html
✓ [OK] api/products.php
... (11 file khac)

===================================================
✓ Hoan tat!
- Da copy: 15 file
- Bo qua: 0 file
- Thu muc xuat: changed-files-export
- Danh sach file: changed-files-export/danh-sach-file-thay-doi.txt
===================================================
```

## Yeu cau
- Thu muc phai la Git repository va co it nhat 1 commit
- Commit ID hop le

## Use case pho bien
- Upload file thay doi len shared hosting
- Tao package update
- Kiem tra truoc khi deploy
- Backup file quan trong da thay doi


