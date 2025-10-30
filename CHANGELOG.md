# 📝 Changelog - Lịch Sử Thay Đổi

Tất cả các thay đổi quan trọng của dự án sẽ được ghi lại trong file này.

---

## [1.1.0] - 2024-10-30

### 🎉 Major Update - 3 Tools mới cao cấp

#### ✨ Tools mới (3)

**PDF Processing:**
- `pdf-tools.py` - Xử lý PDF chuyên nghiệp
  - Merge: Gộp nhiều PDF thành 1
  - Split: Tách PDF theo trang hoặc range
  - Compress: Nén PDF giảm dung lượng
  - PDF to Images: Chuyển PDF sang PNG/JPEG
  - Rotate: Xoay trang PDF
  - Extract Text: Trích xuất text từ PDF
  - Info: Xem metadata và thông tin PDF

**Image Watermarking:**
- `image-watermark.py` - Thêm watermark vào ảnh
  - Text watermark với font, size, color tùy chỉnh
  - Image watermark (logo) với transparency
  - 9 vị trí đặt watermark (góc, cạnh, center)
  - Opacity control (0-255)
  - Batch processing hàng loạt
  - Template system lưu/tái sử dụng config

**Video Processing:**
- `video-converter.py` - Xử lý video chuyên nghiệp
  - Convert format: MP4, AVI, MKV, WEBM, MOV
  - Compress: Nén video với quality control
  - Trim: Cắt video theo time range
  - Extract Audio: Trích xuất audio (MP3/WAV/AAC)
  - Change Resolution: 1080p, 720p, 480p, custom
  - Video Info: Hiển thị thông tin chi tiết
  - Batch Convert: Xử lý nhiều video cùng lúc

#### 📚 Thư viện mới

- `PyPDF2` >= 3.0.0 - PDF processing
- `pdf2image` >= 1.16.0 - PDF to image conversion
- `moviepy` >= 1.0.3 - Video processing

#### 🔧 Cải tiến

- Cập nhật menu.py với tên hiển thị chi tiết hơn
- Documentation đầy đủ cho 3 tools mới
- Error handling tốt hơn
- Progress tracking cho các tác vụ dài

#### 📊 Thống kê

- **Tổng số tools**: 14 (tăng từ 11)
- **Tổng dòng code**: ~15,000+ lines
- **Tools mới**: 3 (PDF, Image, Video)
- **Dependencies mới**: 3 packages

---

## [1.0.0] - 2024-10-29

### 🎉 Phiên bản đầu tiên

#### ✨ Công cụ mới (11 tools)

**Xử lý File & Media:**
- `compress-images.py` - Nén, resize và chuyển đổi định dạng ảnh
- `extract-archive.py` - Giải nén nhiều file nén (ZIP, RAR, 7Z, TAR)
- `duplicate-finder.py` - Tìm và xóa file trùng lặp bằng hash

**Quản lý & Tổ chức:**
- `file-organizer.py` - Sắp xếp file theo loại, extension hoặc ngày
- `rename-files.py` - Đổi tên hàng loạt file (7 chế độ)
- `backup-folder.py` - Backup thư mục với nén và timestamp

**Developer Tools:**
- `copy-changed-files.py` - Copy file thay đổi theo Git commit
- `find-and-replace.py` - Tìm và thay thế text trong nhiều file
- `text-encoding-converter.py` - Chuyển đổi encoding (auto-detect)
- `generate-tree.py` - Tạo cây thư mục với icon

**Maintenance:**
- `clean-temp-files.py` - Dọn dẹp file tạm, cache và file rác

**Tiện ích khác:**
- `menu-ssh.py` - Menu SSH nhanh vào server

#### 📚 Tài liệu
- `README.md` - Hướng dẫn chi tiết đầy đủ
- `HUONG_DAN.txt` - Hướng dẫn ngắn gọn tiếng Việt
- `QUICK_REFERENCE.md` - Tra cứu nhanh
- `CHANGELOG.md` - File này
- `requirements.txt` - Danh sách thư viện

#### 🎨 Tính năng chung
- Menu tự động phát hiện tool trong thư mục
- Giao diện tiếng Việt
- Xác nhận trước các thao tác nguy hiểm
- Hỗ trợ đường dẫn có dấu cách
- Error handling đầy đủ
- Progress indicator cho các tác vụ dài

#### 🔧 Kỹ thuật
- Python 3.7+
- Thư viện: Pillow, chardet
- Hỗ trợ Windows, Linux, macOS
- Không cần database
- Standalone tools, chạy độc lập

---

## [Unreleased] - Dự kiến

### 🚀 Tính năng sẽ thêm

#### Tools mới
- [ ] `video-converter.py` - Chuyển đổi định dạng video
- [ ] `pdf-tools.py` - Merge, split, compress PDF
- [ ] `image-watermark.py` - Thêm watermark hàng loạt
- [ ] `file-sync.py` - Đồng bộ 2 thư mục
- [ ] `disk-analyzer.py` - Phân tích dung lượng ổ đĩa
- [ ] `metadata-editor.py` - Sửa metadata ảnh/video

#### Cải tiến
- [ ] GUI version với tkinter
- [ ] Progress bar đẹp hơn
- [ ] Multi-threading cho tốc độ
- [ ] Config file để lưu settings
- [ ] Log file chi tiết
- [ ] Undo functionality
- [ ] Dry-run mode (preview)
- [ ] Scheduler cho auto backup

#### Tài liệu
- [ ] Video tutorial
- [ ] Screenshots cho mỗi tool
- [ ] FAQ mở rộng
- [ ] Troubleshooting guide chi tiết
- [ ] Best practices

---

## 📋 Template cho phiên bản mới

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added (Thêm mới)
- Tính năng mới

### Changed (Thay đổi)
- Cải tiến tính năng cũ

### Fixed (Sửa lỗi)
- Bug fixes

### Removed (Xóa bỏ)
- Tính năng đã loại bỏ

### Security (Bảo mật)
- Cập nhật bảo mật
```

---

## 🤝 Đóng góp

Mọi đóng góp đều được hoan nghênh! Nếu bạn thêm tool mới hoặc cải tiến, vui lòng:

1. Cập nhật CHANGELOG.md
2. Test kỹ trước khi commit
3. Thêm docstring đầy đủ
4. Cập nhật README.md nếu cần

---

## 📌 Ghi chú phiên bản

Format: `[major.minor.patch]`

- **major**: Thay đổi lớn, không tương thích ngược
- **minor**: Thêm tính năng mới, tương thích ngược
- **patch**: Sửa lỗi, cải tiến nhỏ

---

**Phát triển bởi:** Bạn  
**License:** Free to use  
**Repository:** [Link to GitHub]

