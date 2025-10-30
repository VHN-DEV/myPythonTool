# 👋 Chào mừng đến với myPythonTool!

## 🚀 Bạn mới clone về? Đọc theo thứ tự này:

### 1️⃣ Đọc tổng quan về dự án
📖 **[README.md](README.md)** - Giới thiệu dự án, danh sách công cụ, hướng dẫn sử dụng

### 2️⃣ Cài đặt để chạy từ bất kỳ đâu
⚡ **[INSTALL.md](INSTALL.md)** - Hướng dẫn cài đặt lệnh `myptool` toàn cục

### 3️⃣ Bắt đầu sử dụng
```bash
# Nếu đã cài đặt
myptool

# Hoặc chạy trực tiếp
python .
```

---

## 📁 Cấu trúc dự án

```
myPythonTool/
├── 📄 README.md              ← Tài liệu chính (ĐỌC ĐẦU TIÊN)
├── 📄 INSTALL.md             ← Hướng dẫn cài đặt
├── 📄 CHANGELOG.md           ← Lịch sử phiên bản
│
├── 📁 tool/                  ← Các công cụ chính
│   ├── backup-folder.py
│   ├── compress-images.py
│   ├── file-organizer.py
│   └── ... (15+ công cụ khác)
│
├── 📁 menu/                  ← Hệ thống menu
│   ├── __init__.py           ← Entry point
│   └── tool_manager.py       ← Quản lý tools
│
├── 📁 utils/                 ← Utilities hỗ trợ
│   ├── file_ops.py
│   ├── logger.py
│   └── validation.py
│
├── 📄 __main__.py            ← Chạy bằng: python .
├── 📄 requirements.txt       ← Dependencies
├── 📄 setup.py               ← Cài đặt package
└── 📄 pyproject.toml         ← Config modern
```

---

## ⚡ Quick Start

### Cách 1: Cài đặt toàn cục (Khuyến nghị)

```bash
cd D:\myPythonTool
pip install -e .

# Sau đó chạy từ bất kỳ đâu
myptool
```

### Cách 2: Chạy trực tiếp

```bash
cd D:\myPythonTool
python .
```

---

## 💡 Các file quan trọng

| File | Công dụng | Khi nào đọc? |
|------|-----------|--------------|
| **README.md** | Tài liệu chính, giới thiệu tất cả tools | Đọc đầu tiên |
| **INSTALL.md** | Hướng dẫn cài đặt lệnh toàn cục | Muốn chạy `myptool` từ bất kỳ đâu |
| **CHANGELOG.md** | Lịch sử phiên bản, tính năng mới | Xem có gì mới |
| **requirements.txt** | Danh sách thư viện cần cài | Khi cài dependencies |
| **tool_config.json** | Cấu hình tools | Khi muốn tùy chỉnh |

---

## 🎯 Bước tiếp theo

1. ✅ Đọc [README.md](README.md) để hiểu dự án
2. ✅ Xem [INSTALL.md](INSTALL.md) để cài đặt
3. ✅ Chạy `myptool` và khám phá!

---

**Chúc bạn sử dụng hiệu quả!** 🎉

