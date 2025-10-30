# 🛠️ myPythonTool - Bộ Công Cụ Python Tiện Ích

[![GitHub](https://img.shields.io/badge/GitHub-VHN--DEV-blue?logo=github)](https://github.com/VHN-DEV/myPythonTool)
[![Python](https://img.shields.io/badge/Python-3.7+-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/VHN-DEV/myPythonTool?style=social)](https://github.com/VHN-DEV/myPythonTool/stargazers)

> Bộ công cụ Python đa năng giúp tự động hóa các tác vụ thường gặp khi làm việc với file và thư mục. Giao diện tiếng Việt thân thiện, dễ sử dụng!

> 👋 **Mới bắt đầu?** Xem [Quick Start](#-quick-start) hoặc đọc [INSTALL.md](docs/INSTALL.md) để cài đặt!

---

## 📑 Mục lục

- [🎯 Giới thiệu](#-giới-thiệu)
- [✨ Tính năng nổi bật](#-tính-năng-nổi-bật)
- [🚀 Quick Start](#-quick-start)
- [💾 Cài đặt chi tiết](#-cài-đặt-chi-tiết)
- [📦 Danh sách công cụ](#-danh-sách-công-cụ)
- [📖 Hướng dẫn chi tiết](#-hướng-dẫn-chi-tiết)
- [🔧 FAQ & Troubleshooting](#-faq--troubleshooting)
- [🤝 Đóng góp](#-đóng-góp)
- [📄 License](#-license)
- [👨‍💻 Tác giả](#-tác-giả)

---

## 🎯 Giới thiệu

**myPythonTool** là bộ công cụ Python được thiết kế để giúp bạn tiết kiệm thời gian trong các công việc xử lý file hàng ngày:

- 🖼️ Xử lý hình ảnh chuyên nghiệp
- 🔄 Quản lý file Git thông minh
- 📁 Tổ chức file tự động
- 🧹 Dọn dẹp và tối ưu hóa hệ thống
- 🔍 Tìm kiếm và thay thế mạnh mẽ
- 💾 Backup và nén dữ liệu
- 🌍 Hỗ trợ encoding đa ngôn ngữ

**Giao diện menu tiếng Việt** giúp bạn dễ dàng sử dụng mà không cần nhớ lệnh phức tạp!

---

## ✨ Tính năng nổi bật

### 🖼️ Xử lý Ảnh Chuyên Nghiệp
- Nén ảnh thông minh với quality tùy chỉnh
- Resize giữ nguyên tỉ lệ hoặc kích thước cụ thể
- Chuyển đổi định dạng (JPG, PNG, WEBP)
- Giới hạn dung lượng tối đa tự động

### 🔄 Quản lý Git Thông Minh
- Copy file thay đổi theo commit range
- Giữ nguyên cấu trúc thư mục
- Tạo danh sách file để upload lên server
- Verify commit trước khi thực hiện

### 📁 Tổ chức File Tự Động
- Sắp xếp theo loại (Images, Videos, Documents...)
- Sắp xếp theo extension (.jpg, .mp4, .pdf...)
- Sắp xếp theo ngày tháng (modification date)
- Chế độ copy an toàn hoặc move nhanh

### 🔍 Tìm Kiếm Mạnh Mẽ
- Tìm file trùng lặp bằng hash (MD5/SHA256)
- Tìm và thay thế text trong nhiều file
- Hỗ trợ Regular Expression
- Preview trước khi thay đổi

### 🧹 Dọn Dẹp Thông Minh
- Xóa file tạm và cache tự động
- Tìm file lớn và thư mục rỗng
- Hiển thị dung lượng giải phóng
- Xác nhận an toàn trước khi xóa

---

## 🚀 Quick Start

### Cách 1: Cài đặt toàn cục (Khuyến nghị) ⭐

Sau khi cài đặt, bạn có thể chạy `myptool` từ bất kỳ đâu!

#### Bước 1: Clone repository

```bash
git clone https://github.com/VHN-DEV/myPythonTool.git
cd myPythonTool
```

#### Bước 2: Cài đặt

```bash
pip install -e .
```

#### Bước 3: Chạy từ bất kỳ đâu! 🎉

```bash
# Có thể chạy từ bất kỳ thư mục nào
myptool
```

📖 **Chi tiết:** Xem [INSTALL.md](docs/INSTALL.md) để biết thêm cách cài đặt khác

---

### Cách 2: Chạy trực tiếp (Không cài đặt)

#### Bước 1: Clone repository

```bash
git clone https://github.com/VHN-DEV/myPythonTool.git
cd myPythonTool
```

#### Bước 2: Cài đặt thư viện

```bash
pip install -r requirements.txt
```

#### Bước 3: Chạy menu

```bash
python .
# Hoặc
python __main__.py
```

### Menu sẽ hiển thị:

```
===== Danh sách tool =====
0. Thoát
1. Sao lưu và nén thư mục (có timestamp)
2. Dọn dẹp file tạm, cache và file rác
3. Nén và chỉnh sửa ảnh (resize, đổi format)
4. Sao chép file thay đổi theo Git commit
5. Tìm và xóa file trùng lặp
6. Giải nén file (ZIP, RAR, 7Z, TAR)
7. Sắp xếp file (theo loại/ngày/extension)
8. Tìm và thay thế text trong nhiều file
9. Tạo sơ đồ cây thư mục dự án
10. Đổi tên file hàng loạt (prefix/suffix/số thứ tự)
11. Chuyển đổi encoding file text (UTF-8, ANSI...)
===========================

Chọn số để chạy tool:
```

**Đơn giản vậy thôi!** 🎉

---

## 💾 Cài đặt chi tiết

### Yêu cầu hệ thống

- **Python**: 3.7 trở lên
- **Hệ điều hành**: Windows, Linux, macOS
- **RAM**: 512MB (khuyến nghị 1GB+)
- **Dung lượng**: ~50MB

### Thư viện bắt buộc

```bash
pip install Pillow chardet
```

**Chi tiết:**
- `Pillow` (>=9.0.0) - Xử lý hình ảnh
- `chardet` (>=5.0.0) - Phát hiện encoding

### Thư viện tùy chọn (cho tính năng mở rộng)

```bash
pip install py7zr rarfile
```

**Chi tiết:**
- `py7zr` - Hỗ trợ giải nén file .7z
- `rarfile` - Hỗ trợ giải nén file .rar (cần cài WinRAR/unrar)

### Cài đặt từ requirements.txt

File `requirements.txt` đã bao gồm tất cả thư viện cần thiết:

```bash
pip install -r requirements.txt
```

### Kiểm tra cài đặt

```bash
python -c "import PIL, chardet; print('✅ Cài đặt thành công!')"
```

---

## 📦 Danh sách công cụ

| STT | Tên Tool | Mô tả chức năng | Thích hợp cho |
|-----|----------|----------------|---------------|
| 1 | **backup-folder.py** | Sao lưu và nén thư mục với timestamp | Backup dự án, tài liệu |
| 2 | **clean-temp-files.py** | Dọn dẹp file tạm, cache và file rác | Giải phóng dung lượng |
| 3 | **compress-images.py** | Nén và chỉnh sửa ảnh (resize, đổi format) | Web developer, nhiếp ảnh |
| 4 | **copy-changed-files.py** | Sao chép file thay đổi theo Git commit | Upload lên server |
| 5 | **duplicate-finder.py** | Tìm và xóa file trùng lặp | Dọn dẹp ổ cứng |
| 6 | **extract-archive.py** | Giải nén file (ZIP, RAR, 7Z, TAR) | Giải nén hàng loạt |
| 7 | **file-organizer.py** | Sắp xếp file theo loại/ngày/extension | Tổ chức Downloads |
| 8 | **find-and-replace.py** | Tìm và thay thế text trong nhiều file | Refactor code |
| 9 | **generate-tree.py** | Tạo sơ đồ cây thư mục dự án | Documentation |
| 10 | **rename-files.py** | Đổi tên file hàng loạt (prefix/suffix/số thứ tự) | Đổi tên ảnh, video |
| 11 | **text-encoding-converter.py** | Chuyển đổi encoding file text (UTF-8, ANSI...) | Fix lỗi tiếng Việt |

---

## 📖 Hướng dẫn chi tiết

### 1. 🖼️ Compress Images - Nén và chỉnh sửa ảnh

**Chức năng:**
- ✅ Nén ảnh với quality tùy chỉnh (1-100)
- ✅ Resize theo width/height hoặc giữ tỉ lệ
- ✅ Chuyển đổi định dạng (JPG, PNG, WEBP)
- ✅ Giới hạn dung lượng tối đa (KB)
- ✅ Tự động tối ưu hóa
- ✅ Tạo thư mục output với timestamp

**Cách sử dụng:**

```bash
python tool/compress-images.py
```

**Ví dụ thực tế:**

```
Nhập đường dẫn thư mục chứa ảnh: D:\Photos
Nhập đường dẫn thư mục đầu ra (Enter để mặc định): [Enter]
Nhập quality (mặc định 70): 80
Có bật optimize không? (Y/n): Y
Muốn đổi sang định dạng nào? (jpg, png, webp): webp
Nhập dung lượng tối đa mỗi ảnh (KB, Enter để bỏ qua): 500
Nhập chiều rộng (px, Enter để bỏ qua): 1920
Nhập chiều cao (px, Enter để bỏ qua): [Enter]
```

**Kết quả:**
```
✅ photo1.jpg | 2500.0KB → 450.2KB (q=80)
✅ photo2.png | 1800.5KB → 480.8KB (q=80)
✅ photo3.jpg | 3200.0KB → 495.5KB (q=75)

🎉 Hoàn thành nén ảnh! Ảnh đã được lưu tại: D:\Photos\compressed_20241029_143022
```

**Định dạng hỗ trợ:** JPG, JPEG, PNG, WEBP

**Use case phổ biến:**
- Tối ưu ảnh cho website (giảm thời gian load)
- Resize ảnh để upload lên mạng xã hội
- Chuyển đổi PNG sang WEBP (giảm 30-50% dung lượng)
- Giảm dung lượng album ảnh

---

### 2. 🔄 Copy Changed Files - Sao chép file thay đổi theo Git

**Chức năng:**
- ✅ Copy file theo commit range
- ✅ Giữ nguyên cấu trúc thư mục
- ✅ Bỏ qua file đã xóa
- ✅ Tạo danh sách file đã copy
- ✅ Verify commit ID trước khi thực hiện

**Cách sử dụng:**

```bash
python tool/copy-changed-files.py
```

**Ví dụ thực tế:**

```
Nhập đường dẫn dự án: C:\xampp\htdocs\my-ecommerce
Nhập commit ID bắt đầu (vd: 9d172f6): 9d172f6
Nhập commit ID kết thúc (Enter = HEAD): [Enter]
```

**Kết quả:**
```
🔍 Kiểm tra commit ID...
✓ Commit ID hợp lệ!

📂 Đang lấy danh sách file thay đổi từ commit 9d172f6 đến HEAD...
✓ Tìm thấy 15 file đã thay đổi

📋 Đang copy file...

✓ [OK] src/components/Header.jsx
✓ [OK] src/styles/main.css
✓ [OK] public/index.html
✓ [OK] api/products.php
... (11 file khác)

===================================================
✓ Hoàn tất!
- Đã copy: 15 file
- Bỏ qua: 0 file
- Thư mục xuất: changed-files-export
- Danh sách file: changed-files-export/danh-sach-file-thay-doi.txt

🚀 Bạn có thể upload toàn bộ thư mục 'changed-files-export' lên server bằng FileZilla!
===================================================
```

**Yêu cầu:** Thư mục phải là Git repository

**Use case phổ biến:**
- Upload file thay đổi lên shared hosting (không có Git)
- Tạo package update cho khách hàng
- Kiểm tra file đã sửa trước khi deploy
- Backup file quan trọng đã thay đổi

---

### 3. ✏️ Rename Files - Đổi tên file hàng loạt

**Chức năng:**
- ✅ Thêm prefix (tiền tố)
- ✅ Thêm suffix (hậu tố)
- ✅ Thay thế text trong tên
- ✅ Đổi tên theo số thứ tự (001, 002, 003...)
- ✅ Đổi phần mở rộng file
- ✅ Chuyển sang chữ thường
- ✅ Xóa/thay thế khoảng trắng

**Cách sử dụng:**

```bash
python tool/rename-files.py
```

**Ví dụ 1: Đổi tên theo số thứ tự**

```
Nhập đường dẫn thư mục: D:\Wedding_Photos
Chọn chức năng: 4 (Đổi tên file theo số thứ tự)
Chỉ xử lý file có đuôi (.jpg .png - Enter để xử lý tất cả): .jpg
Nhập tên cơ sở (vd: image): wedding
Bắt đầu từ số (vd: 1): 1
```

**Kết quả:**
```
📂 Thư mục: D:\Wedding_Photos
🔄 Bắt đầu đổi tên...

✓ DSC_5423.jpg → wedding_001.jpg
✓ DSC_5424.jpg → wedding_002.jpg
✓ DSC_5425.jpg → wedding_003.jpg
✓ IMG_9871.jpg → wedding_004.jpg
✓ IMG_9872.jpg → wedding_005.jpg

✅ Hoàn thành! Đã đổi tên 5 file.
```

**Ví dụ 2: Thêm prefix**

```
Chọn chức năng: 1 (Thêm prefix)
Nhập prefix (tiền tố): [Backup]_
```

**Kết quả:**
```
✓ document.pdf → [Backup]_document.pdf
✓ report.xlsx → [Backup]_report.xlsx
```

**Use case phổ biến:**
- Đổi tên ảnh chụp từ máy ảnh (DSC_xxx → tên có nghĩa)
- Thêm prefix cho file backup
- Xóa khoảng trắng trong tên file (tốt cho web server)
- Đổi extension hàng loạt (.jpeg → .jpg)

---

### 4. 💾 Backup Folder - Sao lưu và nén thư mục

**Chức năng:**
- ✅ Backup với tên file timestamp
- ✅ Nén file (ZIP, TAR, TAR.GZ)
- ✅ Backup có loại trừ (node_modules, .git, __pycache__...)
- ✅ Hiển thị tỷ lệ nén
- ✅ Tính toán dung lượng trước/sau

**Cách sử dụng:**

```bash
python tool/backup-folder.py
```

**Ví dụ:**

```
Nhập đường dẫn thư mục cần backup: D:\my-project
Nhập vị trí lưu backup (Enter để lưu tại thư mục hiện tại): D:\Backups

===== CHẾ ĐỘ BACKUP =====
1. Backup toàn bộ
2. Backup có loại trừ (exclude)

Chọn chế độ (1-2): 2

Nhập các pattern cần loại trừ (cách nhau bởi dấu phẩy): node_modules,.git,__pycache__

🚫 Loại trừ: node_modules, .git, __pycache__

🚀 Bắt đầu backup...

📦 Đang copy file...
📦 Đang nén...

✅ Backup thành công!
   💾 File backup: D:\Backups\my-project_backup_20241029_153045.zip
   📊 Kích thước: 45.20 MB

```

**Use case phổ biến:**
- Backup dự án trước khi refactor
- Tạo snapshot định kỳ
- Backup trước khi xóa file cũ
- Nén folder để gửi email/upload

---

### 5. 🔍 Find and Replace - Tìm và thay thế text

**Chức năng:**
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

**Ví dụ 1: Tìm kiếm (không thay đổi)**

```
Nhập đường dẫn thư mục: D:\my-react-project
Tìm kiếm trong tất cả thư mục con? (Y/n, mặc định Yes): Y
Chỉ xử lý file có đuôi (vd: .txt .py .js - Enter để xử lý tất cả): .js .jsx
Nhập text cần tìm: useState
Phân biệt chữ hoa/thường? (y/N, mặc định No): N
Sử dụng Regular Expression? (y/N, mặc định No): N

===== CHẾ ĐỘ =====
1. Chỉ tìm kiếm (không thay đổi file)
2. Tìm và thay thế

Chọn chế độ (1-2): 1
```

**Kết quả:**
```
🔍 Đang tìm kiếm...

📄 src/components/Counter.jsx
   Line 5: import { useState, useEffect } from 'react';
   Line 12: const [count, setCount] = useState(0);

📄 src/components/Form.jsx
   Line 8: const [name, setName] = useState('');
   Line 9: const [email, setEmail] = useState('');

📄 src/pages/Dashboard.jsx
   Line 15: const [data, setData] = useState([]);

============================================================
✅ Tìm thấy 5 kết quả trong 3 file
============================================================
```

**Ví dụ 2: Thay thế**

```
Nhập text cần tìm: var 
Nhập text thay thế: let 
Chọn chế độ (1-2): 2

⚠️  CẢNH BÁO: Bạn sắp thay thế trong nhiều file!
   Tìm: 'var '
   Thay bằng: 'let '

Xác nhận thực hiện? (YES để xác nhận): YES
```

**Kết quả:**
```
🔄 Đang thay thế...

✓ src/old-script.js - Thay thế 5 lần
✓ src/legacy.js - Thay thế 3 lần
✓ src/utils.js - Thay thế 2 lần

============================================================
✅ Đã thay thế 10 lần trong 3 file
============================================================
```

**Use case phổ biến:**
- Refactor code (đổi tên biến, function)
- Cập nhật URL/domain trong nhiều file
- Fix typo trong documentation
- Thay đổi config path hàng loạt

---

### 6. 🌳 Generate Tree - Tạo sơ đồ cây thư mục

**Chức năng:**
- ✅ Hiển thị cây thư mục với icon đẹp mắt
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
Nhập đường dẫn thư mục (Enter để dùng thư mục hiện tại): D:\my-project

Các thư mục/file cần bỏ qua (cách nhau bởi dấu phẩy, Enter để mặc định): [Enter]
Độ sâu tối đa (Enter để không giới hạn): 3
Hiển thị file/folder ẩn (bắt đầu bằng .)? (y/N): N
```

**Kết quả:**
```
🌳 Đang tạo cây thư mục...

============================================================
📂 my-project/
============================================================
├── 📁 src/
│   ├── 📁 components/
│   │   ├── 🌐 Header.jsx
│   │   ├── 🌐 Footer.jsx
│   │   └── 🌐 Sidebar.jsx
│   ├── 📁 pages/
│   │   ├── 🌐 Home.jsx
│   │   ├── 🌐 About.jsx
│   │   └── 🌐 Contact.jsx
│   ├── 📁 utils/
│   │   ├── 🐍 helpers.py
│   │   └── 🐍 validators.py
│   └── 📜 index.js
├── 📁 public/
│   ├── 🌐 index.html
│   ├── 🖼️ logo.png
│   └── 🎨 styles.css
├── 📋 package.json
├── 📝 README.md
└── 📄 .gitignore

============================================================
📊 Tổng kết:
   - Thư mục: 5
   - File: 14
   - Tổng cộng: 19 mục
============================================================

Lưu kết quả ra file? (Y/n): Y

✅ Đã lưu vào: tree_my-project.txt
```

**Use case phổ biến:**
- Tạo documentation cho dự án
- Chia sẻ cấu trúc dự án với team
- Include trong README.md
- Review cấu trúc trước khi refactor

---

### 7. 🧹 Clean Temp Files - Dọn dẹp file rác

**Chức năng:**
- ✅ Xóa file tạm (.tmp, .log, .bak, .cache...)
- ✅ Xóa thư mục cache (__pycache__, node_modules, .pytest_cache...)
- ✅ Tìm file lớn (>10MB tùy chỉnh)
- ✅ Tìm thư mục rỗng
- ✅ Hiển thị dung lượng giải phóng
- ✅ Xác nhận an toàn trước khi xóa

**Cách sử dụng:**

```bash
python tool/clean-temp-files.py
```

**Ví dụ:**

```
Nhập đường dẫn thư mục cần dọn dẹp (Enter để dùng thư mục hiện tại): D:\Projects

📂 Thư mục: D:\Projects

===== TÌM KIẾM FILE RÁC =====

1. File tạm (.tmp, .log, .bak, ...)
2. Thư mục cache (__pycache__, node_modules, ...)
3. File lớn (>10MB)
4. Thư mục rỗng
5. Tất cả các loại trên

Chọn loại cần dọn dẹp (1-5): 5

Kích thước tối thiểu (MB, mặc định 10): 50

🔍 Đang quét...

📄 Tìm thấy 45 file tạm (15.2 MB)
📁 Tìm thấy 8 thư mục cache (850.5 MB)
💾 Tìm thấy 3 file lớn (>50MB) (425.8 MB)
📂 Tìm thấy 12 thư mục rỗng

============================================================
📊 Tổng kết:
   - Số lượng: 68 mục
   - Dung lượng: 1.27 GB
============================================================

📋 Danh sách (10 mục đầu):
   - D:\Projects\project1\node_modules (450.5 MB)
   - D:\Projects\project2\build\temp.log (125.8 MB)
   - D:\Projects\old\backup.bak (200.0 MB)
   ... và 65 mục khác

⚠️  CẢNH BÁO: Bạn sắp xóa 68 mục!

Xác nhận xóa? (YES để xác nhận): YES

🗑️  Đang xóa...

✓ Xóa: node_modules/ (450.5 MB)
✓ Xóa: temp.log (125.8 MB)
✓ Xóa: __pycache__/ (15.2 MB)
...

============================================================
✅ Hoàn thành!
   - Đã xóa: 68/68 mục
   - Giải phóng: 1.27 GB
============================================================
```

**Use case phổ biến:**
- Giải phóng dung lượng ổ cứng
- Dọn dẹp thư mục Downloads
- Xóa file build/temp trong dự án
- Tìm và xóa file log cũ

---

### 8. 📦 Extract Archive - Giải nén file

**Chức năng:**
- ✅ Hỗ trợ nhiều định dạng (ZIP, TAR, TAR.GZ, 7Z, RAR)
- ✅ Giải nén 1 file hoặc hàng loạt
- ✅ Tự động tạo thư mục đích
- ✅ Hiển thị dung lượng trước/sau
- ✅ Xử lý nhiều file cùng lúc

**Cách sử dụng:**

```bash
python tool/extract-archive.py
```

**Ví dụ: Giải nén hàng loạt**

```
===== CHẾ ĐỘ =====
1. Giải nén 1 file
2. Giải nén tất cả file trong thư mục

Chọn chế độ (1-2): 2

Nhập đường dẫn thư mục chứa file nén: D:\Downloads\archives
Giải nén vào thư mục (Enter để dùng thư mục hiện tại): D:\Extracted

📦 Tìm thấy 5 file nén:
   1. project1.zip (50.2 MB)
   2. photos.tar.gz (125.8 MB)
   3. documents.7z (35.5 MB)
   4. backup.rar (80.3 MB)
   5. code.zip (15.7 MB)

Giải nén 5 file? (Y/n): Y

🚀 Bắt đầu giải nén...

📦 project1.zip... ✅ (145.5 MB)
📦 photos.tar.gz... ✅ (380.2 MB)
📦 documents.7z... ✅ (92.8 MB)
📦 backup.rar... ✅ (215.6 MB)
📦 code.zip... ✅ (45.3 MB)

============================================================
✅ Hoàn thành!
   - Thành công: 5/5 file
   - Tổng kích thước: 879.4 MB
============================================================
```

**Lưu ý:** 
- File .7z cần cài: `pip install py7zr`
- File .rar cần cài: `pip install rarfile` và WinRAR/unrar

**Use case phổ biến:**
- Giải nén nhiều file download cùng lúc
- Extract backup files
- Giải nén attachments hàng loạt
- Unpack project files

---

### 9. 🔎 Duplicate Finder - Tìm file trùng lặp

**Chức năng:**
- ✅ Tìm bằng hash (MD5/SHA256) - chính xác 100%
- ✅ Tìm bằng size - nhanh nhưng ước lượng
- ✅ Hiển thị dung lượng lãng phí
- ✅ Xóa file trùng tự động (giữ 1 file gốc)
- ✅ Lưu báo cáo ra file

**Cách sử dụng:**

```bash
python tool/duplicate-finder.py
```

**Ví dụ:**

```
Nhập đường dẫn thư mục: D:\Photos
Tìm trong tất cả thư mục con? (Y/n): Y
Kích thước file tối thiểu (KB, Enter để bỏ qua): 100

===== PHƯƠNG PHÁP TÌM =====
1. Theo hash (MD5) - Chính xác nhưng chậm
2. Theo hash (SHA256) - Chính xác hơn MD5
3. Theo kích thước - Nhanh nhưng không chính xác

Chọn phương pháp (1-3): 1

🔍 Đang quét file và tính hash...
   Đã quét 500 file.       

============================================================
📊 Tìm thấy 15 nhóm file trùng lặp
============================================================

Nhóm 1: 3 file (2.5 MB) - Lãng phí: 5.0 MB
   Hash: a1b2c3d4e5f6...
   - D:\Photos\vacation\IMG_001.jpg
   - D:\Photos\vacation\Copy of IMG_001.jpg
   - D:\Photos\backup\IMG_001.jpg

Nhóm 2: 2 file (1.8 MB) - Lãng phí: 1.8 MB
   Hash: f6e5d4c3b2a1...
   - D:\Photos\wedding\DSC_5423.jpg
   - D:\Photos\wedding\DSC_5423 (1).jpg

... và 13 nhóm khác

============================================================
💾 Tổng dung lượng lãng phí: 25.5 MB
============================================================

Lưu báo cáo ra file? (y/N): Y
✅ Đã lưu báo cáo: duplicate_report.txt

Xóa file trùng lặp? (y/N): Y

===== CHẾ ĐỘ XÓA TRÙNG LẶP =====
1. Giữ file đầu tiên, xóa các file còn lại
2. Chọn thủ công từng file
0. Không xóa

Chọn (0-2): 1

⚠️  CẢNH BÁO: Bạn sắp xóa 25 file trùng lặp!
Xác nhận? (YES để xác nhận): YES

✓ Xóa: D:\Photos\vacation\Copy of IMG_001.jpg
✓ Xóa: D:\Photos\backup\IMG_001.jpg
✓ Xóa: D:\Photos\wedding\DSC_5423 (1).jpg
...

✅ Đã xóa 25/25 file
```

**Use case phổ biến:**
- Dọn dẹp thư mục ảnh/video trùng lặp
- Tìm file backup trùng
- Giải phóng dung lượng ổ cứng
- Merge nhiều thư mục có file chung

---

### 10. 📁 File Organizer - Sắp xếp file tự động

**Chức năng:**
- ✅ Sắp xếp theo loại (Images, Videos, Documents, Code...)
- ✅ Sắp xếp theo extension (.jpg, .mp4, .pdf...)
- ✅ Sắp xếp theo ngày tháng (modification date)
- ✅ Chế độ copy (giữ file gốc) hoặc move (di chuyển)
- ✅ Xử lý trùng tên tự động
- ✅ Thống kê chi tiết

**Cách sử dụng:**

```bash
python tool/file-organizer.py
```

**Ví dụ 1: Sắp xếp theo loại**

```
Nhập đường dẫn thư mục cần sắp xếp: D:\Downloads

===== CHẾ ĐỘ SẮP XẾP =====
1. Theo loại file (Images, Videos, Documents, ...)
2. Theo đuôi file (.jpg, .mp4, .pdf, ...)
3. Theo ngày tháng (modification date)

Chọn chế độ (1-3): 1

Thư mục đích (Enter để tạo thư mục 'Organized' trong thư mục nguồn): [Enter]

===== HÀNH ĐỘNG =====
1. Copy (giữ nguyên file gốc)
2. Move (di chuyển file)

Chọn (1-2): 1

📂 Thư mục nguồn: D:\Downloads
📂 Thư mục đích: D:\Downloads\Organized
🔄 Chế độ: COPY

🚀 Bắt đầu sắp xếp...

✓ Copy: report.pdf → Documents/
✓ Copy: photo1.jpg → Images/
✓ Copy: video.mp4 → Videos/
✓ Copy: song.mp3 → Audio/
✓ Copy: setup.exe → Executables/
✓ Copy: script.py → Code/
✓ Copy: archive.zip → Archives/
... (và 43 file khác)

============================================================
✅ Hoàn thành! Đã xử lý 50 file
============================================================

📊 Thống kê theo loại:
   Images: 20 file
   Documents: 15 file
   Videos: 8 file
   Audio: 5 file
   Archives: 2 file
   Code: 2 file
   Executables: 1 file
   Others: 0 file
```

**Ví dụ 2: Sắp xếp theo ngày**

```
Chọn chế độ (1-3): 3

===== ĐỊNH DẠNG NGÀY =====
1. Năm-Tháng (2024-01)
2. Năm-Tháng-Ngày (2024-01-15)
3. Chỉ năm (2024)

Chọn (1-3): 1

🚀 Bắt đầu sắp xếp theo ngày...

✓ Copy: file1.txt → 2024-10/
✓ Copy: photo.jpg → 2024-10/
✓ Copy: old_doc.pdf → 2024-09/
✓ Copy: backup.zip → 2024-08/
...

============================================================
✅ Hoàn thành! Đã xử lý 50 file
============================================================

📊 Thống kê theo thời gian:
   2024-10: 25 file
   2024-09: 15 file
   2024-08: 10 file
```

**Use case phổ biến:**
- Dọn dẹp thư mục Downloads lộn xộn
- Tổ chức ảnh/video theo năm tháng
- Sắp xếp file project theo loại
- Chuẩn bị file để archive

---

### 11. 🔤 Text Encoding Converter - Chuyển đổi encoding

**Chức năng:**
- ✅ Tự động phát hiện encoding hiện tại
- ✅ Chuyển đổi sang UTF-8, Windows-1252, ISO-8859-1...
- ✅ Backup file gốc (.bak)
- ✅ Xử lý hàng loạt file
- ✅ Hiển thị confidence khi detect
- ✅ Xử lý đệ quy thư mục con

**Cách sử dụng:**

```bash
python tool/text-encoding-converter.py
```

**Ví dụ 1: Phát hiện encoding**

```
Nhập đường dẫn thư mục: D:\old-php-project
Chỉ xử lý file có đuôi (vd: .txt .py .js - Enter để xử lý tất cả): .php .txt
Xử lý tất cả thư mục con? (Y/n): Y

===== CHẾ ĐỘ =====
1. Phát hiện encoding (không thay đổi file)
2. Chuyển đổi encoding

Chọn chế độ (1-2): 1

🔍 Đang phát hiện encoding...

📄 index.php
   Encoding: windows-1252 (confidence: 95%)

📄 config.php
   Encoding: iso-8859-1 (confidence: 88%)

📄atabase.php
   Encoding: utf-8 (confidence: 99%)

📄 readme.txt
   Encoding: windows-1252 (confidence: 92%)

... (và 20 file khác)

============================================================
📊 Thống kê encoding:
   windows-1252: 15 file
   utf-8: 8 file
   iso-8859-1: 5 file
============================================================
```

**Ví dụ 2: Chuyển đổi encoding**

```
Chọn chế độ (1-2): 2

===== ENCODING NGUỒN =====
Nhập encoding nguồn (vd: utf-8, windows-1252, iso-8859-1)
Hoặc nhập 'auto' để tự động phát hiện

Encoding nguồn: auto

===== ENCODING ĐÍCH =====
Các encoding phổ biến:
  - utf-8 (khuyên dùng)
  - utf-16
  - windows-1252 (Windows Western)
  - iso-8859-1 (Latin-1)

Encoding đích: utf-8

Tạo backup file gốc (.bak)? (Y/n): Y

⚠️  CẢNH BÁO: Bạn sắp thay đổi encoding của nhiều file!
   Từ: auto
   Sang: utf-8
   Backup: Có

Xác nhận? (YES để xác nhận): YES

🔄 Bắt đầu chuyển đổi...

📄 index.php (detect: windows-1252, 95%)
   ✓ windows-1252 → utf-8

📄 config.php (detect: iso-8859-1, 88%)
   ✓ iso-8859-1 → utf-8

📄 database.php (detect: utf-8, 99%)
   ✓ utf-8 → utf-8 (không thay đổi)

... (và 20 file khác)

============================================================
✅ Hoàn thành!
   - Chuyển đổi thành công: 25 file
   - Bỏ qua: 2 file
   - Lỗi: 0 file
============================================================
```

**Encoding phổ biến:**
- `utf-8` - Unicode (khuyên dùng cho mọi dự án mới)
- `windows-1252` - Windows Western/Latin (file cũ trên Windows)
- `iso-8859-1` - Latin-1 (file cũ trên Linux/Unix)
- `utf-16` - Unicode 16-bit
- `shift-jis` - Tiếng Nhật
- `gb2312` - Tiếng Trung giản thể

**Use case phổ biến:**
- Fix lỗi hiển thị tiếng Việt (ÄÃ¡ → Đã)
- Chuyển project cũ sang UTF-8
- Chuẩn hóa encoding cho toàn bộ project
- Fix file PHP/HTML cũ bị lỗi font

---

## 🔧 FAQ & Troubleshooting

### ❓ Câu hỏi thường gặp

**Q: Tool không chạy được, báo lỗi "ModuleNotFoundError: No module named 'PIL'"?**

A: Bạn chưa cài đặt thư viện. Chạy lệnh:
```bash
pip install -r requirements.txt
```
Hoặc cài riêng:
```bash
pip install Pillow chardet
```

---

**Q: Làm sao để chạy tool trên Linux/macOS?**

A: Giống Windows, nhưng có thể cần:
```bash
# Cấp quyền execute
chmod +x tool/*.py

# Chạy với python3
python3 menu.py
```

---

**Q: Tool compress-images báo lỗi với một số ảnh?**

A: Một số ảnh có thể bị corrupt hoặc định dạng đặc biệt. Tool sẽ bỏ qua và tiếp tục với ảnh khác. Kiểm tra ảnh bị lỗi bằng viewer khác.

---

**Q: Có thể khôi phục file đã xóa bằng clean-temp-files không?**

A: Không. Hãy cẩn thận khi sử dụng chức năng xóa. Luôn:
- ✅ Kiểm tra danh sách trước khi xác nhận
- ✅ Backup quan trọng trước
- ✅ Chỉ xóa file tạm, không xóa file quan trọng

---

**Q: Tool copy-changed-files yêu cầu gì?**

A: Thư mục phải:
1. Là Git repository (đã chạy `git init`)
2. Có ít nhất 1 commit
3. Commit ID phải hợp lệ

Kiểm tra: `git log --oneline -10`

---

**Q: Encoding converter không detect đúng?**

A: Nếu confidence thấp (<70%), hãy:
1. Chỉ định encoding nguồn thủ công
2. Thử detect bằng tool khác
3. Xem file bằng text editor có hỗ trợ encoding

---

**Q: Tool có xóa file gốc không?**

A: Tùy thuộc vào chế độ:
- **Copy mode**: Giữ file gốc, tạo bản copy mới
- **Move mode**: Di chuyển file (xóa ở vị trí cũ)
- **Backup mode**: Thường có tùy chọn tạo .bak file
- Luôn đọc kỹ xác nhận trước khi chạy!

---

**Q: Có thể thêm tool mới không?**

A: Có! Rất đơn giản:
1. Tạo file `.py` mới trong thư mục `tool/`
2. Viết code với hàm `main()`
3. `menu.py` sẽ tự động nhận diện tool mới

Template:
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: Mô tả tool của bạn
"""

def main():
    print("Tool của tôi!")
    # Code của bạn ở đây

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Đã hủy!")
```

---

**Q: Tool chạy chậm với thư mục lớn?**

A: Tối ưu hóa:
- ✅ Tắt recursive nếu không cần (`recursive = False`)
- ✅ Đặt `min_size` để bỏ qua file nhỏ
- ✅ Loại trừ thư mục không cần (node_modules, .git...)
- ✅ Chạy trên SSD thay vì HDD

---

### ⚠️ Lỗi thường gặp

**Lỗi: "PermissionError: [Errno 13] Permission denied"**

**Nguyên nhân:**
- File đang được mở bởi chương trình khác
- Không có quyền ghi vào thư mục
- File bị read-only

**Giải pháp:**
```bash
# Windows: Chạy với quyền Administrator
# Linux/Mac: Sử dụng sudo
sudo python tool/clean-temp-files.py

# Hoặc thay đổi quyền
chmod 777 /path/to/folder
```

---

**Lỗi: "UnicodeDecodeError: 'utf-8' codec can't decode byte..."**

**Nguyên nhân:** File không phải encoding UTF-8

**Giải pháp:**
```bash
# Dùng tool để phát hiện encoding
python tool/text-encoding-converter.py

# Chọn chế độ 1 để detect
# Sau đó chọn chế độ 2 để convert sang UTF-8
```

---

**Lỗi: "File already exists"**

**Nguyên nhân:** Thư mục output đã tồn tại

**Giải pháp:**
- Xóa thư mục cũ
- Đổi tên thư mục output
- Tool thường tự tạo tên với timestamp

---

**Lỗi: "OSError: [Errno 28] No space left on device"**

**Nguyên nhân:** Ổ đĩa đầy

**Giải pháp:**
```bash
# Kiểm tra dung lượng
df -h  # Linux/Mac
wmic logicaldisk get size,freespace,caption  # Windows

# Dọn dẹp trước
python tool/clean-temp-files.py
```

---

**Lỗi: "ImportError: cannot import name 'Image' from 'PIL'"**

**Nguyên nhân:** Pillow bị lỗi hoặc chưa cài đúng

**Giải pháp:**
```bash
# Gỡ và cài lại
pip uninstall Pillow
pip install Pillow --upgrade
```

---

## 📝 Tips & Best Practices

### 💡 Mẹo sử dụng hiệu quả

1. **Backup trước khi xóa**
   - Luôn backup dữ liệu quan trọng
   - Sử dụng `backup-folder.py` trước khi chạy tool xóa file

2. **Test với thư mục nhỏ trước**
   - Chạy thử với 5-10 file trước
   - Kiểm tra kết quả
   - Mới chạy với toàn bộ thư mục lớn

3. **Sử dụng chế độ Copy thay vì Move**
   - An toàn hơn khi chưa chắc chắn
   - Có thể kiểm tra trước khi xóa file gốc

4. **Đọc kỹ xác nhận**
   - Không spam "YES" mà không đọc
   - Kiểm tra số lượng file sẽ bị ảnh hưởng
   - Xem danh sách 10 file đầu

5. **Sử dụng exclude pattern**
   - Loại trừ node_modules, .git, __pycache__
   - Tăng tốc độ xử lý
   - Tránh làm hỏng project

---

### 🎯 Workflow khuyến nghị

**Dọn dẹp thư mục Downloads:**
```
1. clean-temp-files.py (xóa file tạm)
2. duplicate-finder.py (xóa file trùng)
3. file-organizer.py (sắp xếp theo loại)
```

**Chuẩn bị dự án PHP cũ:**
```
1. text-encoding-converter.py (chuyển sang UTF-8)
2. find-and-replace.py (update đường dẫn)
3. backup-folder.py (backup trước khi deploy)
```

**Tối ưu ảnh cho website:**
```
1. rename-files.py (đổi tên có nghĩa)
2. compress-images.py (nén và resize)
3. file-organizer.py (sắp xếp theo năm/tháng)
```

**Deploy code lên shared hosting:**
```
1. copy-changed-files.py (lấy file thay đổi)
2. generate-tree.py (tạo log cấu trúc)
3. Upload thư mục changed-files-export
```

---

## 🤝 Đóng góp

Bạn muốn thêm tool mới hoặc cải thiện tool hiện tại? Rất hoan nghênh!

### Quy trình đóng góp:

1. **Fork repository**
   ```bash
   # Clone fork của bạn
   git clone https://github.com/YOUR_USERNAME/myPythonTool.git
   ```

2. **Tạo branch mới**
   ```bash
   git checkout -b feature/ten-tinh-nang-moi
   ```

3. **Viết code**
   - Tạo file `.py` trong thư mục `tool/`
   - Tuân thủ format chuẩn
   - Comment đầy đủ bằng tiếng Việt
   - Test kỹ trước khi commit

4. **Commit và push**
   ```bash
   git add .
   git commit -m "Add: Thêm tool xyz"
   git push origin feature/ten-tinh-nang-moi
   ```

5. **Tạo Pull Request**

### Template code tool mới:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: [Tên tool của bạn]
Mục đích: [Mô tả ngắn gọn]
"""

import os
from pathlib import Path


def print_header():
    """In header của tool"""
    print("=" * 60)
    print("  TOOL [TÊN TOOL]")
    print("=" * 60)
    print()


def main():
    """
    Hàm chính của tool
    
    Giải thích:
    - Bước 1: Nhập dữ liệu
    - Bước 2: Xử lý
    - Bước 3: Xuất kết quả
    """
    print_header()
    
    # Code của bạn ở đây
    print("Tool đang chạy...")
    

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Đã hủy!")
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
```

### Quy tắc code:

1. ✅ **Tên biến/hàm rõ ràng** (tiếng Việt không dấu hoặc tiếng Anh)
2. ✅ **Comment đầy đủ** (mục đích, lý do, giải thích)
3. ✅ **Xử lý lỗi** (try-except, validation input)
4. ✅ **User-friendly** (hướng dẫn rõ ràng, xác nhận trước khi xóa)
5. ✅ **Test kỹ** (với nhiều trường hợp khác nhau)

---

## 📄 License

MIT License - Free to use for personal and commercial projects.

```
Copyright (c) 2024 V.H.Nam

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 👨‍💻 Tác giả

**V.H.Nam** - Python Developer

- 🌐 GitHub: [@VHN-DEV](https://github.com/VHN-DEV)
- 📧 Email: vhnam18032002@gmail.com
- 🔗 Repository: [myPythonTool](https://github.com/VHN-DEV/myPythonTool)

---

## 📞 Liên hệ & Hỗ trợ

### Báo lỗi (Bug Report)

Nếu gặp lỗi, hãy tạo [Issue](https://github.com/VHN-DEV/myPythonTool/issues) với thông tin:
- 🐛 Mô tả lỗi
- 💻 Hệ điều hành & Python version
- 📋 Steps to reproduce
- 📸 Screenshot (nếu có)

### Đề xuất tính năng (Feature Request)

Có ý tưởng tool mới? Tạo [Issue](https://github.com/VHN-DEV/myPythonTool/issues) với label `enhancement`

### Hỗ trợ

- 📜 [CHANGELOG.md](docs/CHANGELOG.md) - Lịch sử thay đổi và phiên bản mới nhất
- 📖 [INSTALL.md](docs/INSTALL.md) - Hướng dẫn cài đặt chi tiết
- 🛠️ [tool/README.md](tool/README.md) - Hướng dẫn cấu trúc tool

---

## 🌟 Showcase

Tool này đã giúp:
- ✅ Tiết kiệm hàng giờ làm việc thủ công
- ✅ Tự động hóa workflow hàng ngày
- ✅ Dọn dẹp hàng chục GB dung lượng
- ✅ Xử lý hàng nghìn file một cách dễ dàng

### Bạn đã dùng tool này? 
⭐ Star repo nếu thấy hữu ích!  
🔄 Share cho bạn bè cần dùng!  
💬 Feedback để tool ngày càng tốt hơn!

---

## 📚 Tài liệu tham khảo

- [Python Documentation](https://docs.python.org/3/)
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [Git Documentation](https://git-scm.com/doc)

---

**🎉 Chúc bạn sử dụng tool hiệu quả! 🚀**

> "Automation is not about replacing people, it's about empowering them."

---

<div align="center">

**Made with ❤️ by V.H.Nam**

[⬆ Back to top](#-mypythontool---bộ-công-cụ-python-tiện-ích)

</div>
