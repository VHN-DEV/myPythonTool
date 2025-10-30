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
        self.config_file = Path("tool_config.json")
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
        - Bước 1: Lấy tất cả file .py trong thư mục tool (bao gồm cả trong thư mục con)
        - Bước 2: Tách ra priority tools và tools thường
        - Bước 3: Sắp xếp priority tools theo thứ tự định sẵn
        - Bước 4: Sắp xếp tools thường theo alphabet
        - Bước 5: Ghép lại: priority + alphabet
        
        Lý do tìm trong thư mục con:
        - Hỗ trợ cấu trúc mới: mỗi tool có thư mục riêng
        - Ví dụ: tool/backup-folder/backup-folder.py
        """
        if not self.tool_dir.exists():
            return []
        
        all_tools = []
        
        # Duyệt qua các thư mục con trong tool/
        for item in os.listdir(self.tool_dir):
            item_path = self.tool_dir / item
            
            # Nếu là thư mục, tìm file .py chính trong đó
            if item_path.is_dir():
                # Tìm file có tên giống thư mục
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
        """
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
    
    def _find_tool_path(self, tool: str) -> Optional[Path]:
        """
        Tìm đường dẫn thực tế của tool
        
        Args:
            tool: Tên file tool (vd: backup-folder.py)
        
        Returns:
            Path: Đường dẫn đầy đủ đến file tool, hoặc None nếu không tìm thấy
        
        Giải thích:
        - Bước 1: Thử tìm trong thư mục con (cấu trúc mới)
        - Bước 2: Nếu không có, thử tìm trực tiếp (cấu trúc cũ)
        
        Lý do:
        - Hỗ trợ cả 2 cấu trúc để dễ migration
        - Ưu tiên cấu trúc mới (thư mục con)
        """
        tool_name = tool.replace('.py', '')
        
        # Thử cấu trúc mới: tool/backup-folder/backup-folder.py
        new_structure_path = self.tool_dir / tool_name / tool
        if new_structure_path.exists():
            return new_structure_path
        
        # Thử cấu trúc cũ: tool/backup-folder.py
        old_structure_path = self.tool_dir / tool
        if old_structure_path.exists():
            return old_structure_path
        
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

