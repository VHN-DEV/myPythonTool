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
        
        # Ánh xạ tên file sang tên hiển thị tiếng Việt
        self.tool_names = {
            "ssh-manager.py": "Quản lý và kết nối SSH Server nhanh chóng",
            "backup-folder.py": "Sao lưu và nén thư mục (có timestamp)",
            "clean-temp-files.py": "Dọn dẹp file tạm, cache và file rác",
            "compress-images.py": "Nén và chỉnh sửa ảnh (resize, đổi format)",
            "copy-changed-files.py": "Sao chép file thay đổi theo Git commit",
            "duplicate-finder.py": "Tìm và xóa file trùng lặp",
            "extract-archive.py": "Giải nén file (ZIP, RAR, 7Z, TAR)",
            "file-organizer.py": "Sắp xếp file (theo loại/ngày/extension)",
            "find-and-replace.py": "Tìm và thay thế text trong nhiều file",
            "generate-tree.py": "Tạo sơ đồ cây thư mục dự án",
            "image-watermark.py": "Thêm watermark vào ảnh (text/logo hàng loạt)",
            "pdf-tools.py": "Xử lý PDF (merge, split, compress, convert)",
            "rename-files.py": "Đổi tên file hàng loạt (prefix/suffix/số thứ tự)",
            "setup-project-linux.py": "Quản lý và cài đặt dự án (Linux/Ubuntu)",
            "text-encoding-converter.py": "Chuyển đổi encoding file text (UTF-8, ANSI...)",
            "video-converter.py": "Xử lý video (convert, compress, trim, extract audio)"
        }
        
        # Tags cho mỗi tool (để search)
        self.tool_tags = {
            "ssh-manager.py": ["ssh", "server", "ket noi", "remote", "terminal"],
            "backup-folder.py": ["backup", "sao luu", "nen", "zip", "tar"],
            "clean-temp-files.py": ["clean", "don dep", "temp", "cache", "rac"],
            "compress-images.py": ["image", "anh", "nen", "resize", "compress"],
            "copy-changed-files.py": ["git", "copy", "sao chep", "commit"],
            "duplicate-finder.py": ["duplicate", "trung lap", "xoa", "clean"],
            "extract-archive.py": ["extract", "giai nen", "zip", "rar", "7z"],
            "file-organizer.py": ["organize", "sap xep", "file", "thu muc"],
            "find-and-replace.py": ["find", "replace", "tim", "thay the", "text"],
            "generate-tree.py": ["tree", "cay", "thu muc", "structure"],
            "image-watermark.py": ["watermark", "anh", "logo", "copyright"],
            "pdf-tools.py": ["pdf", "merge", "split", "compress"],
            "rename-files.py": ["rename", "doi ten", "batch"],
            "setup-project-linux.py": ["linux", "server", "setup", "cai dat", "nginx", "php", "mysql"],
            "text-encoding-converter.py": ["encoding", "utf8", "text", "convert"],
            "video-converter.py": ["video", "convert", "compress", "mp4"]
        }
        
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
        - Lưu favorites, recent tools, settings
        - Tạo config mặc định nếu chưa có
        """
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        
        # Config mặc định
        return {
            'favorites': [],
            'recent': [],
            'settings': {
                'show_descriptions': True,
                'max_recent': 10
            }
        }
    
    def _save_config(self):
        """Lưu config ra file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  Lỗi lưu config: {e}")
    
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
            description = self.tool_names.get(tool, "")
            if query in description.lower():
                results.append(tool)
                continue
            
            # Tìm trong tags
            tags = self.tool_tags.get(tool, [])
            if any(query in tag for tag in tags):
                results.append(tool)
        
        return results
    
    def add_to_favorites(self, tool: str):
        """Thêm tool vào favorites"""
        if tool not in self.config['favorites']:
            self.config['favorites'].append(tool)
            self._save_config()
            print(f"⭐ Đã thêm vào favorites: {self.tool_names.get(tool, tool)}")
    
    def remove_from_favorites(self, tool: str):
        """Xóa tool khỏi favorites"""
        if tool in self.config['favorites']:
            self.config['favorites'].remove(tool)
            self._save_config()
            print(f"❌ Đã xóa khỏi favorites: {self.tool_names.get(tool, tool)}")
    
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
            print(f"❌ Tool không tồn tại: {tool}")
            return 1
        
        print(f"\n{'='*60}")
        print(f">>> Đang chạy: {self.tool_names.get(tool, tool)}")
        print(f"{'='*60}\n")
        
        try:
            result = subprocess.run(["python", str(tool_path)])
            
            print(f"\n{'='*60}")
            print(f">>> Tool đã chạy xong!")
            print(f"{'='*60}\n")
            
            # Lưu vào recent
            self.add_to_recent(tool)
            
            return result.returncode
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Tool bị ngắt bởi người dùng")
            return 130
            
        except Exception as e:
            print(f"\n❌ Lỗi khi chạy tool: {e}")
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
        print(f">>> Đang chạy: {self.tool_names.get('setup-project-linux.py', 'setup-project-linux')}")
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
            
            print(f"\n{'='*60}")
            print(f">>> Tool đã chạy xong!")
            print(f"{'='*60}\n")
            
            # Lưu vào recent
            self.add_to_recent("setup-project-linux.py")
            
            return result.returncode
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Tool bị ngắt bởi người dùng")
            return 130
            
        except Exception as e:
            print(f"\n❌ Lỗi khi chạy tool: {e}")
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
    
    def display_menu(self, tools: Optional[List[str]] = None, title: str = "DANH SÁCH TOOL"):
        """
        Hiển thị menu tools
        
        Args:
            tools: Danh sách tools (None = hiển thị tất cả)
            title: Tiêu đề menu
        
        Giải thích:
        - Hiển thị danh sách đẹp với số thứ tự
        - Highlight favorites
        - Hiển thị description
        """
        if tools is None:
            tools = self.get_tool_list()
        
        if not tools:
            print("❌ Không tìm thấy tool nào!")
            return
        
        print(f"\n{'='*60}")
        print(f"                   {title}")
        print(f"{'='*60}")
        
        for idx, tool in enumerate(tools, start=1):
            # Check favorite
            is_favorite = tool in self.config['favorites']
            star = "⭐" if is_favorite else "  "
            
            # Tên tool
            tool_name = self.tool_names.get(tool, tool)
            
            # Hiển thị
            print(f"{star} {idx}. {tool_name}")
        
        print(f"{'='*60}\n")
    
    def show_help(self):
        """Hiển thị help"""
        print("""
============================================================
                  HUONG DAN SU DUNG                       
============================================================

📋 LỆNH CƠ BẢN:
   [số]         - Chạy tool theo số thứ tự
   [số]h        - Xem hướng dẫn của tool (ví dụ: 1h, 4h)
   h, help      - Hiển thị hướng dẫn này
   q, quit, 0   - Thoát chương trình

🔍 TÌM KIẾM:
   s [keyword]  - Tìm kiếm tool
   /[keyword]   - Tìm kiếm tool (cách khác)
   
   Ví dụ: s backup, /image

⭐ FAVORITES:
   f            - Hiển thị danh sách favorites
   f+ [số]      - Thêm tool vào favorites
   f- [số]      - Xóa tool khỏi favorites
   
   Ví dụ: f+ 3, f- 1

📚 RECENT:
   r            - Hiển thị recent tools
   r[số]        - Chạy recent tool
   
   Ví dụ: r1 (chạy tool recent đầu tiên)

⚙️  SETTINGS:
   set          - Xem/chỉnh sửa settings

🔄 KHÁC:
   l, list      - Hiển thị lại danh sách
   clear        - Xóa màn hình
        """)
    
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
            tool_display_name = self.tool_names.get(tool, tool)
            print(f"\n{'='*60}")
            print(f"❌ Không tìm thấy hướng dẫn cho tool: {tool_display_name}")
            print(f"   File doc.py không tồn tại trong {tool_name}/")
            print(f"{'='*60}\n")
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
                tool_display_name = self.tool_names.get(tool, tool)
                print(f"\n{'='*60}")
                print(f"❌ File doc.py không có hàm get_help() hoặc biến HELP_TEXT")
                print(f"   Tool: {tool_display_name}")
                print(f"{'='*60}\n")
                return False
            
            # Hiển thị hướng dẫn
            tool_display_name = self.tool_names.get(tool, tool)
            print(f"\n{'='*60}")
            print(f"📖 HƯỚNG DẪN SỬ DỤNG: {tool_display_name}")
            print(f"{'='*60}\n")
            print(help_text)
            print(f"{'='*60}\n")
            
            return True
            
        except Exception as e:
            tool_display_name = self.tool_names.get(tool, tool)
            print(f"\n{'='*60}")
            print(f"❌ Lỗi khi đọc hướng dẫn cho tool: {tool_display_name}")
            print(f"   Lỗi: {e}")
            print(f"{'='*60}\n")
            import traceback
            traceback.print_exc()
            return False

