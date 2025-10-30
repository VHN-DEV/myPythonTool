@echo off
REM ============================================================
REM myPythonTool - Batch wrapper để chạy từ bất kỳ đâu
REM ============================================================
REM 
REM Mục đích: 
REM   Cho phép chạy myPythonTool từ bất kỳ thư mục nào
REM   mà không cần cài đặt bằng pip
REM
REM Cách sử dụng:
REM   1. Copy file này vào thư mục đã có trong PATH
REM      (ví dụ: C:\Windows\System32\ hoặc C:\Program Files\Git\cmd\)
REM   2. Sửa đường dẫn TOOL_DIR bên dưới cho đúng
REM   3. Mở cmd mới và gõ: myptool
REM
REM Lưu ý:
REM   - Thay đổi đường dẫn TOOL_DIR phù hợp với máy bạn
REM   - Đảm bảo Python đã được thêm vào PATH
REM ============================================================

REM ==================== CẤU HÌNH ====================
REM Đường dẫn đến thư mục myPythonTool
REM Thay đổi đường dẫn này cho phù hợp với máy bạn
set "TOOL_DIR=D:\myPythonTool"

REM Tùy chọn: Chỉ định Python executable cụ thể
REM Bỏ comment và chỉnh sửa nếu cần
REM set "PYTHON_EXE=C:\Python310\python.exe"
REM ===================================================

REM Kiểm tra TOOL_DIR có tồn tại không
if not exist "%TOOL_DIR%" (
    echo.
    echo ===============================================
    echo   ERROR: Khong tim thay thu muc myPythonTool
    echo ===============================================
    echo.
    echo Thu muc hien tai: %TOOL_DIR%
    echo.
    echo Giai phap:
    echo   1. Kiem tra duong dan TOOL_DIR trong file myptool.bat
    echo   2. Sua lai cho dung voi vi tri cua myPythonTool tren may ban
    echo.
    echo Vi du:
    echo   set "TOOL_DIR=C:\Users\YourName\myPythonTool"
    echo.
    pause
    exit /b 1
)

REM Chạy tool
if defined PYTHON_EXE (
    "%PYTHON_EXE%" "%TOOL_DIR%" %*
) else (
    python "%TOOL_DIR%" %*
)

REM Lưu exit code
set EXIT_CODE=%ERRORLEVEL%

REM Nếu có lỗi, hiển thị thông báo
if %EXIT_CODE% neq 0 (
    echo.
    echo ===============================================
    echo   Co loi xay ra khi chay myPythonTool
    echo ===============================================
    echo.
    if %EXIT_CODE%==9009 (
        echo Loi: Khong tim thay Python
        echo.
        echo Giai phap:
        echo   1. Kiem tra Python da duoc cai dat chua: python --version
        echo   2. Them Python vao PATH
        echo   3. Hoac chi dinh duong dan Python cu the trong PYTHON_EXE
        echo.
    )
    pause
)

exit /b %EXIT_CODE%

