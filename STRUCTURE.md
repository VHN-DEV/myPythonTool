# 📁 Cấu Trúc Thư Mục - myPythonTool v2.0

## 🗂️ Tổng Quan

```
myPythonTool/
├── 📁 menu/                    # ✨ NEW - Menu package
│   ├── __init__.py            # Menu chính (main menu)
│   ├── ssh.py                 # Menu SSH (remote tools)
│   └── README.md              # Documentation
│
├── 📁 utils/                   # ✨ NEW - Utils package
│   ├── __init__.py            # Package init
│   ├── common.py              # 15+ utility functions
│   ├── progress.py            # Progress bar system
│   └── logger.py              # Logging system
│
├── 📁 tool/                    # Tools directory
│   ├── compress-images.py     # 🔄 UPGRADED v2.0
│   ├── backup-folder.py       # 🔄 UPGRADED v2.0
│   ├── duplicate-finder.py    # 🔄 UPGRADED v2.0
│   └── ... (11 tools khác)
│
├── 📁 logs/                    # ✨ NEW - Auto-created logs
├── 📁 output/                  # ✨ NEW - Default output
│
├── __main__.py                 # ✨ NEW - Entry point (python .)
├── config.py                   # ✨ NEW - Centralized config
│
├── run.bat                     # ✨ NEW - Windows shortcut
├── run.sh                      # ✨ NEW - Linux/Mac shortcut
│
├── CHANGELOG.md                # 🔄 UPDATED - Version history
├── UPGRADE_SUMMARY.md          # ✨ NEW - Upgrade guide
├── STRUCTURE.md                # ✨ NEW - File này
├── README.md                   # Documentation
├── requirements.txt            # Dependencies
└── .gitignore                  # 🔄 UPDATED
```

---

## 🚀 Cách Chạy Tools

### 1️⃣ Entry Point Mới - `python .`
```bash
# Từ trong thư mục
cd myPythonTool
python .

# Từ bên ngoài
python myPythonTool
```

### 2️⃣ Module Import
```bash
# Menu chính
python -m menu

# Menu SSH
python -m menu.ssh
```

### 3️⃣ Import từ Package
```python
# Menu chính
from menu import main
main()

# Menu SSH
from menu.ssh import main
main()
```

### 4️⃣ Shortcuts
```bash
# Windows
run.bat        # Double-click

# Linux/Mac
./run.sh       # chmod +x run.sh
```

---

## 📦 Menu Package

### `menu/__init__.py` - Menu Chính
**Chức năng:**
- ⭐ Favorites system
- 📚 Recent tools
- 🔍 Search tools
- Config persistence
- Tool management

**Usage:**
```bash
python menu.py
# hoặc
python -m menu
```

### `menu/ssh.py` - Menu SSH
**Chức năng:**
- Chạy tools trên remote server
- SSH connection management

**Usage:**
```bash
python menu-ssh.py
# hoặc
python -m menu.ssh
```

---

## 🛠️ Utils Package

### `utils/common.py`
**Functions (15+):**
- `format_size()` - Format dung lượng
- `print_header()` - Header đẹp
- `get_user_input()` - Input validation
- `confirm_action()` - Confirmation
- `validate_path()` - Path validation
- `get_file_list()` - List files with filters
- `get_folder_size()` - Calculate folder size
- `safe_delete()` - Safe delete files/folders
- `parse_size_string()` - Parse size strings
- ... và nhiều hơn

### `utils/progress.py`
**Classes:**
- `ProgressBar` - Progress bar với ETA
- `Spinner` - Spinner animation

**Functions:**
- `simple_progress()` - Generator wrapper

### `utils/logger.py`
**Functions:**
- `setup_logger()` - Setup logging system
- `log_info()` - Log info messages
- `log_error()` - Log errors
- `log_warning()` - Log warnings

**Features:**
- Auto log rotation
- Log files trong `logs/`
- Configurable levels

---

