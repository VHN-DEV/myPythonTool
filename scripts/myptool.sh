#!/bin/bash
# ============================================================
# myPythonTool - Shell wrapper để chạy từ bất kỳ đâu
# ============================================================

# Mục đích: 
#   Cho phép chạy myPythonTool từ bất kỳ thư mục nào
#   mà không cần cài đặt bằng pip
#
# Cách sử dụng:
#   1. (Khuyến nghị) Đặt file này trong thư mục dự án: scripts/myptool.sh
#      Chạy: ./scripts/myptool.sh
#   2. (Tùy chọn) Tạo symlink hoặc thêm vào PATH:
#      - ln -s /path/to/my-python-tool/scripts/myptool.sh /usr/local/bin/myptool
#      - Hoặc thêm vào ~/.bashrc: export PATH="$PATH:/path/to/my-python-tool/scripts"
#
# Lưu ý:
#   - Script tự động phát hiện đường dẫn, không cần cấu hình
#   - Đảm bảo Python 3.7+ đã được cài đặt
# ============================================================

# ==================== TỰ ĐỘNG PHÁT HIỆN ĐƯỜNG DẪN ====================

# Hàm kiểm tra và chạy tool
run_tool() {
    # Kiểm tra TOOL_DIR
    if [ ! -f "$TOOL_DIR/__main__.py" ]; then
        echo ""
        echo "==============================================="
        echo "   ERROR: Thư mục không hợp lệ"
        echo "==============================================="
        echo ""
        echo "Đường dẫn: $TOOL_DIR"
        echo "Không tìm thấy file: __main__.py"
        echo ""
        exit 1
    fi

    # Chạy tool với encoding UTF-8
    if [ -n "$PYTHON_EXE" ]; then
        "$PYTHON_EXE" -X utf8 "$TOOL_DIR/__main__.py" "$@"
    else
        python3 -X utf8 "$TOOL_DIR/__main__.py" "$@"
    fi

    # Lưu exit code
    EXIT_CODE=$?

    # Nếu có lỗi, hiển thị thông báo
    if [ $EXIT_CODE -ne 0 ]; then
        echo ""
        echo "==============================================="
        echo "   Có lỗi xảy ra khi chạy myPythonTool"
        echo "==============================================="
        echo ""
        if [ $EXIT_CODE -eq 127 ]; then
            echo "Lỗi: Không tìm thấy Python"
            echo ""
            echo "Giải pháp:"
            echo "  1. Kiểm tra Python đã được cài đặt chưa: python3 --version"
            echo "  2. Cài đặt Python 3.7+: sudo apt-get install python3 (Ubuntu/Debian)"
            echo "  3. Hoặc: brew install python3 (macOS)"
            echo "  4. Hoặc chỉ định đường dẫn Python cụ thể trong PYTHON_EXE"
            echo ""
        fi
    fi

    exit $EXIT_CODE
}

# Ưu tiên 1: Kiểm tra biến môi trường MYPYTHONTOOL_DIR
if [ -n "$MYPYTHONTOOL_DIR" ] && [ -f "$MYPYTHONTOOL_DIR/__main__.py" ]; then
    TOOL_DIR="$MYPYTHONTOOL_DIR"
    run_tool "$@"
fi

# Ưu tiên 2: Nếu file .sh nằm trong project (scripts/myptool.sh)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
if [ -f "$PROJECT_ROOT/__main__.py" ]; then
    TOOL_DIR="$PROJECT_ROOT"
    run_tool "$@"
fi

# Ưu tiên 3: Tìm từ thư mục hiện tại lên trên
CURRENT_DIR="$(pwd)"
while [ "$CURRENT_DIR" != "/" ]; do
    if [ -f "$CURRENT_DIR/__main__.py" ]; then
        TOOL_DIR="$CURRENT_DIR"
        run_tool "$@"
    fi
    CURRENT_DIR="$(dirname "$CURRENT_DIR")"
done

# Ưu tiên 4: Thử tìm trong thư mục scripts (nếu file .sh được copy vào PATH)
BAT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_DIR="$(cd "$BAT_DIR/.." && pwd)"
if [ -f "$TEST_DIR/__main__.py" ]; then
    TOOL_DIR="$TEST_DIR"
    run_tool "$@"
fi

# Không tìm thấy
echo ""
echo "==============================================="
echo "   ERROR: Không tìm thấy thư mục myPythonTool"
echo "==============================================="
echo ""
echo "Giải pháp:"
echo ""
echo "   Cách 1: Set biến môi trường (khuyến nghị)"
echo "   ============================================"
echo "   export MYPYTHONTOOL_DIR=\"/path/to/my-python-tool\""
echo "   # Hoặc thêm vào ~/.bashrc hoặc ~/.zshrc:"
echo "   echo 'export MYPYTHONTOOL_DIR=\"/path/to/my-python-tool\"' >> ~/.bashrc"
echo "   source ~/.bashrc"
echo ""
echo "   Cách 2: Chạy trực tiếp từ thư mục project"
echo "   ============================================"
echo "   cd /path/to/my-python-tool"
echo "   python3 ."
echo ""
echo "   Cách 3: Cài đặt bằng pip (khuyến nghị nhất)"
echo "   ============================================"
echo "   cd /path/to/my-python-tool"
echo "   pip3 install -e ."
echo "   # Sau đó chạy: myptool (từ bất kỳ đâu)"
echo ""
echo "   Cách 4: Đặt file .sh trong thư mục scripts"
echo "   ============================================"
echo "   Copy myptool.sh vào: scripts/myptool.sh"
echo "   Chạy: ./scripts/myptool.sh"
echo ""
exit 1

