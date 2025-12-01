# Git Push Source Tool

Tool tự động hóa quá trình kết nối Git, commit và push source code lên repository.

## Tính năng

- ✅ Clone repository từ remote
- ✅ Khởi tạo Git repository mới
- ✅ Thiết lập remote repository
- ✅ Xem trạng thái Git
- ✅ Add files và commit
- ✅ Push code lên remote
- ✅ Tạo branch mới
- ✅ Thực hiện đầy đủ (add + commit + push) trong một lần

## Yêu cầu

- Git đã được cài đặt và có trong PATH
- Quyền truy cập repository (Personal Access Token hoặc SSH key)

## Sử dụng

### Interactive Mode

```bash
python git-push-source.py
```

### CLI Mode

```bash
# Clone repository
python git-push-source.py --clone --repo https://github.com/user/repo --path ./project

# Add, commit và push
python git-push-source.py --add . --commit "Update code" --push --branch main

# Xem trạng thái
python git-push-source.py --status
```

## Repository mặc định

Tool được cấu hình sẵn với repository:
- `https://github.com/VHN-DEV/laravel-botble-cms`

## Lưu ý

- Cần có quyền write vào repository
- Kiểm tra kỹ files trước khi commit
- Không commit files nhạy cảm (.env, keys, passwords)
- Không nên force push lên main/master branch

