# 📝 Changelog - Lịch Sử Thay Đổi

Tất cả các thay đổi quan trọng của dự án sẽ được ghi lại trong file này.

---

## [2.1.0] - 2025-10-30

### 🔧 Refactoring - Tối ưu cấu trúc code

Bản cập nhật này tập trung vào việc refactor và tối ưu cấu trúc code, tách các file lớn thành các module nhỏ hơn theo chức năng.

#### 📦 Utils Package - Refactored

**Tách `utils/common.py` (451 dòng) thành 3 modules:**

1. **`utils/format.py`** - Format & Display Functions
   - `format_size()` - Format dung lượng
   - `print_header()` - In header đẹp
   - `print_separator()` - In đường phân cách
   - `pluralize()` - Pluralize strings

2. **`utils/validation.py`** - Validation & Input Functions
   - `get_user_input()` - Lấy input từ người dùng
   - `normalize_path()` - Chuẩn hóa đường dẫn
   - `confirm_action()` - Hỏi xác nhận
   - `validate_path()` - Kiểm tra path
   - `parse_size_string()` - Parse size string

3. **`utils/file_ops.py`** - File Operations Functions
   - `get_file_list()` - Lấy danh sách file
   - `get_folder_size()` - Tính dung lượng
   - `safe_delete()` - Xóa an toàn
   - `ensure_directory_exists()` - Tạo thư mục
   - `create_backup_name()` - Tạo tên backup
   - `get_available_space()` - Dung lượng trống

#### 📦 Menu Package - Refactored

**Tách `menu/__init__.py` (510 dòng) thành 2 files:**

1. **`menu/tool_manager.py`** (290 dòng) - ToolManager Class
   - Quản lý tools, favorites, recent
   - Search & filter tools
   - Config persistence
   - Run tools

2. **`menu/__init__.py`** (220 dòng) - Main Menu
   - Entry point clean và gọn gàng
   - Main menu loop
   - Command dispatcher

#### 🎯 Lợi ích

- ✅ **Better Organization**: Mỗi module có một chức năng rõ ràng
- ✅ **Easier Maintenance**: File nhỏ hơn, dễ đọc và chỉnh sửa
- ✅ **Scalability**: Dễ thêm functions mới vào đúng module
- ✅ **Clean Code**: Tuân thủ Single Responsibility Principle
- ✅ **Backward Compatible**: Code cũ vẫn hoạt động 100%

#### 📊 Statistics

- ⬇️ Giảm avg lines/file: ~300 → ~160 (-47%)
- ⬆️ Tăng số modules: 5 → 8 (+3 files)
- ✅ No breaking changes

#### 📝 Files Changed

- ✨ NEW: `utils/format.py` (88 dòng)
- ✨ NEW: `utils/validation.py` (175 dòng)
- ✨ NEW: `utils/file_ops.py` (155 dòng)
- ✨ NEW: `menu/tool_manager.py` (290 dòng)
- 🔄 UPDATED: `utils/__init__.py` - Export từ các modules mới
- 🔄 UPDATED: `menu/__init__.py` - Chỉ giữ main function
- ❌ REMOVED: `utils/common.py` - Đã tách thành 3 modules
- 📄 NEW: `REFACTORING.md` - Documentation chi tiết

---

## [2.0.0] - 2025-10-30

### 🚀 Major Overhaul - Tối ưu hóa và Nâng cấp toàn diện

Đây là bản cập nhật lớn với việc refactor và tối ưu hóa toàn bộ codebase, thêm nhiều tính năng mới và cải thiện performance đáng kể.

#### ✨ Tính năng mới

**Utils Package - Thư viện tiện ích chung:**
- `utils/common.py` - Các hàm tiện ích dùng chung
  - `format_size()` - Format dung lượng dễ đọc
  - `print_header()` - In header đẹp
  - `get_user_input()` - Lấy input với validation
  - `confirm_action()` - Xác nhận thao tác nguy hiểm
  - `validate_path()` - Kiểm tra path hợp lệ
  - `get_file_list()` - Lấy danh sách file với filter
  - `get_folder_size()` - Tính dung lượng thư mục
  - `safe_delete()` - Xóa file/folder an toàn
  - `parse_size_string()` - Parse chuỗi size (vd: "10MB")

- `utils/progress.py` - Progress tracking
  - `ProgressBar` class - Progress bar đẹp với ETA
  - `Spinner` class - Spinner animation
  - `simple_progress()` - Progress generator đơn giản

- `utils/logger.py` - Logging system
  - `setup_logger()` - Setup logger với config linh hoạt
  - `log_info()`, `log_error()`, `log_warning()` - Wrapper functions
  - Tự động ghi log ra file với rotation
  - Log format rõ ràng, dễ đọc

