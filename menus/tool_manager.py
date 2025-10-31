#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module tool_manager - Quản lý và chạy tools

Mục đích: Tách logic quản lý tools ra khỏi menu chính
Lý do: Dễ maintain, test và mở rộng
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Optional
from utils.colors import Colors
from utils.format import print_header, print_separator
from utils.categories import group_tools_by_category, get_category_info
from utils.helpers import highlight_keyword


class ToolManager:
    """
    Class quản lý tools
    
    Mục đích: Tập trung logic quản lý tools, favorites, history
    """
    
    def __init__(self, tool_dir: str):
        """
        Khởi tạo ToolManager
        
        Args:
            tool_dir: Thư mục chứa tools
        """
        self.tool_dir = Path(tool_dir)
        # Config file nằm trong thư mục menu
        self.config_file = Path(__file__).parent / "tool_config.json"
        self.config = self._load_config()
        
        # Cache metadata của tools (tự động load khi cần)
        self.tool_names = {}
        self.tool_tags = {}
        
        # Tools ưu tiên hiển thị lên đầu danh sách
        # Mục đích: Các tools hay dùng nhất hoặc quan trọng nhất sẽ hiển thị trước
        # Lý do: Dễ dàng truy cập nhanh các tools thường xuyên sử dụng
        self.priority_tools = [
            "ssh-manager.py",  # Tool SSH Manager - hay dùng nhất
            # Có thể thêm các tools khác vào đây để ưu tiên
        ]
    
    def _load_config(self) -> Dict:
        """
        Load config từ file
        
        Returns:
            dict: Config data
        
        Giải thích:
        - Lưu favorites, recent tools, settings, disabled_tools
        - Tạo config mặc định nếu chưa có
        - Đảm bảo các field mới được thêm vào config cũ (migration)
        """
        default_config = {
            'favorites': [],
            'recent': [],
            'disabled_tools': [],  # Danh sách tools bị vô hiệu hóa
            'settings': {
                'show_descriptions': True,
                'max_recent': 10
            }
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Đảm bảo các field mới có trong config cũ (migration)
                    if 'disabled_tools' not in loaded_config:
                        loaded_config['disabled_tools'] = []
                    # Đảm bảo settings có đầy đủ các field
                    if 'settings' not in loaded_config:
                        loaded_config['settings'] = default_config['settings']
                    else:
                        # Thêm các field settings mới nếu thiếu
                        for key, value in default_config['settings'].items():
                            if key not in loaded_config['settings']:
                                loaded_config['settings'][key] = value
                    return loaded_config
            except Exception:
                pass
        
        # Config mặc định
        return default_config
    
    def _save_config(self):
        """Lưu config ra file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  Lỗi lưu config: {e}")
    
    def _get_tool_metadata_file(self, tool: str) -> Path:
        """
        Tìm file tool_info.json cho tool
        
        Args:
            tool: Tên file tool (vd: backup-folder.py)
        
        Returns:
            Path: Đường dẫn đến tool_info.json hoặc None
        """
        tool_name = tool.replace('.py', '')
        
        # Thử tìm trong tools/py/
        py_tool_dir = self.tool_dir / "py" / tool_name
        py_metadata = py_tool_dir / "tool_info.json"
        if py_metadata.exists():
            return py_metadata
        
        # Thử tìm trong tools/sh/
        sh_tool_dir = self.tool_dir / "sh" / tool_name
        sh_metadata = sh_tool_dir / "tool_info.json"
        if sh_metadata.exists():
            return sh_metadata
        
        # Thử cấu trúc cũ
        old_tool_dir = self.tool_dir / tool_name
        old_metadata = old_tool_dir / "tool_info.json"
        if old_metadata.exists():
            return old_metadata
        
        return None
    
    def _load_tool_metadata(self, tool: str) -> Dict:
        """
        Load metadata cho tool từ tool_info.json hoặc tự động generate
        
        Args:
            tool: Tên file tool (vd: backup-folder.py)
        
        Returns:
            dict: Metadata gồm 'name' và 'tags'
        """
        # Kiểm tra cache trước
        if tool in self.tool_names:
            return {
                'name': self.tool_names[tool],
                'tags': self.tool_tags.get(tool, [])
            }
        
        # Thử đọc từ tool_info.json
        metadata_file = self._get_tool_metadata_file(tool)
        if metadata_file and metadata_file.exists():
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    
                    # Lưu vào cache
                    self.tool_names[tool] = metadata.get('name', self._generate_display_name(tool))
                    self.tool_tags[tool] = metadata.get('tags', [])
                    
                    return {
                        'name': self.tool_names[tool],
                        'tags': self.tool_tags[tool]
                    }
            except Exception:
                pass  # Nếu đọc lỗi, fallback sang generate tự động
        
        # Tự động generate metadata từ tên file
        display_name = self._generate_display_name(tool)
        tags = self._generate_tags(tool)
        
        # Lưu vào cache
        self.tool_names[tool] = display_name
        self.tool_tags[tool] = tags
        
        return {
            'name': display_name,
            'tags': tags
        }
    
    def _generate_display_name(self, tool: str) -> str:
        """
        Tự động generate tên hiển thị từ tên file tool
        
        Args:
            tool: Tên file tool (vd: backup-folder.py)
        
        Returns:
            str: Tên hiển thị tiếng Việt
        """
        tool_name = tool.replace('.py', '')
        
        # Dictionary ánh xạ từ khóa -> tiếng Việt
        keyword_map = {
            'backup': 'Sao lưu',
            'folder': 'thư mục',
            'clean': 'Dọn dẹp',
            'temp': 'file tạm',
            'compress': 'Nén',
            'image': 'ảnh',
            'copy': 'Sao chép',
            'changed': 'thay đổi',
            'duplicate': 'trùng lặp',
            'finder': 'Tìm',
            'extract': 'Giải nén',
            'archive': 'file nén',
            'file': 'file',
            'organizer': 'Sắp xếp',
            'find': 'Tìm',
            'replace': 'thay thế',
            'generate': 'Tạo',
            'tree': 'cây thư mục',
            'watermark': 'watermark',
            'pdf': 'PDF',
            'rename': 'Đổi tên',
            'setup': 'Cài đặt',
            'project': 'dự án',
            'linux': 'Linux',
            'text': 'text',
            'encoding': 'encoding',
            'converter': 'chuyển đổi',
            'video': 'video',
            'ssh': 'SSH',
            'manager': 'Quản lý',
            'server': 'Server'
        }
        
        # Convert kebab-case sang từng từ và translate
        words = tool_name.split('-')
        translated_words = []
        
        for word in words:
            if word in keyword_map:
                translated_words.append(keyword_map[word])
            else:
                # Nếu không tìm thấy, giữ nguyên nhưng capitalize
                translated_words.append(word.capitalize())
        
        # Ghép lại thành tên hiển thị
        display_name = ' '.join(translated_words)
        
        # Thêm mô tả ngắn nếu cần (tùy chọn)
        return display_name
    
    def _generate_tags(self, tool: str) -> List[str]:
        """
        Tự động generate tags từ tên file tool
        
        Args:
            tool: Tên file tool (vd: backup-folder.py)
        
        Returns:
            list: Danh sách tags
        """
        tool_name = tool.replace('.py', '').lower()
        
        # Extract tags từ tên file (các từ trong kebab-case)
        tags = tool_name.split('-')
        
        # Thêm tên file đầy đủ làm tag
        tags.append(tool_name)
        
        # Thêm tags phổ biến dựa trên keywords
        if 'image' in tool_name or 'photo' in tool_name:
            tags.extend(['anh', 'hinh', 'picture'])
        elif 'video' in tool_name:
            tags.extend(['video', 'phim'])
        elif 'pdf' in tool_name:
            tags.extend(['pdf', 'document'])
        elif 'backup' in tool_name:
            tags.extend(['backup', 'sao luu'])
        elif 'compress' in tool_name or 'zip' in tool_name:
            tags.extend(['compress', 'nen'])
        elif 'ssh' in tool_name:
            tags.extend(['ssh', 'remote', 'server'])
        
        return list(set(tags))  # Remove duplicates
    
    def get_tool_display_name(self, tool: str) -> str:
        """
        Lấy tên hiển thị của tool (tự động load metadata nếu chưa có)
        
        Args:
            tool: Tên file tool (vd: backup-folder.py)
        
        Returns:
            str: Tên hiển thị tiếng Việt
        """
        if tool not in self.tool_names:
            self._load_tool_metadata(tool)
        return self.tool_names.get(tool, tool)
    
    def get_tool_tags(self, tool: str) -> List[str]:
        """
        Lấy tags của tool (tự động load metadata nếu chưa có)
        
        Args:
            tool: Tên file tool (vd: backup-folder.py)
        
        Returns:
            list: Danh sách tags
        """
        if tool not in self.tool_tags:
            self._load_tool_metadata(tool)
        return self.tool_tags.get(tool, [])
    
    def get_tool_list(self) -> List[str]:
        """
        Lấy danh sách file .py trong thư mục tool
        
        Returns:
            list: Danh sách tên file tool (priority tools trước, sau đó alphabet)
        
        Giải thích:
        - Bước 1: Tìm tools trong tools/py/ (các tool Python)
        - Bước 2: Tìm tools trong tools/sh/ (các tool shell/đặc biệt)
        - Bước 3: Tách ra priority tools và tools thường
        - Bước 4: Sắp xếp priority tools theo thứ tự định sẵn
        - Bước 5: Sắp xếp tools thường theo alphabet
        - Bước 6: Ghép lại: priority + alphabet
        
        Lý do tìm trong thư mục con:
        - Hỗ trợ cấu trúc mới: mỗi tool có thư mục riêng
        - Ví dụ: tools/py/backup-folder/backup-folder.py
        - Ví dụ: tools/sh/setup-project-linux/setup-project-linux.py
        """
        if not self.tool_dir.exists():
            return []
        
        all_tools = []
        
        # Tìm tools trong tools/py/ (các tool Python thông thường)
        py_dir = self.tool_dir / "py"
        if py_dir.exists() and py_dir.is_dir():
            for item in os.listdir(py_dir):
                item_path = py_dir / item
                if item_path.is_dir():
                    # Tìm file có tên giống thư mục
                    main_file = item_path / f"{item}.py"
                    if main_file.exists():
                        all_tools.append(f"{item}.py")
        
        # Tìm tools trong tools/sh/ (các tool đặc biệt như shell scripts)
        sh_dir = self.tool_dir / "sh"
        if sh_dir.exists() and sh_dir.is_dir():
            for item in os.listdir(sh_dir):
                item_path = sh_dir / item
                if item_path.is_dir():
                    # Tìm file .py trong thư mục con
                    main_file = item_path / f"{item}.py"
                    if main_file.exists():
                        all_tools.append(f"{item}.py")
        
        # Tương thích với cấu trúc cũ: tìm trực tiếp trong tools/ (nếu còn)
        for item in os.listdir(self.tool_dir):
            item_path = self.tool_dir / item
            # Bỏ qua thư mục py và sh (đã xử lý ở trên)
            if item in ['py', 'sh']:
                continue
            # Nếu là thư mục, tìm file .py chính trong đó
            if item_path.is_dir():
                main_file = item_path / f"{item}.py"
                if main_file.exists():
                    all_tools.append(f"{item}.py")
            # Nếu là file .py (để tương thích với cấu trúc cũ)
            elif item.endswith('.py'):
                all_tools.append(item)
        
        # Tách priority tools và tools thường
        priority = []
        regular = []
        
        for tool in all_tools:
            if tool in self.priority_tools:
                priority.append(tool)
            else:
                regular.append(tool)
        
        # Sắp xếp priority tools theo thứ tự định sẵn
        priority.sort(key=lambda x: self.priority_tools.index(x))
        
        # Sắp xếp tools thường theo alphabet
        regular.sort()
        
        # Ghép lại: priority + regular
        all_tools_unsorted = priority + regular
        
        # Filter ra các tool bị disabled
        disabled_tools = set(self.config.get('disabled_tools', []))
        active_tools = [t for t in all_tools_unsorted if t not in disabled_tools]
        
        return active_tools
    
    def get_all_tools_including_disabled(self) -> List[str]:
        """
        Lấy danh sách tất cả tools (bao gồm cả disabled)
        
        Returns:
            list: Danh sách tất cả tools
        """
        if not self.tool_dir.exists():
            return []
        
        all_tools = []
        
        # Tìm tools trong tools/py/ (các tool Python thông thường)
        py_dir = self.tool_dir / "py"
        if py_dir.exists() and py_dir.is_dir():
            for item in os.listdir(py_dir):
                item_path = py_dir / item
                if item_path.is_dir():
                    # Tìm file có tên giống thư mục
                    main_file = item_path / f"{item}.py"
                    if main_file.exists():
                        all_tools.append(f"{item}.py")
        
        # Tìm tools trong tools/sh/ (các tool đặc biệt như shell scripts)
        sh_dir = self.tool_dir / "sh"
        if sh_dir.exists() and sh_dir.is_dir():
            for item in os.listdir(sh_dir):
                item_path = sh_dir / item
                if item_path.is_dir():
                    # Tìm file .py trong thư mục con
                    main_file = item_path / f"{item}.py"
                    if main_file.exists():
                        all_tools.append(f"{item}.py")
        
        # Tương thích với cấu trúc cũ: tìm trực tiếp trong tools/ (nếu còn)
        for item in os.listdir(self.tool_dir):
            item_path = self.tool_dir / item
            # Bỏ qua thư mục py và sh (đã xử lý ở trên)
            if item in ['py', 'sh']:
                continue
            # Nếu là thư mục, tìm file .py chính trong đó
            if item_path.is_dir():
                main_file = item_path / f"{item}.py"
                if main_file.exists():
                    all_tools.append(f"{item}.py")
            # Nếu là file .py (để tương thích với cấu trúc cũ)
            elif item.endswith('.py'):
                all_tools.append(item)
        
        # Tách priority tools và tools thường
        priority = []
        regular = []
        
        for tool in all_tools:
            if tool in self.priority_tools:
                priority.append(tool)
            else:
                regular.append(tool)
        
        # Sắp xếp priority tools theo thứ tự định sẵn
        priority.sort(key=lambda x: self.priority_tools.index(x))
        
        # Sắp xếp tools thường theo alphabet
        regular.sort()
        
        # Ghép lại: priority + regular (bao gồm cả disabled)
        return priority + regular
    
    def search_tools(self, query: str) -> List[str]:
        """
        Tìm kiếm tool theo keyword
        
        Args:
            query: Từ khóa tìm kiếm
        
        Returns:
            list: Danh sách tool phù hợp
        
        Giải thích:
        - Tìm trong tên file
        - Tìm trong description
        - Tìm trong tags
        """
        query = query.lower()
        results = []
        
        for tool in self.get_tool_list():
            # Tìm trong tên file
            if query in tool.lower():
                results.append(tool)
                continue
            
            # Tìm trong description
            description = self.get_tool_display_name(tool)
            if query in description.lower():
                results.append(tool)
                continue
            
            # Tìm trong tags
            tags = self.get_tool_tags(tool)
            if any(query in tag.lower() for tag in tags):
                results.append(tool)
        
        return results
    
    def add_to_favorites(self, tool: str):
        """Thêm tool vào favorites"""
        if tool not in self.config['favorites']:
            self.config['favorites'].append(tool)
            self._save_config()
            tool_name = self.get_tool_display_name(tool)
            print(Colors.success(f"⭐ Đã thêm vào favorites: {Colors.bold(tool_name)}"))
        else:
            tool_name = self.get_tool_display_name(tool)
            print(Colors.warning(f"ℹ️  Tool đã có trong favorites: {tool_name}"))
    
    def remove_from_favorites(self, tool: str):
        """Xóa tool khỏi favorites"""
        if tool in self.config['favorites']:
            self.config['favorites'].remove(tool)
            self._save_config()
            tool_name = self.get_tool_display_name(tool)
            print(Colors.info(f"❌ Đã xóa khỏi favorites: {tool_name}"))
        else:
            tool_name = self.get_tool_display_name(tool)
            print(Colors.warning(f"ℹ️  Tool không có trong favorites: {tool_name}"))
    
    def activate_tool(self, tool: str):
        """Kích hoạt tool (xóa khỏi danh sách disabled)"""
        if tool in self.config['disabled_tools']:
            self.config['disabled_tools'].remove(tool)
            self._save_config()
            tool_name = self.get_tool_display_name(tool)
            print(Colors.success(f"✅ Đã kích hoạt tool: {Colors.bold(tool_name)}"))
        else:
            tool_name = self.get_tool_display_name(tool)
            print(Colors.warning(f"ℹ️  Tool đã được kích hoạt: {tool_name}"))
    
    def deactivate_tool(self, tool: str):
        """Vô hiệu hóa tool (thêm vào danh sách disabled)"""
        if tool not in self.config['disabled_tools']:
            self.config['disabled_tools'].append(tool)
            self._save_config()
            tool_name = self.get_tool_display_name(tool)
            print(Colors.warning(f"⚠️  Đã vô hiệu hóa tool: {Colors.bold(tool_name)}"))
        else:
            tool_name = self.get_tool_display_name(tool)
            print(Colors.warning(f"ℹ️  Tool đã bị vô hiệu hóa: {tool_name}"))
    
    def is_tool_active(self, tool: str) -> bool:
        """Kiểm tra tool có đang active không"""
        return tool not in self.config.get('disabled_tools', [])
    
    def add_to_recent(self, tool: str):
        """
        Thêm tool vào recent
        
        Args:
            tool: Tên file tool
        
        Giải thích:
        - Xóa tool nếu đã có trong list (để move lên đầu)
        - Thêm vào đầu list
        - Giới hạn số lượng recent
        """
        if tool in self.config['recent']:
            self.config['recent'].remove(tool)
        
        self.config['recent'].insert(0, tool)
        
        # Giới hạn số recent
        max_recent = self.config['settings'].get('max_recent', 10)
        self.config['recent'] = self.config['recent'][:max_recent]
        
        self._save_config()
    
    def run_tool(self, tool: str) -> int:
        """
        Chạy tool
        
        Args:
            tool: Tên file tool
        
        Returns:
            int: Exit code
        
        Giải thích:
        - Tìm và chạy tool từ thư mục tool/ hoặc thư mục con
        - Lưu vào recent
        - Hiển thị thông báo
        
        Lý do xử lý cả 2 cấu trúc:
        - Cấu trúc cũ: tool/backup-folder.py
        - Cấu trúc mới: tool/backup-folder/backup-folder.py
        
        Đặc biệt: setup-project-linux.py chạy trực tiếp bash app.sh
        """
        # Tool đặc biệt: setup-project-linux - chạy trực tiếp bash app.sh
        if tool == "setup-project-linux.py":
            return self._run_setup_project_linux()
        
        # Tìm đường dẫn thực tế của tool
        tool_path = self._find_tool_path(tool)
        
        if not tool_path or not tool_path.exists():
            print(Colors.error(f"❌ Tool không tồn tại: {tool}"))
            return 1
        
        tool_display_name = self.get_tool_display_name(tool)
        print()
        print_separator("═", 70, Colors.PRIMARY)
        print(Colors.primary(f"  ▶ Đang chạy: {Colors.bold(tool_display_name)}"))
        print_separator("═", 70, Colors.PRIMARY)
        print()
        
        try:
            result = subprocess.run(["python", str(tool_path)])
            
            print()
            print_separator("═", 70, Colors.SUCCESS)
            print(Colors.success(f"  ✅ Tool đã chạy xong!"))
            print_separator("═", 70, Colors.SUCCESS)
            print()
            
            # Lưu vào recent
            self.add_to_recent(tool)
            
            return result.returncode
            
        except KeyboardInterrupt:
            print()
            print(Colors.warning("⚠️  Tool bị ngắt bởi người dùng"))
            return 130
            
        except Exception as e:
            print()
            print(Colors.error(f"❌ Lỗi khi chạy tool: {e}"))
            return 1
    
    def _run_setup_project_linux(self) -> int:
        """
        Chạy setup-project-linux trực tiếp bằng bash app.sh
        Tránh lỗi với editable install khi chạy qua Python
        """
        import shutil
        
        # Tìm đường dẫn app.sh
        script_dir = self.tool_dir / "sh" / "setup-project-linux"
        app_sh = script_dir / "app.sh"
        
        if not app_sh.exists():
            print(f"❌ Không tìm thấy file app.sh!")
            print(f"   Đường dẫn: {app_sh}")
            return 1
        
        print(f"\n{'='*60}")
        print(f">>> Đang chạy: {self.get_tool_display_name('setup-project-linux.py')}")
        print(f"{'='*60}\n")
        
        try:
            # Tìm bash
            bash_cmd = None
            
            # Trên Windows, tìm Git Bash
            if sys.platform == 'win32':
                git_bash_paths = [
                    r"C:\Program Files\Git\bin\bash.exe",
                    r"C:\Program Files (x86)\Git\bin\bash.exe",
                    os.path.expanduser(r"~\AppData\Local\Programs\Git\bin\bash.exe")
                ]
                
                for bash_path in git_bash_paths:
                    if os.path.exists(bash_path):
                        bash_cmd = [bash_path]
                        break
                
                # Thử WSL nếu không có Git Bash
                if not bash_cmd:
                    wsl_path = shutil.which('wsl')
                    if wsl_path:
                        bash_cmd = ['wsl', 'bash']
                
                # Thử bash.exe trong PATH
                if not bash_cmd:
                    bash_exe = shutil.which('bash.exe')
                    if bash_exe:
                        bash_cmd = [bash_exe]
            else:
                # Linux/macOS
                bash_path = shutil.which('bash')
                if bash_path:
                    bash_cmd = [bash_path]
            
            if not bash_cmd:
                print("❌ Không tìm thấy bash!")
                print("   Trên Windows, cần cài Git Bash hoặc WSL")
                return 1
            
            # Chuyển đổi đường dẫn cho Git Bash trên Windows
            if sys.platform == 'win32' and 'Git' in str(bash_cmd[0]):
                # Chuyển D:\path\to\app.sh thành /d/path/to/app.sh
                script_path_str = str(app_sh.resolve())
                if ':' in script_path_str:
                    drive = script_path_str[0].lower()
                    unix_path = script_path_str.replace('\\', '/').replace(f'{drive}:', f'/{drive}', 1)
                else:
                    unix_path = script_path_str.replace('\\', '/')
                cmd = bash_cmd + [unix_path]
            else:
                cmd = bash_cmd + [str(app_sh)]
            
            # Chạy bash app.sh
            result = subprocess.run(cmd, check=False)
            
            print()
            print_separator("═", 70, Colors.SUCCESS)
            print(Colors.success(f"  ✅ Tool đã chạy xong!"))
            print_separator("═", 70, Colors.SUCCESS)
            print()
            
            # Lưu vào recent
            self.add_to_recent("setup-project-linux.py")
            
            return result.returncode
            
        except KeyboardInterrupt:
            print()
            print(Colors.warning("⚠️  Tool bị ngắt bởi người dùng"))
            return 130
            
        except Exception as e:
            print()
            print(Colors.error(f"❌ Lỗi khi chạy tool: {e}"))
            return 1
    
    def _find_tool_path(self, tool: str) -> Optional[Path]:
        """
        Tìm đường dẫn thực tế của tool
        
        Args:
            tool: Tên file tool (vd: backup-folder.py)
        
        Returns:
            Path: Đường dẫn đầy đủ đến file tool, hoặc None nếu không tìm thấy
        
        Giải thích:
        - Bước 1: Thử tìm trong tools/py/ (các tool Python)
        - Bước 2: Thử tìm trong tools/sh/ (các tool đặc biệt)
        - Bước 3: Thử tìm trực tiếp trong tools/ (cấu trúc cũ)
        
        Lý do:
        - Hỗ trợ cấu trúc mới: tools/py/ và tools/sh/
        - Ưu tiên cấu trúc mới (tools/py/ và tools/sh/)
        - Vẫn tương thích với cấu trúc cũ
        """
        tool_name = tool.replace('.py', '')
        
        # Thử tìm trong tools/py/ (cấu trúc mới)
        py_tool_path = self.tool_dir / "py" / tool_name / tool
        if py_tool_path.exists():
            return py_tool_path
        
        # Thử tìm trong tools/sh/ (các tool đặc biệt)
        sh_tool_path = self.tool_dir / "sh" / tool_name / tool
        if sh_tool_path.exists():
            return sh_tool_path
        
        # Thử cấu trúc cũ: tool/backup-folder/backup-folder.py
        old_structure_path = self.tool_dir / tool_name / tool
        if old_structure_path.exists():
            return old_structure_path
        
        # Thử cấu trúc cũ: tool/backup-folder.py
        old_file_path = self.tool_dir / tool
        if old_file_path.exists():
            return old_file_path
        
        return None
    
    def display_menu(self, tools: Optional[List[str]] = None, title: str = "DANH SÁCH TOOL", group_by_category: bool = True, search_query: Optional[str] = None):
        """
        Hiển thị menu tools với UI/UX đẹp hơn
        
        Args:
            tools: Danh sách tools (None = hiển thị tất cả)
            title: Tiêu đề menu
            group_by_category: Có nhóm theo categories không
        
        Giải thích:
        - Hiển thị danh sách đẹp với số thứ tự
        - Highlight favorites với màu sắc
        - Nhóm tools theo categories nếu có
        - Sử dụng màu sắc và icons đẹp hơn
        - Hiển thị stats nhanh
        """
        if tools is None:
            tools = self.get_tool_list()
        
        if not tools:
            print(Colors.error("❌ Không tìm thấy tool nào!"))
            return
        
        # Header
        print()
        print_separator("═", 70, Colors.PRIMARY)
        title_colored = Colors.primary(f"  {title}")
        print(title_colored)
        print_separator("═", 70, Colors.PRIMARY)
        print()
        
        # Stats nhanh
        total = len(tools)
        all_tools_count = len(self.get_all_tools_including_disabled())
        disabled_count = all_tools_count - total
        favorites_count = len([t for t in tools if t in self.config['favorites']])
        recent_count = len([t for t in self.config['recent'] if t in tools])
        
        stats_line = f"{Colors.muted('📊')} {Colors.info(f'Active: {total}')}"
        if disabled_count > 0:
            stats_line += f" | {Colors.error(f'Disabled: {disabled_count}')}"
        stats_line += f" | {Colors.warning(f'⭐ Favorites: {favorites_count}')} | {Colors.secondary(f'📚 Recent: {recent_count}')}"
        print(f"  {stats_line}")
        print()
        
        # Nhóm theo categories hoặc hiển thị flat list
        if group_by_category and len(tools) > 5:
            grouped = group_tools_by_category(tools, self)
            current_idx = 1
            
            for category, category_tools in grouped.items():
                cat_info = get_category_info(category)
                icon = cat_info['icon']
                cat_name = cat_info['name']
                
                # Category header
                print()
                category_header = f"{icon} {Colors.bold(cat_name)} {Colors.muted(f'({len(category_tools)})')}"
                print(f"  {category_header}")
                print_separator("─", 68, Colors.MUTED)
                
                # Tools trong category
                for tool in category_tools:
                    is_favorite = tool in self.config['favorites']
                    tool_name = self.get_tool_display_name(tool)
                    idx_str = f"{current_idx:2d}."
                    
                    if is_favorite:
                        star = Colors.warning("⭐")
                        idx_colored = Colors.info(idx_str)
                    else:
                        star = "  "
                        idx_colored = Colors.muted(idx_str)
                    
                    # Highlight search query nếu có
                    if search_query:
                        tool_name_colored = highlight_keyword(tool_name, search_query)
                    else:
                        tool_name_colored = Colors.bold(tool_name) if is_favorite else tool_name
                    
                    print(f"  {star} {idx_colored} {tool_name_colored}")
                    current_idx += 1
        else:
            # Hiển thị flat list (không nhóm)
            for idx, tool in enumerate(tools, start=1):
                is_favorite = tool in self.config['favorites']
                tool_name = self.get_tool_display_name(tool)
                idx_str = f"{idx:2d}."
                
                if is_favorite:
                    star = Colors.warning("⭐")
                    idx_colored = Colors.info(idx_str)
                else:
                    star = "  "
                    idx_colored = Colors.muted(idx_str)
                
                # Highlight search query nếu có
                if search_query:
                    tool_name_colored = highlight_keyword(tool_name, search_query)
                else:
                    tool_name_colored = Colors.bold(tool_name) if is_favorite else tool_name
                
                print(f"{star} {idx_colored} {tool_name_colored}")
        
        # Footer
        print()
        print_separator("═", 70, Colors.PRIMARY)
        print()
    
    def show_help(self):
        """Hiển thị help với UI/UX đẹp hơn"""
        print()
        print_separator("═", 70, Colors.PRIMARY)
        title = Colors.primary("  HƯỚNG DẪN SỬ DỤNG")
        print(title)
        print_separator("═", 70, Colors.PRIMARY)
        print()
        
        # Lệnh cơ bản
        print(Colors.bold("📋 LỆNH CƠ BẢN:"))
        print(f"   {Colors.info('[số]')}         - Chạy tool theo số thứ tự")
        print(f"   {Colors.info('[số]h')}        - Xem hướng dẫn của tool (ví dụ: 1h, 4h)")
        print(f"   {Colors.info('h, help')}      - Hiển thị hướng dẫn này")
        print(f"   {Colors.info('q, quit, 0')}   - Thoát chương trình")
        print()
        
        # Tìm kiếm
        print(Colors.bold("🔍 TÌM KIẾM:"))
        print(f"   {Colors.info('s [keyword]')}  - Tìm kiếm tool")
        print(f"   {Colors.info('/[keyword]')}   - Tìm kiếm tool (cách khác)")
        print()
        print(f"   {Colors.muted('Ví dụ:')} {Colors.secondary('s backup')}, {Colors.secondary('/image')}")
        print()
        
        # Favorites
        print(Colors.bold("⭐ FAVORITES:"))
        print(f"   {Colors.info('f')}            - Hiển thị danh sách favorites")
        print(f"   {Colors.info('f+ [số]')}      - Thêm tool vào favorites")
        print(f"   {Colors.info('f- [số]')}      - Xóa tool khỏi favorites")
        print()
        print(f"   {Colors.muted('Ví dụ:')} {Colors.secondary('f+ 3')}, {Colors.secondary('f- 1')}")
        print()
        
        # Recent
        print(Colors.bold("📚 RECENT:"))
        print(f"   {Colors.info('r')}            - Hiển thị recent tools")
        print(f"   {Colors.info('r[số]')}        - Chạy recent tool")
        print()
        print(f"   {Colors.muted('Ví dụ:')} {Colors.secondary('r1')} (chạy tool recent đầu tiên)")
        print()
        
        # Activate/Deactivate
        print(Colors.bold("🔧 ACTIVATE/DEACTIVATE:"))
        print(f"   {Colors.info('off [số]')}      - Vô hiệu hóa tool từ menu hiện tại")
        print(f"   {Colors.info('on [số]')}       - Kích hoạt tool từ danh sách disabled")
        print(f"   {Colors.info('disabled')}      - Hiển thị danh sách tools bị disabled")
        print()
        print(f"   {Colors.muted('Hỗ trợ nhiều tool:')} {Colors.secondary('off 1 2 3')} hoặc {Colors.secondary('off 1,2,3')}")
        print(f"   {Colors.muted('Ví dụ:')} {Colors.secondary('off 3')}, {Colors.secondary('off 1 2 3')}, {Colors.secondary('on 2 5')}")
        print()
        print(f"   {Colors.muted('Lưu ý:')} {Colors.secondary('off [số]')} dùng số từ menu active,")
        print(f"            {Colors.secondary('on [số]')} dùng số từ danh sách disabled (xem bằng 'disabled')")
        print()
        
        # Settings
        print(Colors.bold("⚙️  SETTINGS:"))
        print(f"   {Colors.info('set')}          - Xem/chỉnh sửa settings")
        print()
        
        # Khác
        print(Colors.bold("🔄 KHÁC:"))
        print(f"   {Colors.info('l, list')}      - Hiển thị lại danh sách")
        print(f"   {Colors.info('clear')}        - Xóa màn hình")
        print()
        
        print_separator("═", 70, Colors.PRIMARY)
        print()
    
    def show_tool_help(self, tool: str) -> bool:
        """
        Hiển thị hướng dẫn sử dụng của tool (từ doc.py)
        
        Args:
            tool: Tên file tool (vd: backup-folder.py)
        
        Returns:
            bool: True nếu đọc được doc.py, False nếu không tìm thấy
        
        Giải thích:
        - Bước 1: Tìm thư mục chứa tool (tools/py/ hoặc tools/sh/)
        - Bước 2: Import module doc.py từ thư mục đó
        - Bước 3: Gọi hàm get_help() hoặc đọc biến HELP_TEXT
        - Bước 4: Hiển thị nội dung hướng dẫn
        - Bước 5: Nếu không có doc.py, hiển thị thông báo
        """
        tool_name = tool.replace('.py', '')
        
        # Tìm file doc.py trong tools/py/ trước
        tool_dir_path = self.tool_dir / "py" / tool_name
        doc_path = tool_dir_path / "doc.py"
        
        # Nếu không có trong py/, thử tìm trong sh/
        if not doc_path.exists():
            tool_dir_path = self.tool_dir / "sh" / tool_name
            doc_path = tool_dir_path / "doc.py"
        
        # Nếu vẫn không có, thử cấu trúc cũ
        if not doc_path.exists():
            tool_dir_path = self.tool_dir / tool_name
            doc_path = tool_dir_path / "doc.py"
        
        if not doc_path.exists():
            # Thông báo không tìm thấy doc.py
            tool_display_name = self.get_tool_display_name(tool)
            print()
            print_separator("═", 70, Colors.ERROR)
            print(Colors.error(f"❌ Không tìm thấy hướng dẫn cho tool: {tool_display_name}"))
            print(Colors.muted(f"   File doc.py không tồn tại trong {tool_name}/"))
            print_separator("═", 70, Colors.ERROR)
            print()
            return False
        
        # Import và đọc doc.py
        try:
            # Thêm thư mục tool vào sys.path để import
            if str(tool_dir_path) not in sys.path:
                sys.path.insert(0, str(tool_dir_path))
            
            # Import module doc
            import importlib.util
            spec = importlib.util.spec_from_file_location(f"{tool_name}.doc", doc_path)
            doc_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(doc_module)
            
            # Lấy hướng dẫn từ module
            # Ưu tiên hàm get_help(), nếu không có thì dùng biến HELP_TEXT
            if hasattr(doc_module, 'get_help'):
                help_text = doc_module.get_help()
            elif hasattr(doc_module, 'HELP_TEXT'):
                help_text = doc_module.HELP_TEXT
            else:
                tool_display_name = self.get_tool_display_name(tool)
                print()
                print_separator("═", 70, Colors.ERROR)
                print(Colors.error(f"❌ File doc.py không có hàm get_help() hoặc biến HELP_TEXT"))
                print(Colors.muted(f"   Tool: {tool_display_name}"))
                print_separator("═", 70, Colors.ERROR)
                print()
                return False
            
            # Hiển thị hướng dẫn
            tool_display_name = self.get_tool_display_name(tool)
            print()
            print_separator("═", 70, Colors.INFO)
            title = Colors.info(f"📖 HƯỚNG DẪN SỬ DỤNG: {Colors.bold(tool_display_name)}")
            print(f"  {title}")
            print_separator("═", 70, Colors.INFO)
            print()
            print(help_text)
            print()
            print_separator("═", 70, Colors.INFO)
            print()
            
            return True
            
        except Exception as e:
            tool_display_name = self.get_tool_display_name(tool)
            print()
            print_separator("═", 70, Colors.ERROR)
            print(Colors.error(f"❌ Lỗi khi đọc hướng dẫn cho tool: {tool_display_name}"))
            print(Colors.muted(f"   Lỗi: {e}"))
            print_separator("═", 70, Colors.ERROR)
            print()
            import traceback
            traceback.print_exc()
            return False

