# ⚡ Quick Reference - Tra Cứu Nhanh

## 🎯 Chọn Tool Phù Hợp

| Bạn muốn... | Dùng tool | Command |
|------------|-----------|---------|
| Nén/resize ảnh | compress-images.py | `python tool/compress-images.py` |
| Upload code lên server | copy-changed-files.py | `python tool/copy-changed-files.py` |
| Đổi tên nhiều file | rename-files.py | `python tool/rename-files.py` |
| Backup dự án | backup-folder.py | `python tool/backup-folder.py` |
| Tìm/thay text trong file | find-and-replace.py | `python tool/find-and-replace.py` |
| Xem cấu trúc dự án | generate-tree.py | `python tool/generate-tree.py` |
| Dọn dẹp ổ đĩa | clean-temp-files.py | `python tool/clean-temp-files.py` |
| Giải nén nhiều file | extract-archive.py | `python tool/extract-archive.py` |
| Xóa file trùng | duplicate-finder.py | `python tool/duplicate-finder.py` |
| Sắp xếp file lộn xộn | file-organizer.py | `python tool/file-organizer.py` |
| Chuyển encoding UTF-8 | text-encoding-converter.py | `python tool/text-encoding-converter.py` |
| SSH vào server | menu-ssh.py | `python menu-ssh.py` |

---

## ⌨️ Commands Thường Dùng

```bash
# Cài đặt
pip install -r requirements.txt

# Chạy menu
python menu.py

# Update thư viện
pip install --upgrade -r requirements.txt

# Kiểm tra Python version
python --version
```

---

## 📋 Input Patterns Thường Gặp

### Đường dẫn có dấu cách
```
Nhập đường dẫn: D:\My Documents\Project
Hoặc: "D:\My Documents\Project"
```

### Extension multiple
```
Chỉ xử lý file: .jpg .png .gif
Hoặc: .py .js .jsx .tsx
```

### Pattern loại trừ
```
Loại trừ: node_modules, .git, __pycache__, dist
```

### Xác nhận quan trọng
```
Xác nhận? YES      ← Phải gõ chữ hoa
Xác nhận? (Y/n): Y ← Y hoặc Enter
```

---

## 🔧 Troubleshooting 1-Minute

| Lỗi | Giải pháp nhanh |
|-----|----------------|
| ModuleNotFoundError | `pip install -r requirements.txt` |
| Permission denied | Chạy as Administrator |
| UnicodeDecodeError | Dùng text-encoding-converter |
| File not found | Kiểm tra đường dẫn, dùng dấu ngoặc kép |
| Tool không hiện menu | Kiểm tra file .py trong thư mục tool/ |

---

## 💡 Tips & Tricks

### Tip 1: Test nhỏ trước
Thử với 2-3 file trước, sau đó mới chạy hàng loạt

### Tip 2: Dùng Copy thay vì Move
An toàn hơn, tránh mất file

### Tip 3: Check output folder
Thường tự động tạo với timestamp, không bị ghi đè

### Tip 4: Backup quan trọng
Đặc biệt với tool: clean, duplicate-finder, find-replace

### Tip 5: Regular Expression
Chỉ dùng khi bạn thực sự hiểu regex

---

## 📊 Performance Tips

| Tình huống | Giải pháp |
|-----------|-----------|
| Tool chạy chậm | Tắt recursive, dùng min_size |
| Thư mục quá lớn | Chia nhỏ ra hoặc loại trừ folder không cần |
| Hash lâu | Dùng phương pháp "theo size" thay vì hash |
| Memory cao | Xử lý từng thư mục con riêng lẻ |

---

## 🎨 Regex Examples (find-and-replace)

```regex
# Tìm email
[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}

# Tìm số điện thoại VN
(84|0[3|5|7|8|9])+([0-9]{8,9})

# Tìm URL
https?://[^\s]+

# Tìm IP address
\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b
```

---

## 🔐 SSH Config Example

Edit `menu-ssh.py`:

```python
servers = [
    {
        "name": "Server DEV",
        "user": "dev",
        "host": "192.168.10.163",
        "port": 1506,
        "password": None,
        "ssh_key": None
    },
    {
        "name": "Server PROD (key)",
        "user": "prod",
        "host": "192.168.10.250",
        "port": 22,
        "password": None,
        "ssh_key": r"D:\IT\keys\prod_id_rsa"
    }
]
```

---

## 📦 Common Workflows

### Workflow 1: Deploy Website
1. `copy-changed-files.py` - Lấy file đã sửa
2. `compress-images.py` - Nén ảnh mới (nếu có)
3. `menu-ssh.py` - Upload lên server

### Workflow 2: Organize Downloads
1. `clean-temp-files.py` - Xóa file tạm
2. `duplicate-finder.py` - Xóa file trùng
3. `file-organizer.py` - Sắp xếp file

### Workflow 3: Backup Project
1. `clean-temp-files.py` - Dọn cache trước
2. `backup-folder.py` - Backup dự án
3. Upload backup lên cloud

### Workflow 4: Refactor Code
1. `find-and-replace.py` - Đổi tên biến/hàm
2. `text-encoding-converter.py` - Chuẩn hóa encoding
3. Test lại code

---

## 📝 File Extensions Reference

### Images
`.jpg .jpeg .png .gif .bmp .svg .ico .webp .tiff`

### Videos
`.mp4 .avi .mkv .mov .wmv .flv .webm .m4v`

### Audio
`.mp3 .wav .flac .aac .ogg .wma .m4a`

### Documents
`.pdf .doc .docx .txt .rtf .odt .xls .xlsx .ppt .pptx`

### Archives
`.zip .rar .7z .tar .gz .bz2 .xz .iso`

### Code
`.py .js .java .cpp .c .h .cs .php .html .css .ts .jsx .tsx`

---

## 🚨 Safety Checklist

- [ ] Đã backup file quan trọng
- [ ] Đã test với vài file trước
- [ ] Đã đọc kỹ xác nhận trước khi YES
- [ ] Biết cách restore nếu có sự cố
- [ ] Đã kiểm tra free space nếu copy/backup
- [ ] Đã đóng file đang mở trong editor/app khác

---

## 📞 Quick Support

**Xem hướng dẫn đầy đủ:**
```
README.md          → Chi tiết từng tool
HUONG_DAN.txt      → Hướng dẫn tiếng Việt
QUICK_REFERENCE.md → File này
```

**Thư viện thiếu?**
```bash
pip install Pillow chardet
```

**Muốn thêm tool?**
Tạo file `.py` trong `tool/`, menu tự nhận

---

**Last updated:** 2024-10-29  
**Version:** 1.0

