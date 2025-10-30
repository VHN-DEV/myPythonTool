# 🛠️ myPythonTool - Bộ Công Cụ Python Tiện Ích

Bộ công cụ Python đa năng giúp tự động hóa các tác vụ thường gặp khi làm việc với file và thư mục.

## 📑 Mục lục

- [Giới thiệu](#giới-thiệu)
- [Cài đặt](#cài-đặt)
- [Cách sử dụng](#cách-sử-dụng)
- [Danh sách công cụ](#danh-sách-công-cụ)
- [Chi tiết từng công cụ](#chi-tiết-từng-công-cụ)
- [FAQ & Troubleshooting](#faq--troubleshooting)

---

## 🎯 Giới thiệu

**myPythonTool** là bộ công cụ Python được thiết kế để giúp bạn:
- ✅ Xử lý hình ảnh (nén, resize, chuyển đổi định dạng)
- ✅ Quản lý file Git (copy file thay đổi theo commit)
- ✅ Tổ chức file theo loại, ngày tháng, extension
- ✅ Tìm và xóa file trùng lặp
- ✅ Backup thư mục tự động
- ✅ Đổi tên hàng loạt file
- ✅ Tìm kiếm và thay thế text trong nhiều file
- ✅ Dọn dẹp file tạm và cache
- ✅ Giải nén nhiều file cùng lúc
- ✅ Chuyển đổi encoding của file text
- ✅ Tạo cây thư mục dự án
- ✅ SSH nhanh vào server

---

## 💾 Cài đặt

### Yêu cầu hệ thống
- Python 3.7 trở lên
- Windows, Linux, hoặc macOS

### Bước 1: Clone hoặc tải về dự án

```bash
git clone https://github.com/your-repo/myPythonTool.git
cd myPythonTool
```

### Bước 2: Cài đặt thư viện

```bash
pip install -r requirements.txt
```

**Thư viện bắt buộc:**
- `Pillow` - Xử lý hình ảnh
- `chardet` - Phát hiện encoding

**Thư viện tùy chọn:**
- `py7zr` - Hỗ trợ giải nén .7z
- `rarfile` - Hỗ trợ giải nén .rar

---

## 🚀 Cách sử dụng

### Chạy Menu Chính

```bash
python menu.py
```

Menu sẽ tự động quét và hiển thị tất cả công cụ có sẵn trong thư mục `tool/`:

```
===== Danh sách tool =====
1. backup-folder.py
2. clean-temp-files.py
3. compress-images.py
4. copy-changed-files.py
5. duplicate-finder.py
6. extract-archive.py
7. file-organizer.py
8. find-and-replace.py
9. generate-tree.py
10. rename-files.py
11. text-encoding-converter.py
0. Thoát

Chọn số để chạy tool:
```

### Chạy Tool Riêng Lẻ

```bash
python tool/compress-images.py
python tool/rename-files.py
```

### SSH Menu

```bash
python menu-ssh.py
```

Kết nối SSH nhanh vào các server đã cấu hình sẵn.

---

## 📦 Danh sách công cụ

| STT | Tên Tool | Chức năng chính |
|-----|----------|----------------|
| 1 | **compress-images.py** | Nén và chuyển đổi hình ảnh |
| 2 | **copy-changed-files.py** | Copy file thay đổi theo Git commit |
| 3 | **rename-files.py** | Đổi tên hàng loạt file |
| 4 | **backup-folder.py** | Backup thư mục với timestamp |
| 5 | **find-and-replace.py** | Tìm và thay thế text |
| 6 | **generate-tree.py** | Tạo cây thư mục dự án |
| 7 | **clean-temp-files.py** | Dọn dẹp file tạm và cache |
| 8 | **extract-archive.py** | Giải nén nhiều file |
| 9 | **duplicate-finder.py** | Tìm file trùng lặp |
| 10 | **file-organizer.py** | Sắp xếp file tự động |
| 11 | **text-encoding-converter.py** | Chuyển đổi encoding |

---

## 📖 Chi tiết từng công cụ

### 1. 🖼️ compress-images.py - Nén hình ảnh

**Mục đích:** Nén, resize và chuyển đổi định dạng hình ảnh hàng loạt.

**Tính năng:**
- ✅ Nén với quality tùy chỉnh (1-100)
- ✅ Resize theo width/height hoặc giữ tỉ lệ
- ✅ Chuyển đổi định dạng (JPG, PNG, WEBP)
- ✅ Giới hạn dung lượng tối đa (KB)
- ✅ Tự động tối ưu hóa
- ✅ Tạo thư mục output với timestamp

**Cách sử dụng:**

```bash
python tool/compress-images.py
```

**Ví dụ:**

```
Nhập đường dẫn thư mục chứa ảnh: D:\Photos
Nhập đường dẫn thư mục đầu ra (Enter để mặc định): [Enter]
Nhập quality (70): 80
Có bật optimize không? (Y/n): Y
Muốn đổi sang định dạng nào? (jpg, png, webp): webp
Nhập dung lượng tối đa mỗi ảnh (KB): 500
Nhập chiều rộng (px): 1920
Nhập chiều cao (px): [Enter]
```

**Kết quả:**
```
✅ photo1.jpg | 2500.0KB → 450.2KB (q=80)
✅ photo2.png | 1800.5KB → 480.8KB (q=80)

🎉 Hoàn thành nén ảnh! Ảnh đã được lưu tại: D:\Photos\compressed_20241029_143022
```

**Định dạng hỗ trợ:** JPG, JPEG, PNG, WEBP

---

### 2. 🔄 copy-changed-files.py - Copy file Git thay đổi

**Mục đích:** Copy các file đã thay đổi từ commit cụ thể để dễ dàng upload lên server.

**Tính năng:**
- ✅ Copy file theo commit range
- ✅ Giữ nguyên cấu trúc thư mục
- ✅ Bỏ qua file đã xóa
- ✅ Tạo danh sách file đã copy
- ✅ Verify commit ID trước khi thực hiện

**Cách sử dụng:**

```bash
python tool/copy-changed-files.py
```

**Ví dụ:**

```
Nhập đường dẫn dự án: C:\xampp\htdocs\my-project
Nhập commit ID bắt đầu: 9d172f6
Nhập commit ID kết thúc (Enter = HEAD): [Enter]
```

**Kết quả:**
```
✓ [OK] src/components/Header.jsx
✓ [OK] src/styles/main.css
✓ [OK] public/index.html

✓ Hoàn tất!
- Đã copy: 15 file
- Bỏ qua: 2 file
- Thư mục xuất: changed-files-export
- Danh sách file: changed-files-export/danh-sach-file-thay-doi.txt

🚀 Bạn có thể upload toàn bộ thư mục 'changed-files-export' lên server bằng FileZilla!
```

**Yêu cầu:** Thư mục phải là Git repository

---

### 3. ✏️ rename-files.py - Đổi tên hàng loạt

**Mục đích:** Đổi tên nhiều file cùng lúc theo pattern.

**Tính năng:**
- ✅ Thêm prefix (tiền tố)
- ✅ Thêm suffix (hậu tố)
- ✅ Thay thế text trong tên
- ✅ Đổi tên theo số thứ tự (001, 002, ...)
- ✅ Đổi phần mở rộng file
- ✅ Chuyển sang chữ thường
- ✅ Xóa/thay thế khoảng trắng

**Cách sử dụng:**

```bash
python tool/rename-files.py
```

**Ví dụ 1: Thêm prefix**
```
Nhập đường dẫn thư mục: D:\Photos
Chọn chức năng: 1
Chỉ xử lý file có đuôi (.jpg .png): .jpg
Nhập prefix: vacation_2024_
```

Kết quả:
```
✓ IMG001.jpg → vacation_2024_IMG001.jpg
✓ IMG002.jpg → vacation_2024_IMG002.jpg
```

**Ví dụ 2: Đổi tên theo số thứ tự**
```
Chọn chức năng: 4
Nhập tên cơ sở: photo
Bắt đầu từ số: 1
```

Kết quả:
```
✓ random_name1.jpg → photo_001.jpg
✓ random_name2.jpg → photo_002.jpg
✓ random_name3.jpg → photo_003.jpg
```

---

### 4. 💾 backup-folder.py - Backup thư mục

**Mục đích:** Tạo bản backup thư mục với timestamp tự động.

**Tính năng:**
- ✅ Backup với tên file timestamp
- ✅ Nén file (ZIP, TAR, TAR.GZ)
- ✅ Backup có loại trừ (node_modules, .git, ...)
- ✅ Hiển thị tỷ lệ nén
- ✅ Tính toán dung lượng

**Cách sử dụng:**

```bash
python tool/backup-folder.py
```

**Ví dụ:**

```
Nhập đường dẫn thư mục cần backup: D:\my-project
Nhập vị trí lưu backup (Enter = thư mục hiện tại): D:\Backups
Chọn chế độ backup: 1
Chọn định dạng nén: 1 (ZIP)
```

**Kết quả:**
```
📊 Đang tính dung lượng...
   Dung lượng: 125.50 MB
📦 Đang nén và backup...

✅ Backup thành công!
   📁 Thư mục nguồn: D:\my-project
   💾 File backup: D:\Backups\my-project_backup_20241029_143500.zip
   📊 Kích thước gốc: 125.50 MB
   📊 Kích thước nén: 45.20 MB
   💯 Tỷ lệ nén: 36.0%
```

---

### 5. 🔍 find-and-replace.py - Tìm và thay thế

**Mục đích:** Tìm kiếm và thay thế text trong nhiều file.

**Tính năng:**
- ✅ Tìm kiếm text trong nhiều file
- ✅ Hỗ trợ Regular Expression
- ✅ Case sensitive/insensitive
- ✅ Tìm đệ quy trong thư mục con
- ✅ Chế độ preview (chỉ xem, không thay đổi)
- ✅ Hiển thị số dòng tìm thấy

**Cách sử dụng:**

```bash
python tool/find-and-replace.py
```

**Ví dụ 1: Chỉ tìm kiếm**

```
Nhập đường dẫn thư mục: D:\my-project
Tìm kiếm trong tất cả thư mục con? (Y/n): Y
Chỉ xử lý file có đuôi (.txt .py): .js .jsx
Nhập text cần tìm: useState
Phân biệt chữ hoa/thường? (y/N): N
Sử dụng Regular Expression? (y/N): N
Chọn chế độ: 1
```

**Kết quả:**
```
📄 src/components/Header.jsx
   Line 5: import { useState, useEffect } from 'react';
   Line 12: const [count, setCount] = useState(0);

📄 src/pages/Home.jsx
   Line 8: const [data, setData] = useState([]);

✅ Tìm thấy 3 kết quả trong 2 file
```

**Ví dụ 2: Tìm và thay thế**

```
Nhập text cần tìm: var 
Nhập text thay thế: let 
Chọn chế độ: 2
Xác nhận thực hiện? (YES): YES
```

**Kết quả:**
```
✓ src/old-script.js - Thay thế 5 lần
✓ src/legacy.js - Thay thế 3 lần

✅ Đã thay thế 8 lần trong 2 file
```

---

### 6. 🌳 generate-tree.py - Tạo cây thư mục

**Mục đích:** Tạo sơ đồ cây thư mục của dự án.

**Tính năng:**
- ✅ Hiển thị cây thư mục với icon
- ✅ Loại trừ folder không cần (node_modules, .git, ...)
- ✅ Giới hạn độ sâu
- ✅ Hiển thị/ẩn file ẩn
- ✅ Xuất ra file text
- ✅ Thống kê số file và folder

**Cách sử dụng:**

```bash
python tool/generate-tree.py
```

**Ví dụ:**

```
Nhập đường dẫn thư mục (Enter = thư mục hiện tại): D:\my-project
Các thư mục/file cần bỏ qua: node_modules, .git, dist
Độ sâu tối đa (Enter = không giới hạn): 3
Hiển thị file/folder ẩn? (y/N): N
```

**Kết quả:**
```
📂 my-project/
├── 📁 src/
│   ├── 📁 components/
│   │   ├── 🌐 Header.jsx
│   │   └── 🌐 Footer.jsx
│   ├── 📁 pages/
│   │   └── 🌐 Home.jsx
│   └── 🐍 index.js
├── 📁 public/
│   └── 🌐 index.html
├── 📋 package.json
└── 📝 README.md

📊 Tổng kết:
   - Thư mục: 4
   - File: 7
   - Tổng cộng: 11 mục

Lưu kết quả ra file? (Y/n): Y
✅ Đã lưu vào: tree_my-project.txt
```

---

### 7. 🧹 clean-temp-files.py - Dọn dẹp file rác

**Mục đích:** Xóa file tạm, cache, và file không cần thiết.

**Tính năng:**
- ✅ Xóa file tạm (.tmp, .log, .bak, ...)
- ✅ Xóa thư mục cache (__pycache__, node_modules, ...)
- ✅ Tìm file lớn (>10MB)
- ✅ Tìm thư mục rỗng
- ✅ Hiển thị dung lượng giải phóng
- ✅ Xác nhận trước khi xóa

**Cách sử dụng:**

```bash
python tool/clean-temp-files.py
```

**Ví dụ:**

```
Nhập đường dẫn thư mục: D:\my-project
Chọn loại cần dọn dẹp: 5 (Tất cả)
Kích thước tối thiểu (MB): 10
```

**Kết quả:**
```
📄 Tìm thấy 25 file tạm (5.2 MB)
📁 Tìm thấy 3 thư mục cache (450.5 MB)
💾 Tìm thấy 2 file lớn (>10MB) (125.8 MB)
📂 Tìm thấy 5 thư mục rỗng

📊 Tổng kết:
   - Số lượng: 35 mục
   - Dung lượng: 581.5 MB

⚠️  CẢNH BÁO: Bạn sắp xóa 35 mục!
Xác nhận xóa? (YES): YES

✓ Xóa: temp_file.tmp (1.2 MB)
✓ Xóa: __pycache__/ (15.5 MB)
...

✅ Hoàn thành!
   - Đã xóa: 35/35 mục
   - Giải phóng: 581.5 MB
```

---

### 8. 📦 extract-archive.py - Giải nén file

**Mục đích:** Giải nén nhiều file nén cùng lúc.

**Tính năng:**
- ✅ Hỗ trợ ZIP, TAR, TAR.GZ, 7Z, RAR
- ✅ Giải nén 1 file hoặc hàng loạt
- ✅ Tự động tạo thư mục đích
- ✅ Hiển thị dung lượng trước/sau
- ✅ Xử lý nhiều định dạng

**Cách sử dụng:**

```bash
python tool/extract-archive.py
```

**Ví dụ 1: Giải nén 1 file**

```
Chọn chế độ: 1
Nhập đường dẫn file nén: D:\downloads\project.zip
Giải nén vào thư mục (Enter = project): [Enter]
```

**Kết quả:**
```
📦 Đang giải nén: project.zip
✅ Giải nén thành công!
   📁 Thư mục: D:\downloads\project
   📊 Kích thước nén: 45.2 MB
   📊 Kích thước giải nén: 125.5 MB
```

**Ví dụ 2: Giải nén hàng loạt**

```
Chọn chế độ: 2
Nhập đường dẫn thư mục chứa file nén: D:\archives
Giải nén vào thư mục (Enter = thư mục hiện tại): [Enter]
Giải nén 5 file? (Y/n): Y
```

**Kết quả:**
```
📦 file1.zip... ✅ (50.2 MB)
📦 file2.tar.gz... ✅ (35.8 MB)
📦 file3.7z... ✅ (28.5 MB)

✅ Hoàn thành!
   - Thành công: 3/5 file
   - Tổng kích thước: 114.5 MB
```

---

### 9. 🔎 duplicate-finder.py - Tìm file trùng lặp

**Mục đích:** Tìm và xóa file trùng lặp để tiết kiệm dung lượng.

**Tính năng:**
- ✅ Tìm bằng hash (MD5/SHA256) - chính xác
- ✅ Tìm bằng size - nhanh
- ✅ Hiển thị dung lượng lãng phí
- ✅ Xóa file trùng tự động
- ✅ Lưu báo cáo ra file

**Cách sử dụng:**

```bash
python tool/duplicate-finder.py
```

**Ví dụ:**

```
Nhập đường dẫn thư mục: D:\Photos
Tìm trong tất cả thư mục con? (Y/n): Y
Kích thước file tối thiểu (KB): 100
Chọn phương pháp tìm: 1 (MD5)
```

**Kết quả:**
```
🔍 Đang quét file và tính hash...
   Đã quét 500 file.

📊 Tìm thấy 15 nhóm file trùng lặp

Nhóm 1: 3 file (2.5 MB) - Lãng phí: 5.0 MB
   Hash: a1b2c3d4e5f6...
   - D:\Photos\vacation\IMG_001.jpg
   - D:\Photos\backup\IMG_001.jpg
   - D:\Photos\old\photo1.jpg

Nhóm 2: 2 file (1.8 MB) - Lãng phí: 1.8 MB
   ...

💾 Tổng dung lượng lãng phí: 15.5 MB

Lưu báo cáo ra file? (y/N): Y
✅ Đã lưu báo cáo: duplicate_report.txt

Xóa file trùng lặp? (y/N): Y
Chọn: 1 (Giữ file đầu tiên, xóa các file còn lại)
Xác nhận? (YES): YES

✅ Đã xóa 20/20 file
```

---

### 10. 📁 file-organizer.py - Sắp xếp file

**Mục đích:** Tổ chức file tự động theo loại, extension, hoặc ngày tháng.

**Tính năng:**
- ✅ Sắp xếp theo loại (Images, Videos, Documents, ...)
- ✅ Sắp xếp theo extension (.jpg, .mp4, ...)
- ✅ Sắp xếp theo ngày tháng (modification date)
- ✅ Chế độ copy hoặc move
- ✅ Xử lý trùng tên tự động

**Cách sử dụng:**

```bash
python tool/file-organizer.py
```

**Ví dụ 1: Sắp xếp theo loại**

```
Nhập đường dẫn thư mục: D:\Downloads
Chọn chế độ sắp xếp: 1 (Theo loại file)
Thư mục đích (Enter = Organized): [Enter]
Chọn hành động: 1 (Copy)
```

**Kết quả:**
```
✓ Copy: report.pdf → Documents/
✓ Copy: photo.jpg → Images/
✓ Copy: video.mp4 → Videos/
✓ Copy: song.mp3 → Audio/
✓ Copy: script.py → Code/

✅ Hoàn thành! Đã xử lý 50 file

📊 Thống kê theo loại:
   Images: 20 file
   Documents: 15 file
   Videos: 8 file
   Audio: 5 file
   Code: 2 file
```

**Ví dụ 2: Sắp xếp theo ngày**

```
Chọn chế độ sắp xếp: 3 (Theo ngày tháng)
Chọn định dạng ngày: 1 (Năm-Tháng: 2024-01)
```

**Kết quả:**
```
✓ Copy: file1.txt → 2024-10/
✓ Copy: file2.jpg → 2024-10/
✓ Copy: file3.pdf → 2024-09/

📊 Thống kê theo thời gian:
   2024-10: 25 file
   2024-09: 15 file
   2024-08: 10 file
```

---

### 11. 🔤 text-encoding-converter.py - Chuyển đổi encoding

**Mục đích:** Chuyển đổi encoding của file text.

**Tính năng:**
- ✅ Tự động phát hiện encoding
- ✅ Chuyển đổi UTF-8, Windows-1252, ISO-8859-1, ...
- ✅ Backup file gốc
- ✅ Xử lý hàng loạt file
- ✅ Hiển thị confidence khi detect

**Cách sử dụng:**

```bash
python tool/text-encoding-converter.py
```

**Ví dụ 1: Phát hiện encoding**

```
Nhập đường dẫn thư mục: D:\old-project
Chỉ xử lý file có đuôi (.txt .py): .txt .php
Xử lý tất cả thư mục con? (Y/n): Y
Chọn chế độ: 1 (Phát hiện encoding)
```

**Kết quả:**
```
🔍 Đang phát hiện encoding...

📄 file1.txt
   Encoding: windows-1252 (confidence: 95%)

📄 file2.txt
   Encoding: utf-8 (confidence: 99%)

📄 file3.txt
   Encoding: iso-8859-1 (confidence: 85%)

📊 Thống kê encoding:
   windows-1252: 15 file
   utf-8: 10 file
   iso-8859-1: 5 file
```

**Ví dụ 2: Chuyển đổi encoding**

```
Chọn chế độ: 2 (Chuyển đổi)
Encoding nguồn: auto
Encoding đích: utf-8
Tạo backup file gốc? (Y/n): Y
Xác nhận? (YES): YES
```

**Kết quả:**
```
📄 old_file.txt (detect: windows-1252, 95%)
   ✓ windows-1252 → utf-8

📄 legacy.php (detect: iso-8859-1, 88%)
   ✓ iso-8859-1 → utf-8

✅ Hoàn thành!
   - Chuyển đổi thành công: 25 file
   - Bỏ qua: 2 file
   - Lỗi: 0 file
```

**Encoding phổ biến:**
- `utf-8` - Unicode (khuyên dùng)
- `windows-1252` - Windows Western
- `iso-8859-1` - Latin-1
- `utf-16` - Unicode 16-bit
- `shift-jis` - Tiếng Nhật
- `gb2312` - Tiếng Trung giản thể

---

## 🔧 FAQ & Troubleshooting

### Câu hỏi thường gặp

**Q: Tool không chạy được, báo lỗi "ModuleNotFoundError"?**

A: Bạn chưa cài đặt thư viện. Chạy lệnh:
```bash
pip install -r requirements.txt
```

**Q: Làm sao để chạy tool trên Linux/Mac?**

A: Giống Windows, nhưng có thể cần thêm quyền execute:
```bash
chmod +x tool/*.py
python3 menu.py
```

**Q: Tool compress-images báo lỗi với một số ảnh?**

A: Một số ảnh có thể bị corrupt hoặc định dạng đặc biệt. Tool sẽ bỏ qua và tiếp tục với ảnh khác.

**Q: Có thể khôi phục file đã xóa bằng clean-temp-files không?**

A: Không. Hãy cẩn thận khi sử dụng chức năng xóa. Luôn kiểm tra danh sách trước khi xác nhận.

**Q: Tool copy-changed-files yêu cầu gì?**

A: Thư mục phải là Git repository và đã có commit.

**Q: Encoding converter không detect đúng?**

A: Nếu confidence thấp (<70%), hãy chỉ định encoding nguồn thủ công thay vì dùng "auto".

**Q: Tool có xóa file gốc không?**

A: Tùy thuộc vào chế độ:
- Copy mode: Giữ file gốc
- Move mode: Di chuyển file gốc
- Backup mode: Thường có tùy chọn tạo .bak file

**Q: Có thể thêm tool mới không?**

A: Có! Chỉ cần tạo file .py mới trong thư mục `tool/`, menu.py sẽ tự động nhận diện.

### Lỗi thường gặp

**Lỗi: "PermissionError: [Errno 13] Permission denied"**

Giải pháp:
- Chạy với quyền Administrator (Windows)
- Sử dụng `sudo` (Linux/Mac)
- Kiểm tra file có đang được mở bởi chương trình khác

**Lỗi: "UnicodeDecodeError"**

Giải pháp:
- Sử dụng tool text-encoding-converter để phát hiện encoding đúng
- Chỉ định encoding khi mở file

**Lỗi: "File already exists"**

Giải pháp:
- Xóa thư mục output cũ
- Đổi tên thư mục output
- Tool thường tạo tên với timestamp để tránh trùng

---

## 📝 Ghi chú

### Backup quan trọng
- Luôn backup dữ liệu quan trọng trước khi sử dụng tool
- Kiểm tra kỹ trước khi xác nhận xóa file
- Sử dụng chế độ Copy thay vì Move khi chưa chắc chắn

### Hiệu suất
- Với thư mục lớn, một số tool có thể chạy lâu (duplicate-finder, compress-images)
- Sử dụng min_size để bỏ qua file nhỏ và tăng tốc
- Tắt recursive nếu không cần quét thư mục con

### Bảo mật
- Không chia sẻ file cấu hình SSH (menu-ssh.py) chứa password
- Sử dụng SSH key thay vì password khi có thể
- Cẩn thận với tool find-and-replace trên file code

---

## 🤝 Đóng góp

Nếu bạn muốn thêm tool mới hoặc cải thiện tool hiện tại:

1. Tạo file `.py` mới trong thư mục `tool/`
2. Tuân thủ format:
   - Có hàm `main()`
   - Có hàm `print_header()` để hiển thị tiêu đề
   - Có try-except để bắt lỗi
   - Comment đầy đủ bằng tiếng Việt
3. Test kỹ trước khi sử dụng

---

## 📄 License

Free to use for personal and commercial projects.

---

## 👨‍💻 Tác giả

Phát triển bởi bạn với ❤️

---

## 📞 Liên hệ & Hỗ trợ

Nếu gặp vấn đề hoặc có đề xuất, hãy tạo issue hoặc liên hệ trực tiếp.

---

**Chúc bạn sử dụng tool hiệu quả! 🚀**

