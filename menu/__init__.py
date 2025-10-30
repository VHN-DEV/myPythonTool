#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Menu chính - Giao diện quản lý và chạy các tools

Mục đích: Entry point cho menu system
Lý do: Dễ dàng truy cập và quản lý tools
"""

import os
import sys

# Fix Windows console encoding - Simple way
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Import ToolManager từ module riêng
from .tool_manager import ToolManager


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
╔══════════════════════════════════════════════════════════╗
║                  MY PYTHON TOOLS                         ║
║              Bộ công cụ Python tiện ích                  ║
║                                                          ║
║         Nhập 'h' hoặc 'help' để xem hướng dẫn            ║
╚══════════════════════════════════════════════════════════╝
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
