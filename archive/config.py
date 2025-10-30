#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Config - Cấu hình chung cho tất cả tools

Mục đích: Tập trung settings, dễ quản lý và customize
Lý do: Tránh hardcode, dễ thay đổi cấu hình
"""

import os
from pathlib import Path


class Config:
    """
    Class chứa config chung
    
    Mục đích: Centralize configuration
    """
    
    # ========== PATHS ==========
    # Thư mục gốc của project
    PROJECT_ROOT = Path(__file__).parent
    
    # Thư mục chứa tools
    TOOL_DIR = PROJECT_ROOT / "tool"
    
    # Thư mục chứa utils
    UTILS_DIR = PROJECT_ROOT / "utils"
    
    # Thư mục logs
    LOG_DIR = PROJECT_ROOT / "logs"
    
    # Thư mục output mặc định
    OUTPUT_DIR = PROJECT_ROOT / "output"
    
    # ========== LOGGING ==========
    # Level logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    LOG_LEVEL = "INFO"
    
    # Có ghi log ra file không
    LOG_TO_FILE = True
    
    # Có hiển thị log trên console không
    LOG_TO_CONSOLE = False
    
    # Số ngày giữ log files
    LOG_RETENTION_DAYS = 30
    
    # ========== COMPRESSION ==========
    # Định dạng nén mặc định cho backup
    DEFAULT_COMPRESSION_FORMAT = "zip"  # zip, tar, gztar, bztar, xztar
    
    # Chất lượng nén ảnh mặc định (1-100)
    DEFAULT_IMAGE_QUALITY = 70
    
    # Có optimize ảnh không
    DEFAULT_IMAGE_OPTIMIZE = True
    
    # ========== MULTIPROCESSING ==========
    # Số workers cho multiprocessing (None = auto)
    MAX_WORKERS = None
    
    # Số file tối thiểu để bật multiprocessing
    MIN_FILES_FOR_MULTIPROCESSING = 5
    
    # ========== FILE OPERATIONS ==========
    # Patterns loại trừ mặc định
    DEFAULT_EXCLUDE_PATTERNS = [
        'node_modules',
        '.git',
        '__pycache__',
        '.vscode',
        '.idea',
        'venv',
        'env',
        'dist',
        'build',
        '.pytest_cache',
        '.mypy_cache'
    ]
    
    # Extensions ảnh
    IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif', '.tiff']
    
    # Extensions video
    VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v']
    
    # Extensions audio
    AUDIO_EXTENSIONS = ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a']
    
    # Extensions document
    DOCUMENT_EXTENSIONS = [
        '.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt',
        '.xls', '.xlsx', '.ppt', '.pptx', '.csv'
    ]
    
    # Extensions archive
    ARCHIVE_EXTENSIONS = ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso']
    
    # Extensions code
    CODE_EXTENSIONS = [
        '.py', '.js', '.java', '.cpp', '.c', '.h', '.cs', '.php',
        '.html', '.css', '.scss', '.ts', '.jsx', '.tsx', '.go',
        '.rs', '.rb', '.sh', '.bat', '.ps1'
    ]
    
    # ========== HASH ==========
    # Thuật toán hash mặc định cho duplicate finder
    DEFAULT_HASH_ALGORITHM = 'md5'  # md5, sha1, sha256
    
    # Chunk size khi đọc file để hash (bytes)
    HASH_CHUNK_SIZE = 8192
    
    # ========== MENU ==========
    # Số recent tools tối đa
    MAX_RECENT_TOOLS = 10
    
    # Hiển thị description trong menu
    SHOW_TOOL_DESCRIPTIONS = True
    
    # ========== PROGRESS BAR ==========
    # Độ dài progress bar (ký tự)
    PROGRESS_BAR_LENGTH = 50
    
    # Ký tự fill progress bar
    PROGRESS_BAR_FILL = '█'
    
    # Hiển thị ETA (estimated time)
    SHOW_ETA = True
    
    # ========== BACKUP ==========
    # Số backup metadata giữ lại
    MAX_BACKUP_METADATA = 50
    
    # Tự động xóa backup cũ
    AUTO_DELETE_OLD_BACKUPS = False
    
    # Số ngày giữ backup
    BACKUP_RETENTION_DAYS = 90
    
    # ========== SAFETY ==========
    # Yêu cầu xác nhận cho thao tác nguy hiểm
    REQUIRE_CONFIRMATION = True
    
    # Yêu cầu nhập "YES" thay vì "y" cho thao tác rất nguy hiểm
    REQUIRE_YES_FOR_DESTRUCTIVE = True
    
    # Tạo backup trước khi thao tác nguy hiểm
    AUTO_BACKUP_BEFORE_DESTRUCTIVE = True
    
    # ========== PERFORMANCE ==========
    # Buffer size khi copy file (bytes)
    COPY_BUFFER_SIZE = 64 * 1024  # 64KB
    
    # Timeout cho các thao tác file (seconds, None = no timeout)
    FILE_OPERATION_TIMEOUT = None
    
    # ========== ENCODING ==========
    # Encoding mặc định cho text files
    DEFAULT_TEXT_ENCODING = 'utf-8'
    
    # Fallback encodings khi auto-detect
    FALLBACK_ENCODINGS = ['utf-8', 'utf-16', 'windows-1252', 'iso-8859-1']
    
    # ========== METHODS ==========
    
    @classmethod
    def get(cls, key: str, default=None):
        """
        Lấy config value theo key
        
        Args:
            key: Tên config
            default: Giá trị mặc định nếu không tìm thấy
        
        Returns:
            Config value
        """
        return getattr(cls, key, default)
    
    @classmethod
    def set(cls, key: str, value):
        """
        Set config value
        
        Args:
            key: Tên config
            value: Giá trị mới
        """
        setattr(cls, key, value)
    
    @classmethod
    def to_dict(cls) -> dict:
        """
        Convert config thành dictionary
        
        Returns:
            dict: Config dictionary
        
        Giải thích:
        - Chỉ lấy các attributes UPPERCASE (constants)
        - Bỏ qua methods và private attributes
        """
        config_dict = {}
        
        for key in dir(cls):
            if key.isupper() and not key.startswith('_'):
                value = getattr(cls, key)
                # Convert Path thành string để serializable
                if isinstance(value, Path):
                    value = str(value)
                config_dict[key] = value
        
        return config_dict
    
    @classmethod
    def load_from_file(cls, config_file: str):
        """
        Load config từ file JSON
        
        Args:
            config_file: Đường dẫn file config
        
        Giải thích:
        - Cho phép user customize config
        - Override default config
        """
        import json
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            for key, value in config_data.items():
                if key.isupper():
                    # Convert string path thành Path object nếu cần
                    if key.endswith('_DIR') or key.endswith('_PATH'):
                        value = Path(value)
                    cls.set(key, value)
            
            print(f"✅ Đã load config từ: {config_file}")
        
        except FileNotFoundError:
            print(f"⚠️  File config không tồn tại: {config_file}")
        except Exception as e:
            print(f"⚠️  Lỗi khi load config: {e}")
    
    @classmethod
    def save_to_file(cls, config_file: str):
        """
        Lưu config ra file JSON
        
        Args:
            config_file: Đường dẫn file config
        """
        import json
        
        try:
            config_dict = cls.to_dict()
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Đã lưu config: {config_file}")
        
        except Exception as e:
            print(f"❌ Lỗi khi lưu config: {e}")
    
    @classmethod
    def ensure_directories(cls):
        """
        Đảm bảo các thư mục cần thiết tồn tại
        
        Giải thích:
        - Tạo LOG_DIR, OUTPUT_DIR nếu chưa có
        - Gọi khi khởi động tools
        """
        directories = [cls.LOG_DIR, cls.OUTPUT_DIR]
        
        for directory in directories:
            if isinstance(directory, Path):
                directory.mkdir(parents=True, exist_ok=True)


# Tạo các thư mục cần thiết khi import config
try:
    Config.ensure_directories()
except Exception:
    pass


# ========== HELPER FUNCTIONS ==========

def get_config(key: str, default=None):
    """
    Hàm wrapper để lấy config
    
    Args:
        key: Config key
        default: Default value
    
    Returns:
        Config value
    
    Ví dụ:
        quality = get_config('DEFAULT_IMAGE_QUALITY', 70)
    """
    return Config.get(key, default)


def set_config(key: str, value):
    """
    Hàm wrapper để set config
    
    Args:
        key: Config key
        value: Config value
    
    Ví dụ:
        set_config('DEFAULT_IMAGE_QUALITY', 85)
    """
    Config.set(key, value)


if __name__ == "__main__":
    """
    Script để xem và quản lý config
    
    Cách dùng:
        python config.py                    # Hiển thị tất cả config
        python config.py save config.json   # Lưu config ra file
        python config.py load config.json   # Load config từ file
    """
    import sys
    
    if len(sys.argv) == 1:
        # Hiển thị tất cả config
        print("=" * 60)
        print("  CONFIGURATION")
        print("=" * 60)
        print()
        
        config_dict = Config.to_dict()
        
        # Group theo category
        categories = {}
        for key, value in config_dict.items():
            # Tìm prefix
            parts = key.split('_')
            if len(parts) > 1:
                category = parts[0]
            else:
                category = 'OTHER'
            
            if category not in categories:
                categories[category] = {}
            
            categories[category][key] = value
        
        # Hiển thị theo category
        for category, items in sorted(categories.items()):
            print(f"[{category}]")
            for key, value in sorted(items.items()):
                print(f"  {key} = {value}")
            print()
    
    elif len(sys.argv) == 3:
        action = sys.argv[1]
        file_path = sys.argv[2]
        
        if action == 'save':
            Config.save_to_file(file_path)
        
        elif action == 'load':
            Config.load_from_file(file_path)
        
        else:
            print(f"❌ Action không hợp lệ: {action}")
            print("Sử dụng: python config.py [save|load] <file>")
    
    else:
        print("Sử dụng:")
        print("  python config.py                    # Hiển thị config")
        print("  python config.py save config.json   # Lưu config")
        print("  python config.py load config.json   # Load config")

