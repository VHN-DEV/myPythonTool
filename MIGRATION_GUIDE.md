# 🔄 Migration Guide - Hướng dẫn cập nhật cấu trúc Tool

## 📋 Tổng quan

Từ phiên bản **2.2.0**, cấu trúc thư mục tools đã được tổ chức lại để mỗi tool có thư mục riêng.

## 🎯 Lý do thay đổi

### Vấn đề cũ:
- Tất cả file tools nằm chung trong 1 thư mục
- Khó quản lý khi tool có nhiều file (code, config, README...)
- File README_SSH.md nằm lẻ trong thư mục tool/

### Giải pháp mới:
- Mỗi tool có thư mục riêng
- Dễ thêm file phụ trợ cho từng tool
- Tổ chức rõ ràng, dễ bảo trì

## 📁 Cấu trúc mới

### Trước (v2.1.0):
```
tool/
├── backup-folder.py
├── clean-temp-files.py
├── compress-images.py
├── ...
└── README_SSH.md
```

### Sau (v2.2.0):
```
tool/
├── README.md                          # Hướng dẫn chung
├── backup-folder/
│   ├── __init__.py                    # Module init
│   ├── backup-folder.py               # Code chính
│   └── README.md                      # Hướng dẫn chi tiết
├── clean-temp-files/
│   ├── __init__.py
│   └── clean-temp-files.py
├── compress-images/
│   ├── __init__.py
│   ├── compress-images.py
│   └── README.md
├── ...
└── ssh-manager/
    ├── __init__.py
    ├── ssh-manager.py
    └── README.md                      # README_SSH.md đã được di chuyển vào đây
```

## ✅ Đã được tự động migrate

Migration đã được thực hiện tự động và bao gồm:

1. ✅ Tạo 15 thư mục riêng cho 15 tools
2. ✅ Di chuyển file .py vào thư mục tương ứng
3. ✅ Tạo `__init__.py` cho mỗi thư mục
4. ✅ Di chuyển `README_SSH.md` → `ssh-manager/README.md`
5. ✅ Cập nhật `menu/tool_manager.py` để hỗ trợ cấu trúc mới
6. ✅ Tạo README cho một số tools quan trọng

## 🔧 Thay đổi kỹ thuật

### Tool Manager (`menu/tool_manager.py`)

#### 1. Hàm `get_tool_list()`:
```python
# Cũ: Chỉ tìm file .py trực tiếp trong tool/
all_tools = [f for f in os.listdir(self.tool_dir) if f.endswith('.py')]

# Mới: Tìm cả trong thư mục con
for item in os.listdir(self.tool_dir):
    item_path = self.tool_dir / item
    if item_path.is_dir():
        main_file = item_path / f"{item}.py"
        if main_file.exists():
            all_tools.append(f"{item}.py")
```

#### 2. Hàm `_find_tool_path()` (Mới):
```python
def _find_tool_path(self, tool: str) -> Optional[Path]:
    """
    Tìm đường dẫn thực tế của tool
    
    Ưu tiên:
    1. Cấu trúc mới: tool/backup-folder/backup-folder.py
    2. Cấu trúc cũ: tool/backup-folder.py (backward compatible)
    """
```

## 🎯 Hướng dẫn thêm Tool mới

### Cách 1: Tạo thủ công

```bash
# 1. Tạo thư mục
mkdir tool/ten-tool-moi

# 2. Tạo __init__.py
echo '"""Tool: ten-tool-moi"""' > tool/ten-tool-moi/__init__.py

# 3. Tạo file chính
# Tên file phải giống tên thư mục
touch tool/ten-tool-moi/ten-tool-moi.py

# 4. (Optional) Tạo README
touch tool/ten-tool-moi/README.md
```

### Cách 2: Template nhanh

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: Ten Tool Moi
Mo ta: Công dụng của tool

Mục đích: Tại sao cần tool này
Lý do: Giải quyết vấn đề gì
"""

def main():
    """Hàm chính của tool"""
    print("Tool đang hoạt động!")

if __name__ == "__main__":
    main()
```

## 🔄 Backward Compatibility

### Vẫn hỗ trợ cấu trúc cũ

Nếu bạn vẫn có file `.py` nằm trực tiếp trong `tool/`, chúng vẫn hoạt động bình thường:

```
tool/
├── my-old-tool.py          # ✅ Vẫn hoạt động
├── backup-folder/          # ✅ Cấu trúc mới
│   └── backup-folder.py
```

**Lưu ý:** Khuyến khích migrate sang cấu trúc mới để dễ quản lý.

## 📊 Thống kê Migration

| Chỉ số | Giá trị |
|--------|---------|
| Tools đã migrate | 15/15 |
| Thư mục được tạo | 15 |
| `__init__.py` files | 15 |
| README.md mới | 4 |
| Breaking changes | 0 |
| Backward compatible | ✅ 100% |

## 🐛 Troubleshooting

### Tool không xuất hiện trong menu?

**Nguyên nhân:** Tên file không khớp với tên thư mục

```
❌ Sai:
tool/backup-folder/
    backup.py           # ← Sai tên

✅ Đúng:
tool/backup-folder/
    backup-folder.py    # ← Đúng tên
```

### Tool chạy báo lỗi import?

**Giải pháp:** Kiểm tra đường dẫn import trong code tool

```python
# Nếu tool có file phụ trợ
from pathlib import Path
import sys

# Thêm thư mục tool vào sys.path
tool_dir = Path(__file__).parent
sys.path.insert(0, str(tool_dir))

# Import từ file phụ trợ
from helpers import some_function
```

## 💡 Best Practices

### 1. Đặt tên rõ ràng
```
✅ Tốt:
- tool/image-resizer/
- tool/pdf-merger/
- tool/file-organizer/

❌ Tránh:
- tool/t1/
- tool/util/
- tool/misc/
```

### 2. Tổ chức file trong tool
```
tool/my-complex-tool/
├── __init__.py              # Module init
├── my-complex-tool.py       # Entry point
├── README.md                # Hướng dẫn
├── config.json              # Cấu hình (nếu cần)
├── helpers.py               # Hàm phụ trợ
└── tests.py                 # Unit tests (nếu có)
```

### 3. README.md template
```markdown
# Tool Name

## Mô tả
Mô tả ngắn gọn công dụng tool

## Tính năng
✅ Feature 1
✅ Feature 2

## Cách sử dụng
1. Bước 1
2. Bước 2

## Ví dụ
\```
Input: ...
Output: ...
\```

## Lưu ý
- Lưu ý 1
- Lưu ý 2
```

## 📚 Tài liệu liên quan

- `tool/README.md` - Hướng dẫn cấu trúc thư mục tool
- `CHANGELOG.md` - Lịch sử thay đổi chi tiết
- Các tool có README riêng:
  - `tool/backup-folder/README.md`
  - `tool/compress-images/README.md`
  - `tool/find-and-replace/README.md`
  - `tool/ssh-manager/README.md`

## 🎉 Kết luận

Migration đã hoàn tất thành công! Cấu trúc mới giúp:

- ✅ Tổ chức tốt hơn
- ✅ Dễ mở rộng
- ✅ Dễ bảo trì
- ✅ 100% backward compatible

Chúc bạn code vui vẻ! 🚀

