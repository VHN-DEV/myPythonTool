# 🔌 SSH Manager Tool

## 📖 Giới Thiệu

Tool quản lý và kết nối nhanh đến các SSH server đã cấu hình sẵn.

## 🚀 Cách Sử Dụng

### **Phương thức 1: Chạy từ Menu chính (Khuyến nghị)**

```bash
python __main__.py
# Hoặc
python -m menu
```

Sau đó chọn số **13** để chạy SSH Manager.

### **Phương thức 2: Chạy trực tiếp**

```bash
python tool/ssh-manager.py
```

## ⚙️ Cấu Hình Server

Mở file `tool/ssh-manager.py` và tìm hàm `get_servers_config()`:

```python
def get_servers_config():
    servers = [
        {
            "name": "Tên server của bạn",
            "user": "username",
            "host": "192.168.1.100",   # IP hoặc domain
            "port": 22,                 # Port SSH
            "password": None,           # Để None
            "ssh_key": None             # Đường dẫn key (nếu có)
        }
    ]
    return servers
```

### **Ví dụ cấu hình:**

**1. Server với SSH Key:**
```python
{
    "name": "Production VPS",
    "user": "root",
    "host": "vps.mycompany.com",
    "port": 22,
    "password": None,
    "ssh_key": r"C:\Users\You\.ssh\id_rsa"
}
```

**2. Server nhập password thủ công:**
```python
{
    "name": "Dev Server",
    "user": "developer",
    "host": "192.168.1.50",
    "port": 2222,
    "password": None,  # Sẽ hỏi khi kết nối
    "ssh_key": None
}
```

**3. Server localhost:**
```python
{
    "name": "WSL Ubuntu",
    "user": "myuser",
    "host": "localhost",
    "port": 22,
    "password": None,
    "ssh_key": None
}
```

## 🎯 Tính Năng

- ✅ Kết nối nhanh bằng SSH key
- ✅ Kết nối với password
- ✅ Thêm server mới (tạm thời trong phiên)
- ✅ Hiển thị phương thức xác thực rõ ràng
- ✅ Hướng dẫn cấu hình chi tiết
- ✅ Tìm kiếm tool: `s ssh` trong menu

## 🔐 Bảo Mật

### ⚠️ **QUAN TRỌNG:**

1. **Không lưu password trong code**
2. **Sử dụng SSH key thay vì password**
3. **Bảo vệ SSH key:**
   ```bash
   # Linux/Mac
   chmod 600 ~/.ssh/id_rsa
   ```
4. **Thêm vào .gitignore nếu chứa thông tin nhạy cảm:**
   ```bash
   tool/ssh-manager.py
   ```

## 🛠️ Yêu Cầu

- **Windows:** OpenSSH Client (Windows 10/11 có sẵn) hoặc Git Bash
- **Linux/Mac:** SSH có sẵn

Kiểm tra:
```bash
ssh -V
```

## 💡 Menu Commands

Khi chạy tool, bạn có thể:

- Nhập **số** (1-n) - Kết nối đến server
- Nhập **a** - Thêm server mới (tạm thời)
- Nhập **h** - Xem hướng dẫn chi tiết
- Nhập **0** - Quay lại menu chính

## 🔍 Tìm Kiếm Tool

Trong menu chính, bạn có thể tìm SSH tool bằng:

```
s ssh          # Tìm theo keyword "ssh"
s server       # Tìm theo keyword "server"
s ket noi      # Tìm theo keyword "ket noi"
s remote       # Tìm theo keyword "remote"
```

## 📝 Lưu Ý

- Cấu hình server trong hàm `get_servers_config()` chỉ tồn tại trong code
- Server thêm bằng lệnh `a` chỉ tồn tại trong phiên chạy hiện tại
- Để lưu vĩnh viễn, cần thêm vào code

## 🚀 Use Cases

1. **DevOps:** Quản lý nhiều server (dev/staging/prod)
2. **Web Developer:** Kết nối VPS/hosting nhanh
3. **Sysadmin:** Quản lý danh sách server tập trung
4. **Team work:** Share config (không share password!)

---

**Happy SSHing! 🔌**

_myPythonTool v2.1 - SSH Manager Tool_

