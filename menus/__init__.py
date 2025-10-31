#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Menu chính - Giao diện quản lý và chạy các tools

Mục đích: Entry point cho menu system
Lý do: Dễ dàng truy cập và quản lý tools
"""

import os
import sys
import re

# Fix Windows console encoding - Improved
if sys.platform == 'win32':
    try:
        # Thiết lập UTF-8 cho console output
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
        
        # Thiết lập UTF-8 cho console input (quan trọng cho EOFError)
        sys.stdin.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        # Fallback: sử dụng wrapper
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')

# Import ToolManager từ module riêng
from .tool_manager import ToolManager
from utils.colors import Colors
from utils.format import print_separator
from utils.helpers import print_welcome_tip, print_command_suggestions, suggest_command


def safe_print(text, fallback_text=None):
    """
    In text an toàn với fallback cho encoding errors
    
    Args:
        text: Text cần in (có thể chứa emoji/unicode)
        fallback_text: Text dự phòng nếu không in được (ASCII)
    
    Giải thích:
    - Cố gắng in text gốc với emoji
    - Nếu lỗi encoding, dùng fallback
    - Nếu không có fallback, bỏ qua emoji
    """
    try:
        print(text)
    except UnicodeEncodeError:
        if fallback_text:
            print(fallback_text)
        else:
            # Loại bỏ emoji và in lại
            import re
            ascii_text = re.sub(r'[^\x00-\x7F]+', '', text)
            print(ascii_text)


def _run_tool_loop(manager, tool, tools):
    """
    Chạy tool với vòng lặp riêng - tự động quay lại đầu tool khi kết thúc
    
    Args:
        manager: ToolManager instance
        tool: Tên tool cần chạy
        tools: Danh sách tools để hiển thị menu khi thoát
    
    Giải thích:
    - Bước 1: Chạy tool lần đầu
    - Bước 2: Kiểm tra exit code từ tool
    - Bước 3: Nếu exit code là 130 (KeyboardInterrupt), quay về menu chính
    - Bước 4: Nếu exit code là 0 (thành công), tự động chạy lại tool đó
    - Bước 5: Nếu có lỗi khác, quay về menu chính
    
    Lý do:
    - Giúp người dùng tiếp tục làm việc với cùng một tool mà không cần quay về menu chính
    - Tiết kiệm thời gian và thao tác
    - Cho phép người dùng nhấn Ctrl+C để quay về menu chính
    """
    # Vòng lặp cho tool - tự động chạy lại khi kết thúc
    while True:
        try:
            # Chạy tool và lấy exit code
            exit_code = manager.run_tool(tool)
            
            # Kiểm tra exit code
            # 130 là exit code khi người dùng nhấn Ctrl+C (KeyboardInterrupt)
            if exit_code == 130:
                # Người dùng nhấn Ctrl+C trong tool - quay về menu chính
                print()
                print(Colors.info("🔄 Quay lại menu chính..."))
                print()
                manager.display_menu(tools)
                break
            
            # Exit code 0 (thành công) hoặc code khác - tự động chạy lại tool
            # Không cần hiển thị menu chính, chỉ chạy lại tool
            continue
            
        except KeyboardInterrupt:
            # Người dùng nhấn Ctrl+C trong vòng lặp tool (ngoài tool)
            # Quay về menu chính
            print()
            print(Colors.info("🔄 Quay lại menu chính..."))
            print()
            manager.display_menu(tools)
            break
        
        except Exception as e:
            # Xử lý lỗi khác
            try:
                print()
                print(Colors.error(f"❌ Lỗi khi chạy tool: {e}"))
                print(Colors.info("🔄 Quay lại menu chính..."))
                print()
                manager.display_menu(tools)
            except Exception:
                print(f"\nLoi: {str(e)}")
            break


def main():
    """
    Hàm main - Menu chính
    
    Giải thích:
    - Vòng lặp chính của menu
    - Xử lý input từ người dùng
    - Dispatch đến các chức năng tương ứng
    """
    # Khởi tạo ToolManager
    # __file__ là menus/__init__.py, cần lùi 1 cấp lên project root
    from pathlib import Path
    project_root = Path(__file__).parent.parent
    tool_dir = str(project_root / "tools")
    manager = ToolManager(tool_dir)
    
    # Lấy danh sách tools
    tools = manager.get_tool_list()
    
    if not tools:
        print(Colors.error("❌ Không tìm thấy tool nào trong thư mục tools/"))
        return
    
    # Hiển thị banner đẹp hơn
    print()
    
    # Logo/Title
    title_line1 = Colors.primary("  ╔═══════════════════════════════════════════════════════╗")
    title_line2 = Colors.primary("  ║") + Colors.bold(Colors.info("                  MY PYTHON TOOLS")) + Colors.primary("                      ║")
    title_line3 = Colors.primary("  ║") + Colors.secondary("              Bộ công cụ Python tiện ích") + Colors.primary("               ║")
    title_line4 = Colors.primary("  ║") + " " * 55 + Colors.primary("║")
    title_line5 = Colors.primary("  ║") + Colors.muted("         Nhập 'h' hoặc 'help' để xem hướng dẫn") + Colors.primary("         ║")
    title_line6 = Colors.primary("  ╚═══════════════════════════════════════════════════════╝")
    
    print(title_line1)
    print(title_line2)
    print(title_line3)
    print(title_line4)
    print(title_line5)
    print(title_line6)
    
    print()
    
    # Welcome tip
    print_welcome_tip()
    print()
    
    # Hiển thị menu lần đầu
    manager.display_menu(tools)
    
    # Vòng lặp chính
    while True:
        try:
            # Nhận input với prompt đẹp hơn
            prompt = Colors.primary(">>> ") + Colors.secondary("Chọn tool") + Colors.muted(" (h=help, q=quit): ")
            user_input = input(prompt).strip()
            
            if not user_input:
                continue
            
            # Parse command
            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""
            
            # Xử lý command
            
            # Thoát
            if command in ['q', 'quit', '0', 'exit']:
                print(Colors.info("👋 Tạm biệt!"))
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
                    print(Colors.warning("⚠️  Vui lòng nhập từ khóa tìm kiếm"))
                    continue
                
                results = manager.search_tools(query)
                
                if results:
                    count_msg = Colors.success(f"{len(results)}")
                    query_msg = Colors.secondary(f"'{query}'")
                    print()
                    print(Colors.info(f"🔍 Tìm thấy {count_msg} tool phù hợp với {query_msg}:"))
                    manager.display_menu(results, title=f"KẾT QUẢ TÌM KIẾM: {query}", group_by_category=False, search_query=query)
                else:
                    print(Colors.error(f"❌ Không tìm thấy tool nào phù hợp với '{query}'"))
                    # Gợi ý các tools gần đúng
                    all_tools = manager.get_tool_list()
                    suggestions = suggest_command(query, [manager.get_tool_display_name(t) for t in all_tools][:10])
                    if suggestions:
                        print()
                        print(Colors.info(f"💡 Gợi ý tìm kiếm: {', '.join([Colors.secondary(s) for s in suggestions[:3]])}"))
            
            # Favorites
            elif command == 'f':
                favorites = manager.config['favorites']
                if favorites:
                    valid_favorites = [f for f in favorites if f in tools]
                    manager.display_menu(valid_favorites, title="FAVORITES")
                else:
                    print(Colors.warning("⭐ Chưa có favorites nào"))
            
            elif command.startswith('f+'):
                # Thêm vào favorites
                try:
                    idx = int(args or command[2:])
                    if 1 <= idx <= len(tools):
                        tool = tools[idx - 1]
                        manager.add_to_favorites(tool)
                    else:
                        print(Colors.error("❌ Số không hợp lệ"))
                except ValueError:
                    print(Colors.error("❌ Số không hợp lệ"))
            
            elif command.startswith('f-'):
                # Xóa khỏi favorites
                try:
                    idx = int(args or command[2:])
                    if 1 <= idx <= len(tools):
                        tool = tools[idx - 1]
                        manager.remove_from_favorites(tool)
                    else:
                        print(Colors.error("❌ Số không hợp lệ"))
                except ValueError:
                    print(Colors.error("❌ Số không hợp lệ"))
            
            # Recent
            elif command == 'r':
                recent = manager.config['recent']
                if recent:
                    # Lọc chỉ những tool còn tồn tại
                    valid_recent = [r for r in recent if r in tools]
                    manager.display_menu(valid_recent, title="RECENT TOOLS")
                else:
                    print(Colors.warning("📚 Chưa có recent tools"))
            
            elif command.startswith('r') and len(command) > 1:
                # Chạy recent tool
                try:
                    idx = int(command[1:])
                    recent = manager.config['recent']
                    
                    if 1 <= idx <= len(recent):
                        tool = recent[idx - 1]
                        if tool in tools:
                            # Chạy tool với vòng lặp riêng - quay lại đầu tool khi kết thúc
                            _run_tool_loop(manager, tool, tools)
                        else:
                            print(Colors.error(f"❌ Tool không tồn tại: {tool}"))
                    else:
                        print(Colors.error("❌ Số không hợp lệ"))
                except ValueError:
                    print(Colors.error("❌ Số không hợp lệ"))
            
            # Activate/Deactivate tools
            elif command.startswith('on') or command.startswith('activate'):
                # Kích hoạt tool từ danh sách disabled (hỗ trợ nhiều tool)
                try:
                    idx_str = args or (command[2:].lstrip() if command.startswith('on') else "")
                    disabled_tools = manager.config.get('disabled_tools', [])
                    all_tools = manager.get_all_tools_including_disabled()
                    valid_disabled = [t for t in disabled_tools if t in all_tools]
                    
                    if not valid_disabled:
                        print(Colors.warning("⚠️  Không có tool nào bị disabled"))
                        continue
                    
                    if not idx_str:
                        # Nếu không có số, hiển thị danh sách disabled để user chọn
                        print(Colors.info("💡 Danh sách tools bị disabled:"))
                        manager.display_menu(valid_disabled, title="DISABLED TOOLS", group_by_category=False)
                        print(Colors.info("💡 Sử dụng 'on [số]' để kích hoạt lại tool (ví dụ: on 1 hoặc on 1 2 3)"))
                        continue
                    
                    # Parse nhiều số (hỗ trợ cả space và comma)
                    # Tách số từ string (hỗ trợ space, comma, hoặc cả hai)
                    numbers_str = re.split(r'[,\s]+', idx_str.strip())
                    numbers = []
                    for num_str in numbers_str:
                        if num_str.strip():
                            try:
                                num = int(num_str.strip())
                                numbers.append(num)
                            except ValueError:
                                print(Colors.error(f"❌ Số không hợp lệ: {num_str}"))
                    
                    if not numbers:
                        print(Colors.error("❌ Không có số hợp lệ nào"))
                        continue
                    
                    # Xử lý từng số
                    activated_count = 0
                    invalid_numbers = []
                    for idx in numbers:
                        if 1 <= idx <= len(valid_disabled):
                            tool = valid_disabled[idx - 1]
                            # Activate tool (không in thông báo ngay)
                            if tool in manager.config['disabled_tools']:
                                manager.config['disabled_tools'].remove(tool)
                                activated_count += 1
                                tool_name = manager.get_tool_display_name(tool)
                                print(Colors.success(f"✅ Đã kích hoạt: {Colors.bold(tool_name)}"))
                            else:
                                tool_name = manager.get_tool_display_name(tool)
                                print(Colors.warning(f"ℹ️  Tool đã được kích hoạt: {tool_name}"))
                        else:
                            invalid_numbers.append(idx)
                    
                    # Lưu config nếu có thay đổi
                    if activated_count > 0:
                        manager._save_config()
                        # Refresh tools list
                        tools = manager.get_tool_list()
                        print()
                        print(Colors.success(f"📊 Đã kích hoạt {activated_count} tool(s)"))
                    
                    if invalid_numbers:
                        print(Colors.error(f"❌ Số không hợp lệ: {', '.join(map(str, invalid_numbers))}"))
                        print(Colors.info(f"💡 Vui lòng nhập số từ 1 đến {len(valid_disabled)}"))
                        
                except Exception as e:
                    print(Colors.error(f"❌ Lỗi: {e}"))
                    # Tự động hiển thị danh sách disabled
                    disabled_tools = manager.config.get('disabled_tools', [])
                    all_tools = manager.get_all_tools_including_disabled()
                    valid_disabled = [t for t in disabled_tools if t in all_tools]
                    if valid_disabled:
                        print()
                        print(Colors.info("💡 Danh sách tools bị disabled:"))
                        manager.display_menu(valid_disabled, title="DISABLED TOOLS", group_by_category=False)
            
            elif command.startswith('off') or command.startswith('deactivate'):
                # Vô hiệu hóa tool từ danh sách active (menu hiện tại, hỗ trợ nhiều tool)
                try:
                    idx_str = args or (command[3:].lstrip() if command.startswith('off') else "")
                    if not idx_str:
                        print(Colors.warning("⚠️  Vui lòng nhập số thứ tự tool cần vô hiệu hóa"))
                        print(Colors.info(f"💡 Sử dụng số từ 1 đến {len(tools)} (ví dụ: off 1 hoặc off 1 2 3)"))
                        continue
                    
                    # Parse nhiều số (hỗ trợ cả space và comma)
                    # Tách số từ string (hỗ trợ space, comma, hoặc cả hai)
                    numbers_str = re.split(r'[,\s]+', idx_str.strip())
                    numbers = []
                    for num_str in numbers_str:
                        if num_str.strip():
                            try:
                                num = int(num_str.strip())
                                numbers.append(num)
                            except ValueError:
                                print(Colors.error(f"❌ Số không hợp lệ: {num_str}"))
                    
                    if not numbers:
                        print(Colors.error("❌ Không có số hợp lệ nào"))
                        continue
                    
                    # Xử lý từng số
                    deactivated_count = 0
                    invalid_numbers = []
                    for idx in numbers:
                        if 1 <= idx <= len(tools):
                            tool = tools[idx - 1]
                            # Deactivate tool (không in thông báo ngay)
                            if tool not in manager.config['disabled_tools']:
                                manager.config['disabled_tools'].append(tool)
                                deactivated_count += 1
                                tool_name = manager.get_tool_display_name(tool)
                                print(Colors.warning(f"⚠️  Đã vô hiệu hóa: {Colors.bold(tool_name)}"))
                            else:
                                tool_name = manager.get_tool_display_name(tool)
                                print(Colors.warning(f"ℹ️  Tool đã bị vô hiệu hóa: {tool_name}"))
                        else:
                            invalid_numbers.append(idx)
                    
                    # Lưu config nếu có thay đổi
                    if deactivated_count > 0:
                        manager._save_config()
                        # Refresh tools list
                        tools = manager.get_tool_list()
                        print()
                        print(Colors.success(f"📊 Đã vô hiệu hóa {deactivated_count} tool(s)"))
                        # Hiển thị lại menu nếu còn tools
                        if tools:
                            manager.display_menu(tools)
                        else:
                            print(Colors.warning("⚠️  Tất cả tools đã bị vô hiệu hóa"))
                            print(Colors.info("💡 Sử dụng 'on [số]' hoặc 'disabled' để kích hoạt lại"))
                    
                    if invalid_numbers:
                        print(Colors.error(f"❌ Số không hợp lệ: {', '.join(map(str, invalid_numbers))}"))
                        print(Colors.info(f"💡 Vui lòng nhập số từ 1 đến {len(tools)}"))
                        
                except Exception as e:
                    print(Colors.error(f"❌ Lỗi: {e}"))
            
            elif command == 'disabled':
                # Hiển thị danh sách tools bị disabled
                disabled_tools = manager.config.get('disabled_tools', [])
                if disabled_tools:
                    # Lấy tất cả tools để mapping số thứ tự
                    all_tools = manager.get_all_tools_including_disabled()
                    # Chỉ lấy những tool disabled và còn tồn tại
                    valid_disabled = [t for t in disabled_tools if t in all_tools]
                    if valid_disabled:
                        manager.display_menu(valid_disabled, title="DISABLED TOOLS", group_by_category=False)
                        print(Colors.info("💡 Sử dụng 'on [số]' để kích hoạt lại tool"))
                    else:
                        print(Colors.warning("⚠️  Không có tool nào bị disabled"))
                else:
                    print(Colors.warning("⚠️  Không có tool nào bị disabled"))
            
            # Settings
            elif command == 'set':
                print()
                print_separator("─", 70, Colors.INFO)
                print(Colors.bold("⚙️  SETTINGS:"))
                for key, value in manager.config['settings'].items():
                    key_colored = Colors.info(key)
                    value_colored = Colors.secondary(str(value))
                    print(f"   {key_colored}: {value_colored}")
                
                # Hiển thị số disabled tools
                disabled_count = len(manager.config.get('disabled_tools', []))
                if disabled_count > 0:
                    print(f"   {Colors.info('disabled_tools')}: {Colors.error(str(disabled_count))}")
                print_separator("─", 70, Colors.INFO)
                print()
            
            # Hiển thị hướng dẫn tool (pattern: số+h, ví dụ: 1h, 4h)
            elif command.endswith('h') and len(command) > 1 and command[:-1].isdigit():
                try:
                    # Lấy số từ đầu command (bỏ 'h' ở cuối)
                    idx = int(command[:-1])
                    
                    if 1 <= idx <= len(tools):
                        tool = tools[idx - 1]
                        # Hiển thị hướng dẫn của tool
                        manager.show_tool_help(tool)
                    else:
                        print(Colors.error("❌ Số không hợp lệ"))
                except ValueError:
                    # Không phải pattern số+h, xử lý như lệnh khác
                    print(Colors.error(f"❌ Lệnh không hợp lệ: {command}"))
                    print(Colors.info("💡 Nhập 'h' hoặc 'help' để xem hướng dẫn"))
            
            # Chạy tool theo số
            elif command.isdigit():
                idx = int(command)
                
                if 1 <= idx <= len(tools):
                    tool = tools[idx - 1]
                    # Chạy tool với vòng lặp riêng - quay lại đầu tool khi kết thúc
                    _run_tool_loop(manager, tool, tools)
                else:
                    print(Colors.error("❌ Số không hợp lệ"))
            
            else:
                print(Colors.error(f"❌ Lệnh không hợp lệ: {command}"))
                
                # Gợi ý commands
                valid_commands = ['h', 'help', 'q', 'quit', 'l', 'list', 's', 'search', 'f', 'r', 'set', 'clear']
                suggestions = suggest_command(command, valid_commands)
                if suggestions:
                    print_command_suggestions(command, suggestions)
                else:
                    print(Colors.info("💡 Nhập 'h' hoặc 'help' để xem hướng dẫn"))
        
        except (EOFError, KeyboardInterrupt):
            # Xử lý EOF error (input stream bị đóng) hoặc Ctrl+C
            print()
            print(Colors.info("👋 Tạm biệt!"))
            sys.exit(0)
        
        except Exception as e:
            # Xử lý các lỗi khác
            try:
                print()
                print(Colors.error(f"❌ Lỗi: {e}"))
                import traceback
                traceback.print_exc()
            except Exception:
                # Nếu không print được do encoding, dùng ASCII
                print(f"\nLỗi: {str(e)}")


if __name__ == "__main__":
    main()
