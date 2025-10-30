#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__main__.py - Entry point cho myPythonTool

Mục đích: Cho phép chạy tool bằng lệnh "python ." hoặc "python myPythonTool/"

Cách dùng:
    python .                # Từ trong thư mục
    python myPythonTool     # Từ bên ngoài
"""

import sys
import os

# Fix Windows console encoding - Simple way
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Đảm bảo thư mục hiện tại trong sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import và chạy menu
if __name__ == "__main__":
    try:
        # Import menu module từ menu package
        from menu import main
        
        # Chạy menu
        main()
    
    except KeyboardInterrupt:
        print("\n\n👋 Tạm biệt!")
    
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

