# Find and Replace - Tim va thay the text

Mo ta ngan gon: Tim kiem trong nhieu file, ho tro Regex, case sensitive/insensitive, de quy thu muc con, che do preview, thong ke so dong.

## Cach su dung

```bash
python tools/find-and-replace.py
```

## Vi du 1: Chi tim kiem

```
Nhap duong dan thu muc: D:\my-react-project
Tim kiem trong tat ca thu muc con? (Y/n): Y
Chi xu ly file co duoi (vd: .txt .py .js - Enter de tat ca): .js .jsx
Nhap text can tim: useState
Phan biet chu hoa/thuong? (y/N): N
Su dung Regular Expression? (y/N): N
Che do: 1 (Chi tim kiem)
```

## Vi du 2: Thay the

```
Nhap text can tim: var 
Nhap text thay the: let 
Che do: 2 (Tim va thay the)
Xac nhan (YES): YES
```

## Use case pho bien
- Refactor code
- Cap nhat URL/domain
- Fix typo documentation
- Thay doi config path hang loat

# Find and Replace Tool

## Mô tả

Tool tìm kiếm và thay thế text trong nhiều file cùng lúc.

## Tính năng

✅ Tìm kiếm text trong nhiều file
✅ Thay thế text (simple hoặc regex)
✅ Hỗ trợ nhiều loại file: .txt, .py, .js, .html, .css, .json...
✅ Preview trước khi thay thế
✅ Backup tự động
✅ Case-sensitive hoặc case-insensitive
✅ Tìm kiếm đệ quy trong thư mục con

## Cách sử dụng

1. Chạy tool từ menu chính
2. Nhập đường dẫn thư mục hoặc file
3. Nhập text cần tìm
4. Nhập text thay thế
5. Chọn các tùy chọn:
   - Case-sensitive
   - Use regex
   - Recursive search
6. Preview kết quả
7. Xác nhận để thực hiện thay thế

## Ví dụ

### Thay thế đơn giản
```
Find: oldFunctionName
Replace: newFunctionName
Files: *.py
Result: Thay thế trong tất cả file Python
```

### Thay thế với Regex
```
Find: \d{3}-\d{3}-\d{4}
Replace: (xxx) xxx-xxxx
Files: *.txt
Result: Format lại số điện thoại
```

### Thay thế trong HTML
```
Find: <div class="old">
Replace: <div class="new">
Files: *.html
Result: Cập nhật CSS class
```

## Lưu ý

- Tool tự động backup file trước khi thay thế
- Backup lưu trong thư mục `.backup_[timestamp]`
- Hỗ trợ regex pattern cho tìm kiếm nâng cao
- Kiểm tra kỹ preview trước khi xác nhận

