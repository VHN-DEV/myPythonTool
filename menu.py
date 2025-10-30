import os
import subprocess

def hien_thi_menu(py_files, ten_hien_thi):
    """
    Mục đích: Hiển thị danh sách các tool có sẵn
    Lý do: Tách thành function riêng để có thể gọi lại sau khi chạy xong tool
    """
    print("\n===== Danh sách tool =====")
    print("0. Thoát")
    for idx, file in enumerate(py_files, start=1):
        # Hiển thị tên tiếng Việt nếu có, không thì hiển thị tên file gốc
        ten_tool = ten_hien_thi.get(file, file)
        print(f"{idx}. {ten_tool}")
    print("="*27)

def main():
    # Đường dẫn đến thư mục tool (cùng cấp với file menu.py)
    tool_dir = os.path.join(os.path.dirname(__file__), "tool")

    # Bước 1: Khởi tạo dictionary ánh xạ tên file sang tên hiển thị tiếng Việt
    # Mục đích: Giúp người dùng dễ hiểu chức năng của từng tool
    # Lý do: Tên file tiếng Anh khó hiểu, cần tên tiếng Việt mô tả rõ chức năng
    ten_hien_thi = {
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
        "text-encoding-converter.py": "Chuyển đổi encoding file text (UTF-8, ANSI...)"
    }

    # Bước 2: Lấy danh sách file .py trong thư mục tool
    py_files = [f for f in os.listdir(tool_dir) if f.endswith(".py")]

    if not py_files:
        print("Không tìm thấy file .py nào trong thư mục tool.")
        return

    # Bước 3: Hiển thị menu lần đầu tiên
    hien_thi_menu(py_files, ten_hien_thi)

    # Bước 4: Vòng lặp xử lý lựa chọn của người dùng
    while True:
        try:
            choice = int(input("\nChọn số để chạy tool: "))
            if choice == 0:
                print("Thoát chương trình.")
                break
            elif 1 <= choice <= len(py_files):
                file_to_run = py_files[choice - 1]
                file_path = os.path.join(tool_dir, file_to_run)

                print(f"\n>>> Đang chạy {file_to_run}...\n")
                subprocess.run(["python", file_path], check=True)
                print("\n>>> Tool đã chạy xong!\n")
                
                # Hiển thị lại menu sau khi chạy xong tool
                # Mục đích: Giúp người dùng dễ dàng chọn tiếp tool khác mà không cần cuộn lên
                hien_thi_menu(py_files, ten_hien_thi)
            else:
                print("Lựa chọn không hợp lệ.")
        except ValueError:
            print("Vui lòng nhập số.")

if __name__ == "__main__":
    main()
