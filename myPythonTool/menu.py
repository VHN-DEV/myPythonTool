import os
import subprocess

def main():
    # Đường dẫn đến thư mục tool (cùng cấp với file menu.py)
    tool_dir = os.path.join(os.path.dirname(__file__), "tool")

    # Lấy danh sách file .py trong thư mục tool
    py_files = [f for f in os.listdir(tool_dir) if f.endswith(".py")]

    if not py_files:
        print("Không tìm thấy file .py nào trong thư mục tool.")
        return

    # In ra danh sách lựa chọn
    print("===== Danh sách tool =====")
    for idx, file in enumerate(py_files, start=1):
        print(f"{idx}. {file}")
    print("0. Thoát")

    while True:
        try:
            choice = int(input("Chọn số để chạy tool: "))
            if choice == 0:
                print("Thoát chương trình.")
                break
            elif 1 <= choice <= len(py_files):
                file_to_run = py_files[choice - 1]
                file_path = os.path.join(tool_dir, file_to_run)

                print(f"\n>>> Đang chạy {file_to_run}...\n")
                subprocess.run(["python", file_path], check=True)
                print("\n>>> Tool đã chạy xong!\n")
            else:
                print("Lựa chọn không hợp lệ.")
        except ValueError:
            print("Vui lòng nhập số.")

if __name__ == "__main__":
    main()
