#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Menu chính - Quản lý và chạy các tools

Mục đích: Giao diện tập trung cho tất cả tools
Lý do: Dễ dàng truy cập và quản lý tools
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Fix Windows console encoding - Simple way
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass


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
            list: Danh sách tên file tool
        """
        if not self.tool_dir.exists():
            return []
        
        tools = [f for f in os.listdir(self.tool_dir) if f.endswith('.py')]
        tools.sort()  # Sắp xếp theo alphabet
        return tools
    
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
        - Chạy tool bằng subprocess
        - Lưu vào recent
        - Hiển thị thông báo
        """
        tool_path = self.tool_dir / tool
        
        if not tool_path.exists():
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
        print(f"  {title}")
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


def main():
    """
    Hàm main - Menu chính
    
    Giải thích:
    - Vòng lặp chính của menu
    - Xử lý input từ người dùng
    - Dispatch đến các chức năng tương ứng
    """
    # Khởi tạo ToolManager
    # __file__ là menu/__init__.py, cần lùi 1 cấp lên project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tool_dir = os.path.join(project_root, "tool")
    manager = ToolManager(tool_dir)
    
    # Lấy danh sách tools
    tools = manager.get_tool_list()
    
    if not tools:
        print("❌ Không tìm thấy tool nào trong thư mục tool/")
        return
    
    # Hiển thị banner
    print("""
============================================================
                  MY PYTHON TOOLS                         
              Bo cong cu Python tien ich                 
                                                          
         Nhap 'h' hoac 'help' de xem huong dan          
============================================================
    """)
    
    # Hiển thị menu lần đầu
    manager.display_menu(tools)
    
    # Vòng lặp chính
    while True:
        try:
            # Nhận input
            user_input = input(">>> Chọn tool (h=help, q=quit): ").strip()
            
            if not user_input:
                continue
            
            # Parse command
            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""
            
            # Xử lý command
            
            # Thoát
            if command in ['q', 'quit', '0', 'exit']:
                print("👋 Tạm biệt!")
                break
            
            # Help
            elif command in ['h', 'help', '?']:
                manager.show_help()
            
            # List
            elif command in ['l', 'list']:
                manager.display_menu(tools)
            
            # Clear
            elif command == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
                manager.display_menu(tools)
            
            # Search
            elif command in ['s', 'search'] or command.startswith('/'):
                if command.startswith('/'):
                    query = command[1:] + (" " + args if args else "")
                else:
                    query = args
                
                if not query:
                    print("⚠️  Vui lòng nhập từ khóa tìm kiếm")
                    continue
                
                results = manager.search_tools(query)
                
                if results:
                    print(f"\n🔍 Tìm thấy {len(results)} tool phù hợp với '{query}':")
                    manager.display_menu(results, title=f"KẾT QUẢ TÌM KIẾM: {query}")
                else:
                    print(f"❌ Không tìm thấy tool nào phù hợp với '{query}'")
            
            # Favorites
            elif command == 'f':
                favorites = manager.config['favorites']
                if favorites:
                    valid_favorites = [f for f in favorites if f in tools]
                    manager.display_menu(valid_favorites, title="FAVORITES")
                else:
                    print("⭐ Chưa có favorites nào")
            
            elif command.startswith('f+'):
                # Thêm vào favorites
                try:
                    idx = int(args or command[2:])
                    if 1 <= idx <= len(tools):
                        tool = tools[idx - 1]
                        manager.add_to_favorites(tool)
                    else:
                        print("❌ Số không hợp lệ")
                except ValueError:
                    print("❌ Số không hợp lệ")
            
            elif command.startswith('f-'):
                # Xóa khỏi favorites
                try:
                    idx = int(args or command[2:])
                    if 1 <= idx <= len(tools):
                        tool = tools[idx - 1]
                        manager.remove_from_favorites(tool)
                    else:
                        print("❌ Số không hợp lệ")
                except ValueError:
                    print("❌ Số không hợp lệ")
            
            # Recent
            elif command == 'r':
                recent = manager.config['recent']
                if recent:
                    # Lọc chỉ những tool còn tồn tại
                    valid_recent = [r for r in recent if r in tools]
                    manager.display_menu(valid_recent, title="RECENT TOOLS")
                else:
                    print("📚 Chưa có recent tools")
            
            elif command.startswith('r') and len(command) > 1:
                # Chạy recent tool
                try:
                    idx = int(command[1:])
                    recent = manager.config['recent']
                    
                    if 1 <= idx <= len(recent):
                        tool = recent[idx - 1]
                        if tool in tools:
                            manager.run_tool(tool)
                            manager.display_menu(tools)
                        else:
                            print(f"❌ Tool không tồn tại: {tool}")
                    else:
                        print("❌ Số không hợp lệ")
                except ValueError:
                    print("❌ Số không hợp lệ")
            
            # Settings
            elif command == 'set':
                print("\n⚙️  SETTINGS:")
                for key, value in manager.config['settings'].items():
                    print(f"   {key}: {value}")
                print()
            
            # Chạy tool theo số
            elif command.isdigit():
                idx = int(command)
                
                if 1 <= idx <= len(tools):
                    tool = tools[idx - 1]
                    manager.run_tool(tool)
                    # Hiển thị lại menu
                    manager.display_menu(tools)
                else:
                    print("❌ Số không hợp lệ")
            
            else:
                print(f"❌ Lệnh không hợp lệ: {command}")
                print("💡 Nhập 'h' hoặc 'help' để xem hướng dẫn")
        
        except KeyboardInterrupt:
            print("\n\n👋 Tạm biệt!")
            break
        
        except Exception as e:
            print(f"\n❌ Lỗi: {e}")


if __name__ == "__main__":
    main()
