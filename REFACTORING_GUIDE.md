# 🚀 Hướng Dẫn Sau Refactoring v2.1

## ✅ Những Gì Đã Thay Đổi

### 📦 Utils Package - Đã tách thành 3 modules

**Trước:**
```
utils/
├── common.py (451 dòng - TẤT CẢ functions)
├── logger.py
└── progress.py
```

**Sau:**
```
utils/
├── format.py      (88 dòng - Format & Display)
├── validation.py  (175 dòng - Validation & Input)
├── file_ops.py    (155 dòng - File Operations)
├── logger.py
└── progress.py
```

### 📦 Menu Package - Đã tách ToolManager

**Trước:**
```
menu/
├── __init__.py (510 dòng - ToolManager + main)
└── ssh.py
```

**Sau:**
```
menu/
├── __init__.py        (220 dòng - main menu only)
├── tool_manager.py    (290 dòng - ToolManager class)
└── ssh.py
```

---

## 💻 Cách Import (Không Cần Thay Đổi Code Cũ!)

### Cách 1: Import từ package (KHUYẾN NGHỊ cho đơn giản)
```python
from utils import format_size, get_user_input, ProgressBar
from utils import get_file_list, safe_delete
```
✅ **Vẫn hoạt động như cũ!**

### Cách 2: Import trực tiếp từ module (KHUYẾN NGHỊ cho rõ ràng)
```python
# Format functions
from utils.format import format_size, print_header

# Validation functions
from utils.validation import get_user_input, confirm_action

# File operations
from utils.file_ops import get_file_list, safe_delete

# Progress
from utils.progress import ProgressBar

# Logger
from utils.logger import log_info, setup_logger
```

---

## 🎯 Khi Nào Dùng Module Nào?

### `utils.format` - Format & Display
Dùng khi cần:
- Format dung lượng file
- In header, separator
- Pluralize strings

```python
from utils.format import format_size, print_header

print_header("My Tool")
print(format_size(1024000))  # "1.00 MB"
```

### `utils.validation` - Validation & Input
Dùng khi cần:
- Lấy input từ người dùng
- Validate path
- Confirm actions
- Parse size strings

```python
from utils.validation import get_user_input, confirm_action

path = get_user_input("Nhập đường dẫn")
if confirm_action("Bạn có chắc muốn xóa?"):
    # Do something
```

### `utils.file_ops` - File Operations
Dùng khi cần:
- Lấy danh sách files
- Tính dung lượng folder
- Xóa files/folders
- Tạo directories

```python
from utils.file_ops import get_file_list, safe_delete

files = get_file_list("./images", extensions=['.jpg', '.png'])
success, error = safe_delete("old_file.txt")
```

---

## 📚 Thêm Function Mới

### Bước 1: Xác định chức năng
- Format/Display → `utils/format.py`
- Validation/Input → `utils/validation.py`
- File operations → `utils/file_ops.py`

### Bước 2: Thêm function vào file phù hợp
```python
# utils/format.py
def format_time(seconds: int) -> str:
    """Format thời gian"""
    minutes = seconds // 60
    return f"{minutes}m {seconds % 60}s"
```

### Bước 3: Export trong `utils/__init__.py`
```python
from .format import (
    format_size,
    print_header,
    format_time  # ✨ Thêm dòng này
)

__all__ = [
    'format_size',
    'print_header',
    'format_time',  # ✨ Thêm vào __all__
    # ...
]
```

### Bước 4: Sử dụng
```python
from utils import format_time
# hoặc
from utils.format import format_time
```

---

## 🔍 Tìm Function Nào Ở Đâu?

### Format & Display
| Function | Module | Mô tả |
|----------|--------|-------|
| `format_size()` | `utils.format` | Format dung lượng |
| `print_header()` | `utils.format` | In header |
| `print_separator()` | `utils.format` | In separator |
| `pluralize()` | `utils.format` | Pluralize strings |

### Validation & Input
| Function | Module | Mô tả |
|----------|--------|-------|
| `get_user_input()` | `utils.validation` | Lấy input |
| `normalize_path()` | `utils.validation` | Chuẩn hóa path |
| `confirm_action()` | `utils.validation` | Hỏi xác nhận |
| `validate_path()` | `utils.validation` | Validate path |
| `parse_size_string()` | `utils.validation` | Parse size |

### File Operations
| Function | Module | Mô tả |
|----------|--------|-------|
| `get_file_list()` | `utils.file_ops` | Lấy list files |
| `get_folder_size()` | `utils.file_ops` | Tính dung lượng |
| `safe_delete()` | `utils.file_ops` | Xóa an toàn |
| `ensure_directory_exists()` | `utils.file_ops` | Tạo thư mục |
| `create_backup_name()` | `utils.file_ops` | Tạo tên backup |
| `get_available_space()` | `utils.file_ops` | Dung lượng trống |

---

## 🧪 Testing

Tất cả imports đã được test và hoạt động tốt:

```bash
# Test utils imports
python -c "from utils import format_size, get_user_input, ProgressBar"
✅ OK

# Test direct imports
python -c "from utils.format import format_size; from utils.validation import get_user_input"
✅ OK

# Test menu imports
python -c "from menu import ToolManager, main"
✅ OK

# Test backward compatibility
python -c "from utils import format_size, print_header, get_user_input"
✅ OK
```

---

## 🎉 Kết Luận

### ✅ Ưu điểm
1. **Rõ ràng hơn**: Biết function nằm ở đâu dễ dàng
2. **Dễ maintain**: File nhỏ, dễ đọc và sửa
3. **Dễ mở rộng**: Thêm function mới vào đúng chỗ
4. **Backward compatible**: Code cũ vẫn chạy!

### 🚫 Không Cần Làm Gì
- ❌ KHÔNG cần sửa code cũ
- ❌ KHÔNG cần update imports
- ❌ KHÔNG breaking changes

### 💡 Khuyến Nghị
- ✅ Import trực tiếp từ module cho code mới (rõ ràng hơn)
- ✅ Đọc docstring để hiểu function
- ✅ Xem `REFACTORING.md` để biết chi tiết

---

**Happy Coding! 🚀**

_myPythonTool v2.1.0_

