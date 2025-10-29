#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: Copy các file đã thay đổi từ commit cụ thể đến commit mới nhất
Mục đích: Tạo thư mục chứa các file thay đổi theo đúng cấu trúc để upload lên server
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def print_header():
    """In header của script"""
    print("=" * 50)
    print("  SCRIPT COPY FILE THAY DOI THEO COMMIT")
    print("=" * 50)
    print()


def get_project_path():
    """
    Hỏi người dùng nhập đường dẫn dự án

    Returns:
        Path: Đường dẫn đến thư mục dự án

    Giải thích:
    - Nhận đường dẫn từ người dùng
    - Kiểm tra đường dẫn có tồn tại không
    - Kiểm tra có phải là Git repository không
    - Trả về Path object nếu hợp lệ
    """
    project_path_input = input("Nhap duong dan du an (vi du: C:\\xampp\\htdocs\\mitsuheavy-ecommerce): ").strip()

    if not project_path_input:
        print("❌ Loi: Ban phai nhap duong dan du an!")
        sys.exit(1)

    # Chuyển đổi sang Path object
    project_path = Path(project_path_input).resolve()

    # Kiểm tra đường dẫn có tồn tại không
    if not project_path.exists():
        print(f"❌ Loi: Duong dan '{project_path}' khong ton tai!")
        sys.exit(1)

    # Kiểm tra có phải là thư mục không
    if not project_path.is_dir():
        print(f"❌ Loi: '{project_path}' khong phai la thu muc!")
        sys.exit(1)

    # Kiểm tra có phải là Git repository không
    git_dir = project_path / ".git"
    if not git_dir.exists():
        print(f"❌ Loi: '{project_path}' khong phai la Git repository!")
        print("💡 Dam bao thu muc da duoc khoi tao Git: git init")
        sys.exit(1)

    print(f"✓ Du an hop le: {project_path}")
    print()
    return project_path


def get_user_input():
    """
    Bước 1: Hỏi người dùng nhập commit ID

    Returns:
        tuple: (commit_start, commit_end)

    Giải thích:
    - Nhận input từ người dùng về commit bắt đầu (bắt buộc)
    - Nhận input commit kết thúc (mặc định là HEAD)
    """
    # Nhập commit bắt đầu
    commit_start = input("Nhap commit ID bat dau (vi du: 9d172f6): ").strip()
    if not commit_start:
        print("❌ Loi: Ban phai nhap commit ID bat dau!")
        sys.exit(1)

    # Nhập commit kết thúc
    commit_end_input = input("Nhap commit ID ket thuc (Enter de chon HEAD - commit moi nhat): ").strip()
    if not commit_end_input:
        commit_end = "HEAD"
        print("✓ Su dung commit ket thuc: HEAD (commit moi nhat)")
    else:
        commit_end = commit_end_input

    print()
    return commit_start, commit_end


