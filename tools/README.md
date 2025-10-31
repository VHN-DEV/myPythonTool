# Thư mục Tools

## Cấu trúc

Mỗi tool nằm trong một thư mục riêng để dễ quản lý và mở rộng:

```
tools/
├── py/
│   ├── backup-folder/
│   │   ├── __init__.py
│   │   ├── backup-folder.py          # File chính của tool
│   │   ├── tool_info.json            # (Optional) Metadata của tool
│   │   ├── doc.py                    # (Optional) Hướng dẫn sử dụng
│   │   └── README.md                  # (Optional) Hướng dẫn chi tiết
│   └── ...
└── sh/
    ├── setup-project-linux/
    │   ├── __init__.py
    │   ├── setup-project-linux.py    # File chính của tool
    │   ├── tool_info.json            # (Optional) Metadata của tool
    │   ├── doc.py                    # (Optional) Hướng dẫn sử dụng
    │   └── app.sh                    # Script shell (nếu cần)
    └── ...
```

## Cách thêm tool mới

### Bước 1: Tạo thư mục tool

Tạo thư mục mới trong `tools/py/` (cho tool Python) hoặc `tools/sh/` (cho tool shell script):

```
tools/py/ten-tool-moi/
```

### Bước 2: Tạo file chính

Tạo file chính có tên giống tên thư mục:

```
tools/py/ten-tool-moi/ten-tool-moi.py
```

### Bước 3: Tạo __init__.py

Tạo file `__init__.py`:

```python
"""
Tool: ten-tool-moi
"""
```

### Bước 4: (Optional) Tạo tool_info.json

Tạo file `tool_info.json` để cung cấp metadata cho tool:

```json
{
  "name": "Tên hiển thị tiếng Việt của tool",
  "tags": [
    "tag1",
    "tag2",
    "tag3"
  ]
}
```

**Lưu ý:**
- Nếu không có `tool_info.json`, hệ thống sẽ tự động generate tên hiển thị và tags từ tên file
- Tên file theo format `kebab-case` (ví dụ: `backup-folder.py`) sẽ được tự động chuyển đổi
- Tags sẽ được tự động tạo từ các từ trong tên file

### Bước 5: (Optional) Tạo doc.py

Tạo file `doc.py` để cung cấp hướng dẫn sử dụng:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File doc.py - Hướng dẫn sử dụng tool
"""

def get_help():
    """
    Trả về hướng dẫn sử dụng cơ bản của tool
    
    Returns:
        str: Hướng dẫn sử dụng tool
    """
    return """
📋 HƯỚNG DẪN SỬ DỤNG:

1️⃣  Bước 1: ...
2️⃣  Bước 2: ...

💡 TIP: ...
    """
```

### Bước 6: Hoàn thành!

**Tool sẽ tự động xuất hiện trong menu chính mà không cần sửa code nào khác!**

- Tool sẽ tự động được phát hiện
- Tên hiển thị sẽ tự động được tạo (hoặc lấy từ `tool_info.json`)
- Tags sẽ tự động được tạo (hoặc lấy từ `tool_info.json`)
- Hướng dẫn sử dụng sẽ tự động được đọc từ `doc.py`

## Ví dụ: Thêm tool mới

### Tool: `my-new-tool`

1. Tạo thư mục: `tools/py/my-new-tool/`
2. Tạo file: `tools/py/my-new-tool/my-new-tool.py`
3. Tạo file: `tools/py/my-new-tool/__init__.py`
4. (Optional) Tạo file: `tools/py/my-new-tool/tool_info.json`:
```json
{
  "name": "Tool mới của tôi - Mô tả ngắn",
  "tags": ["my", "new", "tool", "custom"]
}
```

**Kết quả:**
- Tool `my-new-tool.py` sẽ tự động xuất hiện trong menu
- Nếu không có `tool_info.json`, tên hiển thị sẽ là: "My New Tool"
- Tags sẽ tự động là: `["my", "new", "tool", "my-new-tool"]`

## File Config của Tool

Mỗi tool có thể có file config riêng trong thư mục của nó:

- **ssh-manager**: `ssh_config.json` - Danh sách SSH servers
- **image-watermark**: `watermark_templates.json` - Templates watermark đã lưu
- **backup-folder**: `backup_metadata.json` - Lịch sử backup (lưu trong thư mục backup)

**Lợi ích:**
- Config được tổ chức cùng tool sử dụng nó
- Dễ backup/restore từng tool với config riêng
- Không lộn xộn ở project root

## Lưu ý

- Tool phải có file `.py` chính có tên giống tên thư mục
- File chính phải có thể chạy độc lập bằng `python ten-tool.py`
- Nếu tool cần dependencies, thêm vào `requirements.txt` ở project root
- Tool nên có xử lý lỗi và thông báo rõ ràng cho người dùng