## ⚙️ Config System

### `config.py`
**Features:**
- Centralized configuration
- 38+ constants
- Load/save JSON
- Auto-create directories

**Usage:**
```bash
# View config
python config.py

# Save config
python config.py save my_config.json

# Load config
python config.py load my_config.json
```

**Python:**
```python
from config import Config, get_config

quality = get_config('DEFAULT_IMAGE_QUALITY', 70)
Config.set('DEFAULT_IMAGE_QUALITY', 85)
```

---

## 🔧 Upgraded Tools

### compress-images.py v2.0
- ⚡ Multiprocessing
- 📊 Progress bar
- 🎯 CLI mode
- 📝 Logging

### backup-folder.py v2.0
- 📋 BackupManager class
- 💾 Metadata tracking
- 🔄 Restore feature
- ⚙️ CLI mode

### duplicate-finder.py v2.0
- ⚡ Multiprocessing
- 🎯 Smart algorithm
- 🗑️ Multiple delete modes
- 📝 Export report

---

## 📁 Runtime Files (Not Committed)

### Logs
```
logs/
├── compress-images_20251030.log
├── backup-folder_20251030.log
└── ...
```

### Config Files
```
tool_config.json          # Menu settings
backup_metadata.json      # Backup history
watermark_templates.json  # Watermark templates
```

### Output
```
output/                   # Default output directory
```

**Note:** Tất cả files này đã được add vào `.gitignore`

---

## 🎯 Clean Structure

### Running Tools
**Recommended ways:**
```bash
python .               # Từ trong thư mục (via __main__.py)
python myPythonTool    # Từ bên ngoài
python -m menu         # Module style
python -m menu.ssh     # SSH menu
run.bat               # Windows shortcut
./run.sh              # Linux/Mac shortcut
```

### Import
```python
from menu import main
main()

from menu.ssh import main as ssh_main
ssh_main()
```

---

## 📊 File Statistics

| Category | Files | Lines | Status |
|----------|-------|-------|--------|
| Menu | 2 | ~500 | ✅ Reorganized |
| Utils | 3 | ~1,100 | ✨ New |
| Config | 1 | ~400 | ✨ New |
| Tools (upgraded) | 3 | ~2,000 | 🔄 Upgraded |
| Tools (other) | 11 | ~2,500 | ✅ OK |
| Entry points | 3 | ~100 | ✨ New |
| **Total** | **23** | **~6,600** | ✅ |

---

## 🔮 Roadmap

### Phase 1 (Done ✅)
- [x] Utils package
- [x] Config system
- [x] Menu reorganization
- [x] 3 tools upgraded

### Phase 2 (Pending)
- [ ] Upgrade remaining tools
- [ ] Unit tests
- [ ] CI/CD

### Phase 3 (Future)
- [ ] GUI interface
- [ ] Web dashboard
- [ ] Plugin system

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| README.md | Overview và hướng dẫn |
| CHANGELOG.md | Lịch sử versions |
| UPGRADE_SUMMARY.md | Chi tiết upgrade v2.0 |
| STRUCTURE.md | Cấu trúc project (file này) |
| menu/README.md | Menu package docs |
| QUICK_REFERENCE.md | Quick reference |
| HUONG_DAN.txt | Hướng dẫn tiếng Việt |

---

## ✨ Key Improvements v2.0

### Organization
- ✅ Menu trong package riêng
- ✅ Utils package tái sử dụng
- ✅ Config centralized
- ✅ Clear structure

### Entry Points
- ✅ `python .` - Ngắn gọn
- ✅ `run.bat` - Windows friendly
- ✅ Backward compatible

### Code Quality
- ✅ DRY principle
- ✅ OOP design
- ✅ Type hints
- ✅ Full docstrings

### Performance
- ✅ 3-10x faster
- ✅ Multiprocessing
- ✅ Smart algorithms

---

_myPythonTool v2.0.0 - Structure Documentation_

