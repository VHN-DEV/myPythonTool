# Thư mục Tools

## Cấu trúc

Mỗi tool nằm trong một thư mục riêng để dễ quản lý và mở rộng:

```
tools/
├── backup-folder/
│   ├── __init__.py
│   ├── backup-folder.py          # File chính của tool
│   └── README.md                 # (Optional) Hướng dẫn chi tiết
├── ssh-manager/
│   ├── __init__.py
│   ├── ssh-manager.py
│   └── README.md
├── ...
```

## Lợi ích của cấu trúc mới

✅ **Dễ quản lý**: Mỗi tool có thư mục riêng, tránh lộn xộn

✅ **Mở rộng dễ dàng**: Có thể thêm nhiều file phụ trợ cho mỗi tool:
   - README.md: Hướng dẫn chi tiết
   - config.json: Cấu hình riêng
   - helpers.py: Các hàm phụ trợ
   - tests.py: Unit tests

✅ **Tổ chức tốt hơn**: Dễ tìm kiếm và bảo trì

## Cách thêm tool mới

1. Tạo thư mục mới trong `tools/`:
   ```
   tools/ten-tool-moi/
   ```

2. Tạo file `__init__.py`:
   ```python
   """
   Tool: ten-tool-moi
   """
   ```

3. Tạo file chính có tên giống thư mục:
   ```
   tools/ten-tool-moi/ten-tool-moi.py
   ```

4. (Optional) Thêm README.md để hướng dẫn sử dụng

5. (Optional) Thêm file config riêng nếu cần:
   ```
   tools/ten-tool-moi/config.json
   tools/ten-tool-moi/settings.json
   ```

6. Tool sẽ tự động xuất hiện trong menu chính!

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

- Tên file chính phải giống tên thư mục (vd: `backup-folder/backup-folder.py`)
- Hệ thống tự động phát hiện và load tool từ cấu trúc này
- Vẫn tương thích với cấu trúc cũ (file .py nằm trực tiếp trong tools/)

