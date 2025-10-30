# 📦 Hướng dẫn cài đặt myPythonTool

## 🎯 Mục tiêu: Chạy `myptool` từ bất kỳ đâu

---

## ⚡ Cài đặt nhanh (2 bước)

```bash
# Bước 1: Vào thư mục dự án
cd D:\myPythonTool

# Bước 2: Cài đặt
pip install -e .
```

**Xong!** Bây giờ bạn có thể chạy `myptool` từ bất kỳ đâu 🎉

```bash
# Test từ bất kỳ thư mục nào
cd C:\
myptool
```

---

## 📖 Giải thích chi tiết

### Lệnh `pip install -e .` làm gì?

1. **Cài myPythonTool như một Python package**
2. **Tạo lệnh toàn cục `myptool`**
3. **Thêm vào PATH tự động**
4. **Cho phép sửa code có hiệu lực ngay** (nhờ cờ `-e`)

### Sau khi cài đặt

```bash
# Từ bất kỳ thư mục nào
cd D:\Documents
cd C:\Projects
cd ~

# Chỉ cần gõ
myptool

# Menu sẽ xuất hiện! ✨
```

---

## 🔧 Phương pháp thay thế (Windows)

Nếu không muốn dùng pip, có thể dùng batch file:

### Bước 1: Sửa file `myptool.bat`

Mở file `myptool.bat`, tìm dòng:
```batch
set "TOOL_DIR=D:\myPythonTool"
```

Sửa đường dẫn cho đúng với máy bạn.

### Bước 2: Copy vào thư mục trong PATH

**Cách nhanh** (cần quyền Admin):
```bash
copy myptool.bat C:\Windows\System32\
```

**Cách an toàn:**
1. Tạo thư mục: `C:\Users\<TenBan>\bin\`
2. Copy `myptool.bat` vào đó
3. Thêm thư mục vào PATH:
   - Win+R → `sysdm.cpl` → Enter
   - Tab "Advanced" → "Environment Variables"
   - Chọn "Path" → "Edit" → "New"
   - Thêm: `C:\Users\<TenBan>\bin`
   - OK

### Bước 3: Thử nghiệm

```bash
# Mở CMD mới
myptool
```

---

## 🆘 Xử lý lỗi

### ❌ Lỗi: "myptool không được nhận dạng"

**Nguyên nhân:** Thư mục Scripts chưa trong PATH

**Giải pháp:**

```bash
# 1. Tìm thư mục Scripts
python -m site --user-base

# 2. Thêm Scripts vào PATH
# Kết quả (ví dụ): C:\Users\YourName\AppData\Roaming\Python\Python310
# → Thư mục Scripts: ...\Python\Python310\Scripts

# 3. Thêm vào PATH theo hướng dẫn trên
# 4. Mở CMD mới và thử lại
```

---

### ❌ Lỗi: "ModuleNotFoundError"

**Giải pháp:**

```bash
cd D:\myPythonTool
pip install -r requirements.txt
```

---

### ❌ Lỗi: "Permission denied"

**Giải pháp:**

```bash
# Cài cho user hiện tại
pip install --user -e .

# Hoặc chạy CMD với quyền Administrator
```

---

## 🗑️ Gỡ cài đặt

### Nếu cài bằng pip:

```bash
pip uninstall myPythonTool
```

### Nếu dùng batch file:

Xóa file `myptool.bat` đã copy:
```bash
del C:\Windows\System32\myptool.bat
```

---

## 💡 Lưu ý

- **Mở terminal/cmd mới** sau khi cài đặt để lệnh có hiệu lực
- **Cài ở chế độ editable** (`-e`) → sửa code không cần cài lại
- **Cập nhật code:** `git pull` → không cần cài lại

---

## 📚 Xem thêm

- **Tài liệu đầy đủ:** [README.md](../README.md)
- **Lịch sử thay đổi:** [CHANGELOG.md](CHANGELOG.md)

---

**Chúc bạn sử dụng hiệu quả!** 🎉