**Config System:**
- `config.py` - Cấu hình tập trung
  - Tất cả settings ở một nơi
  - Dễ customize và maintain
  - Load/save config từ/ra file JSON
  - Auto-create directories cần thiết
  - Constants cho paths, extensions, defaults

**Menu System Upgrade:**
- `menu.py` - Menu nâng cao
  - ⭐ Favorites system - Đánh dấu tools yêu thích
  - 📚 Recent tools - Lịch sử tools đã dùng
  - 🔍 Search tools - Tìm kiếm theo keyword/tags
  - Config persistence - Lưu settings
  - Better UI với box drawing characters
  - Shortcuts cho các thao tác thường dùng

#### 🔧 Tools được tối ưu hóa

**compress-images.py v2.0:**
- ⚡ Multiprocessing - Xử lý song song nhiều ảnh
- 📊 Progress bar với ETA
- 🎯 CLI mode với argparse
- 📝 Logging đầy đủ
- ✅ Better error handling
- 🔄 Refactor code structure
- 🎨 RGB conversion cho JPEG
- 📐 Smart resize với aspect ratio

**backup-folder.py v2.0:**
- 📋 BackupManager class - OOP design
- 📊 Progress bar cho copy files
- 💾 Metadata tracking - Lưu lịch sử backup
- 🔍 List previous backups
- 🔄 Restore from backup
- ⚙️ CLI mode với argparse
- 🚫 Better exclude patterns
- 📝 Logging đầy đủ

**duplicate-finder.py v2.0:**
- ⚡ Multiprocessing cho hash calculation
- 🎯 Smart algorithm - Filter theo size trước
- 📊 Progress bar với ETA
- 🗑️ Multiple delete modes:
  - Giữ file đầu tiên
  - Giữ file mới nhất
  - Giữ file cũ nhất
- 📝 Export report ra file
- ⚙️ CLI mode với argparse
- 📈 Better statistics display

#### 🎨 Cải thiện UX

**Progress Tracking:**
- Progress bar với ETA cho tất cả thao tác lâu
- Spinner animation cho thao tác không biết thời gian
- Real-time status updates
- Format đẹp, dễ đọc

**Error Handling:**
- Try-catch đầy đủ
- Error messages chi tiết hơn
- Graceful degradation
- Logging errors để debug

**Input Validation:**
- Validate paths, sizes, numbers
- Clear error messages
- Default values hợp lý
- Strip quotes tự động

**Confirmations:**
- Confirm cho thao tác nguy hiểm
- Require "YES" cho thao tác rất nguy hiểm
- Preview trước khi thực hiện
- Dry-run mode (sẽ thêm sau)

#### 🚀 Performance

**Multiprocessing:**
- Compress images song song
- Hash files song song cho duplicate finder
- Auto-detect số CPU cores
- Configurable max workers

**Optimizations:**
- Smart filtering (size trước, hash sau)
- Buffer size optimization
- Chunk reading cho file lớn
- Early exit khi có thể

**Memory Management:**
- Không load toàn bộ file vào RAM
- Stream processing
- Generator cho iteration
- Cleanup resources properly

#### 📚 Documentation

**Code Documentation:**
- Docstrings đầy đủ cho tất cả functions/classes
- Type hints cho parameters và returns
- Giải thích logic phức tạp
- Examples trong docstring

**User Documentation:**
- Help command trong menu
- CLI --help cho mỗi tool
- Clear error messages
- CHANGELOG.md chi tiết

#### 🛠️ Technical Improvements

**Code Quality:**
- DRY principle - Không lặp code
- OOP design cho tools phức tạp
- Separation of concerns
- Consistent naming conventions
- Better project structure

**Maintainability:**
- Centralized config
- Shared utilities
- Modular design
- Easy to extend

**Testing Ready:**
- Testable functions
- Separated logic và I/O
- Clear interfaces
- Mock-friendly design

#### 🐛 Bug Fixes

- Fix encoding issues khi đọc file
- Fix progress bar không hiển thị đúng
- Fix memory leak khi xử lý nhiều file
- Fix crash khi file không có quyền truy cập
- Fix path handling trên Windows

#### 📦 Dependencies

Không thêm dependency mới, tất cả utils đều pure Python.

#### ⚠️ Breaking Changes

**Menu System:**
- Command shortcuts đã thay đổi
- Config file format mới (tool_config.json)

**Tools:**
- Một số tool có thêm CLI arguments
- Log files giờ lưu trong thư mục `logs/`
- Output mặc định trong thư mục `output/`

#### 🔮 Roadmap (Coming Soon)

- [ ] Tối ưu file-organizer.py với undo feature
- [ ] Nâng cấp find-and-replace.py với preview
- [ ] Thêm batch preview cho image-watermark.py
- [ ] Unit tests cho utils
- [ ] Configuration UI
- [ ] Plugin system

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