def run_git_command(command, cwd=None):
    """
    Chạy lệnh git và trả về kết quả

    Args:
        command (list): Danh sách lệnh git
        cwd (Path): Thư mục làm việc (working directory)

    Returns:
        tuple: (success, output)

    Giải thích:
    - Chạy lệnh git bằng subprocess trong thư mục cwd
    - Bắt lỗi nếu lệnh thất bại
    - Trả về True/False và output
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8',
            cwd=cwd
        )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()


def verify_commit(commit_id, project_path):
    """
    Bước 2: Kiểm tra commit ID có tồn tại không

    Args:
        commit_id (str): Commit ID cần kiểm tra
        project_path (Path): Đường dẫn đến dự án

    Returns:
        bool: True nếu commit hợp lệ, False nếu không

    Giải thích:
    - Sử dụng git rev-parse để verify commit
    - Chạy lệnh trong thư mục project_path
    - Nếu commit không tồn tại, git sẽ trả về lỗi
    """
    success, _ = run_git_command(['git', 'rev-parse', '--verify', commit_id], cwd=project_path)
    return success


def get_changed_files(commit_start, commit_end, project_path):
    """
    Bước 3: Lấy danh sách các file đã thay đổi

    Args:
        commit_start (str): Commit bắt đầu
        commit_end (str): Commit kết thúc
        project_path (Path): Đường dẫn đến dự án

    Returns:
        list: Danh sách file đã thay đổi

    Giải thích:
    - Sử dụng git diff --name-only để lấy tên file
    - --diff-filter=d để loại bỏ file đã xóa
    - Chạy lệnh trong thư mục project_path
    - Trả về danh sách file dạng list
    """
    success, output = run_git_command([
        'git', 'diff', '--name-only', '--diff-filter=d',
        f'{commit_start}..{commit_end}'
    ], cwd=project_path)

    if not success:
        print(f"❌ Loi khi lay danh sach file: {output}")
        sys.exit(1)

    if not output:
        return []

    return output.split('\n')


def create_export_folder(folder_name):
    """
    Bước 4: Tạo thư mục export

    Args:
        folder_name (str): Tên thư mục export

    Giải thích:
    - Xóa thư mục cũ nếu tồn tại
    - Tạo thư mục mới
    """
    export_path = Path(folder_name)

    # Xóa thư mục cũ
    if export_path.exists():
        print(f"🗑️  Dang xoa thu muc cu...")
        shutil.rmtree(export_path)

    # Tạo thư mục mới
    export_path.mkdir(parents=True, exist_ok=True)
    print(f"✓ Tao thu muc: {folder_name}\n")


def copy_files(changed_files, output_folder, project_path):
    """
    Bước 5: Copy từng file vào thư mục đích với cấu trúc giống gốc

    Args:
        changed_files (list): Danh sách file cần copy
        output_folder (str): Thư mục đích
        project_path (Path): Đường dẫn đến dự án

    Returns:
        tuple: (copied_count, skipped_count)

    Giải thích:
    - Duyệt qua từng file trong danh sách
    - File gốc nằm trong project_path
    - Tạo thư mục cha nếu chưa có
    - Copy file giữ nguyên cấu trúc thư mục
    - Đếm số file đã copy và bỏ qua
    """
    copied_count = 0
    skipped_count = 0

    for file_path in changed_files:
        # Đường dẫn file gốc (trong thư mục dự án)
        source_path = project_path / file_path

        # Đường dẫn file đích (giữ nguyên cấu trúc)
        destination_path = Path(output_folder) / file_path

        # Kiểm tra file có tồn tại không
        if source_path.exists():
            # Tạo thư mục cha nếu chưa có
            destination_path.parent.mkdir(parents=True, exist_ok=True)

            # Copy file
            shutil.copy2(source_path, destination_path)
            print(f"✓ [OK] {file_path}")
            copied_count += 1
        else:
            print(f"⚠️  [SKIP] {file_path} (file khong ton tai)")
            skipped_count += 1

    return copied_count, skipped_count


def save_file_list(changed_files, output_folder):
    """
    Bước 6: Xuất danh sách file đã copy ra file text

    Args:
        changed_files (list): Danh sách file đã thay đổi
        output_folder (str): Thư mục đích

    Giải thích:
    - Tạo file text chứa danh sách tất cả file đã copy
    - Giúp người dùng kiểm tra và đối chiếu
    """
    list_file = Path(output_folder) / "danh-sach-file-thay-doi.txt"
    with open(list_file, 'w', encoding='utf-8') as f:
        for file_path in changed_files:
            f.write(f"{file_path}\n")

    return str(list_file)


def print_summary(copied_count, skipped_count, output_folder, list_file):
    """
    Bước 7: In thông tin tổng kết

    Args:
        copied_count (int): Số file đã copy
        skipped_count (int): Số file đã bỏ qua
        output_folder (str): Thư mục export
        list_file (str): Đường dẫn file danh sách

    Giải thích:
    - Hiển thị thông tin tổng kết cho người dùng
    - Hướng dẫn cách upload lên server
    """
    print("\n" + "=" * 50)
    print("✓ Hoan tat!")
    print(f"- Da copy: {copied_count} file")
    print(f"- Bo qua: {skipped_count} file")
    print(f"- Thu muc xuat: {output_folder}")
    print(f"- Danh sach file: {list_file}")
    print("\n🚀 Ban co the upload toan bo thu muc '{}' len server bang FileZilla!".format(output_folder))
    print("=" * 50)
    print()


def main():
    """
    Hàm chính của script

    Giải thích:
    - Điều phối tất cả các bước của script
    - Hỏi đường dẫn dự án, commit ID
    - Xử lý lỗi và thoát khi cần thiết
    - Tạo thư mục export ở vị trí chạy script (không phải trong dự án)
    """
    # Bước 1: In header và lấy đường dẫn dự án
    print_header()
    project_path = get_project_path()

    # Bước 2: Lấy commit ID từ người dùng
    commit_start, commit_end = get_user_input()

    # Bước 3: Kiểm tra commit ID hợp lệ
    print("🔍 Kiem tra commit ID...")
    if not verify_commit(commit_start, project_path):
        print(f"❌ Loi: Commit ID bat dau '{commit_start}' khong ton tai!")
        print("💡 Ban co the xem danh sach commit bang lenh: git log --oneline -20")
        sys.exit(1)

    if commit_end != "HEAD":
        if not verify_commit(commit_end, project_path):
            print(f"❌ Loi: Commit ID ket thuc '{commit_end}' khong ton tai!")
            print("💡 Ban co the xem danh sach commit bang lenh: git log --oneline -20")
            sys.exit(1)

    print("✓ Commit ID hop le!\n")

    # Bước 4: Lấy danh sách file thay đổi
    print(f"📂 Dang lay danh sach file thay doi tu commit {commit_start} den {commit_end}...")
    changed_files = get_changed_files(commit_start, commit_end, project_path)

    if not changed_files:
        print("❌ Khong co file nao thay doi!")
        sys.exit(0)

    print(f"✓ Tim thay {len(changed_files)} file da thay doi\n")

    # Bước 5: Tạo thư mục export (ở vị trí hiện tại, không phải trong dự án)
    output_folder = "changed-files-export"
    create_export_folder(output_folder)

    # Bước 6: Copy files
    print("📋 Dang copy file...\n")
    copied_count, skipped_count = copy_files(changed_files, output_folder, project_path)

    # Bước 7: Lưu danh sách file
    list_file = save_file_list(changed_files, output_folder)

    # Bước 8: In tổng kết
    print_summary(copied_count, skipped_count, output_folder, list_file)


# Chạy script
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Script da bi huy boi nguoi dung!")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Loi: {e}")
        sys.exit(1)

