#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: Kết nối Git và push source code lên repository

Mục đích: Tự động hóa quá trình kết nối Git, commit và push code lên GitHub
Lý do: Tiết kiệm thời gian, tránh lỗi khi thao tác Git thủ công
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import Optional, Tuple

# Thêm thư mục cha vào sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils import (
    print_header, get_user_input, confirm_action,
    log_info, log_error, setup_logger, normalize_path
)
from utils.colors import Colors


class GitManager:
    """
    Class quản lý Git operations
    
    Mục đích: Tập trung logic Git, dễ mở rộng và maintain
    """
    
    def __init__(self, repo_url: str, local_path: str):
        """
        Khởi tạo GitManager
        
        Args:
            repo_url: URL repository (vd: https://github.com/VHN-DEV/laravel-botble-cms)
            local_path: Đường dẫn thư mục local
        """
        self.repo_url = repo_url
        self.local_path = Path(local_path).resolve()
        
        # Đảm bảo thư mục tồn tại
        if not self.local_path.exists():
            self.local_path.mkdir(parents=True, exist_ok=True)
    
    def check_git_installed(self) -> bool:
        """
        Kiểm tra Git đã được cài đặt chưa
        
        Returns:
            bool: True nếu Git đã cài đặt
        """
        try:
            result = subprocess.run(
                ["git", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            log_info(f"Git version: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            log_error("Git chưa được cài đặt hoặc không có trong PATH")
            return False
    
    def run_git_command(self, command: list, cwd: Optional[Path] = None) -> Tuple[bool, str]:
        """
        Chạy lệnh Git và trả về kết quả
        
        Args:
            command: Danh sách lệnh Git (vd: ["git", "status"])
            cwd: Thư mục làm việc (mặc định: self.local_path)
        
        Returns:
            tuple: (success, output)
        """
        if cwd is None:
            cwd = self.local_path
        
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8',
                cwd=str(cwd)
            )
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else str(e)
            return False, error_msg
        except Exception as e:
            return False, str(e)
    
    def is_git_repo(self) -> bool:
        """
        Kiểm tra thư mục có phải Git repository không
        
        Returns:
            bool: True nếu là Git repo
        """
        git_dir = self.local_path / ".git"
        return git_dir.exists() and git_dir.is_dir()
    
    def init_repo(self) -> bool:
        """
        Khởi tạo Git repository mới
        
        Returns:
            bool: True nếu thành công
        """
        print("📦 Đang khởi tạo Git repository...")
        success, output = self.run_git_command(["git", "init"])
        
        if success:
            log_info("Git repository đã được khởi tạo")
            print("✅ Đã khởi tạo Git repository")
            return True
        else:
            log_error(f"Lỗi khởi tạo repository: {output}")
            print(f"❌ Lỗi: {output}")
            return False
    
    def clone_repo(self) -> bool:
        """
        Clone repository từ remote
        
        Returns:
            bool: True nếu thành công
        """
        print(f"📥 Đang clone repository từ: {self.repo_url}")
        print(f"   Đến: {self.local_path}")
        
        success, output = self.run_git_command(
            ["git", "clone", self.repo_url, str(self.local_path)],
            cwd=self.local_path.parent
        )
        
        if success:
            log_info(f"Đã clone repository thành công")
            print("✅ Đã clone repository thành công")
            return True
        else:
            log_error(f"Lỗi clone repository: {output}")
            print(f"❌ Lỗi: {output}")
            return False
    
    def setup_remote(self, remote_name: str = "origin") -> bool:
        """
        Thiết lập remote repository
        
        Args:
            remote_name: Tên remote (mặc định: origin)
        
        Returns:
            bool: True nếu thành công
        """
        # Kiểm tra remote đã tồn tại chưa
        success, output = self.run_git_command(["git", "remote", "get-url", remote_name])
        if success:
            print(f"ℹ️  Remote '{remote_name}' đã tồn tại: {output}")
            # Cập nhật URL nếu khác
            if output != self.repo_url:
                if confirm_action(f"Remote URL khác với URL mới. Cập nhật?"):
                    success, output = self.run_git_command(
                        ["git", "remote", "set-url", remote_name, self.repo_url]
                    )
                    if success:
                        print(f"✅ Đã cập nhật remote URL")
                        return True
                    else:
                        print(f"❌ Lỗi cập nhật remote: {output}")
                        return False
            return True
        
        # Thêm remote mới
        print(f"🔗 Đang thêm remote '{remote_name}'...")
        success, output = self.run_git_command(
            ["git", "remote", "add", remote_name, self.repo_url]
        )
        
        if success:
            log_info(f"Đã thêm remote: {remote_name} -> {self.repo_url}")
            print(f"✅ Đã thêm remote '{remote_name}'")
            return True
        else:
            log_error(f"Lỗi thêm remote: {output}")
            print(f"❌ Lỗi: {output}")
            return False
    
    def get_status(self) -> Tuple[bool, str]:
        """
        Lấy trạng thái Git
        
        Returns:
            tuple: (success, status_output)
        """
        return self.run_git_command(["git", "status", "--short"])
    
    def add_files(self, pattern: str = ".") -> bool:
        """
        Thêm files vào staging area
        
        Args:
            pattern: Pattern files cần add (mặc định: "." = tất cả)
        
        Returns:
            bool: True nếu thành công
        """
        print(f"📝 Đang thêm files vào staging area...")
        success, output = self.run_git_command(["git", "add", pattern])
        
        if success:
            log_info(f"Đã thêm files: {pattern}")
            print("✅ Đã thêm files vào staging area")
            return True
        else:
            log_error(f"Lỗi thêm files: {output}")
            print(f"❌ Lỗi: {output}")
            return False
    
    def commit(self, message: str) -> bool:
        """
        Commit changes
        
        Args:
            message: Commit message
        
        Returns:
            bool: True nếu thành công
        """
        print(f"💾 Đang commit với message: {message}")
        success, output = self.run_git_command(
            ["git", "commit", "-m", message]
        )
        
        if success:
            log_info(f"Đã commit: {message}")
            print("✅ Đã commit thành công")
            return True
        else:
            log_error(f"Lỗi commit: {output}")
            print(f"❌ Lỗi: {output}")
            return False
    
    def push(self, branch: str = "main", remote: str = "origin", force: bool = False) -> bool:
        """
        Push code lên remote repository
        
        Args:
            branch: Tên branch (mặc định: main)
            remote: Tên remote (mặc định: origin)
            force: Có force push không
        
        Returns:
            bool: True nếu thành công
        """
        print(f"🚀 Đang push code lên {remote}/{branch}...")
        
        cmd = ["git", "push", remote, branch]
        if force:
            cmd.append("--force")
        
        success, output = self.run_git_command(cmd)
        
        if success:
            log_info(f"Đã push thành công lên {remote}/{branch}")
            print(f"✅ Đã push thành công lên {remote}/{branch}")
            return True
        else:
            log_error(f"Lỗi push: {output}")
            print(f"❌ Lỗi push: {output}")
            if "authentication" in output.lower() or "permission" in output.lower():
                print("\n💡 Gợi ý:")
                print("   - Kiểm tra quyền truy cập repository")
                print("   - Sử dụng Personal Access Token nếu cần")
                print("   - Kiểm tra SSH key nếu dùng SSH URL")
            return False
    
    def get_current_branch(self) -> Optional[str]:
        """
        Lấy tên branch hiện tại
        
        Returns:
            str: Tên branch hoặc None
        """
        success, output = self.run_git_command(["git", "branch", "--show-current"])
        if success and output:
            return output.strip()
        return None
    
    def create_branch(self, branch_name: str) -> bool:
        """
        Tạo branch mới
        
        Args:
            branch_name: Tên branch
        
        Returns:
            bool: True nếu thành công
        """
        print(f"🌿 Đang tạo branch: {branch_name}")
        success, output = self.run_git_command(["git", "checkout", "-b", branch_name])
        
        if success:
            log_info(f"Đã tạo branch: {branch_name}")
            print(f"✅ Đã tạo và chuyển sang branch: {branch_name}")
            return True
        else:
            log_error(f"Lỗi tạo branch: {output}")
            print(f"❌ Lỗi: {output}")
            return False


def main_interactive():
    """
    Chế độ interactive
    
    Giải thích:
    - Hỏi người dùng từng bước
    - Hiển thị menu lựa chọn
    """
    print_header("TOOL KẾT NỐI GIT VÀ PUSH SOURCE CODE")
    
    # Repository URL mặc định
    default_repo = "https://github.com/VHN-DEV/laravel-botble-cms"
    
    print(f"\n📋 Repository mặc định: {Colors.info(default_repo)}")
    use_default = get_user_input(
        f"Sử dụng repository mặc định? (y/n)",
        default="y"
    ).lower() == "y"
    
    if use_default:
        repo_url = default_repo
    else:
        repo_url = get_user_input("Nhập URL repository", default=default_repo)
    
    # Đường dẫn local
    print("\n💡 Mẹo: Bạn có thể kéo thả thư mục vào terminal để nhập đường dẫn")
    local_path_input = get_user_input(
        "Nhập đường dẫn thư mục local (Enter để dùng thư mục hiện tại)",
        default="."
    )
    local_path = normalize_path(local_path_input)
    
    # Khởi tạo GitManager
    git_manager = GitManager(repo_url, local_path)
    
    # Kiểm tra Git đã cài đặt
    if not git_manager.check_git_installed():
        print("❌ Git chưa được cài đặt!")
        print("   Vui lòng cài đặt Git từ: https://git-scm.com/downloads")
        return
    
    print(f"\n✅ Đã chọn:")
    print(f"   Repository: {repo_url}")
    print(f"   Local path: {local_path}\n")
    
    # Menu chính
    print("===== MENU CHÍNH =====")
    print("1. Clone repository (nếu chưa có)")
    print("2. Khởi tạo repository mới")
    print("3. Thiết lập remote")
    print("4. Xem trạng thái")
    print("5. Add files và commit")
    print("6. Push code lên remote")
    print("7. Tạo branch mới")
    print("8. Thực hiện đầy đủ (add + commit + push)")
    print("0. Thoát")
    
    choice = get_user_input("\nChọn chức năng (0-8)", default="8")
    
    if choice == "0":
        print("Thoát chương trình.")
        return
    
    # Xử lý các lựa chọn
    if choice == "1":
        # Clone repository
        if git_manager.local_path.exists() and any(git_manager.local_path.iterdir()):
            if not confirm_action("Thư mục không trống. Tiếp tục?"):
                return
        git_manager.clone_repo()
    
    elif choice == "2":
        # Khởi tạo repository
        if git_manager.is_git_repo():
            print("ℹ️  Thư mục đã là Git repository")
        else:
            git_manager.init_repo()
            git_manager.setup_remote()
    
    elif choice == "3":
        # Thiết lập remote
        if not git_manager.is_git_repo():
            print("❌ Thư mục chưa phải Git repository!")
            if confirm_action("Khởi tạo repository mới?"):
                git_manager.init_repo()
        git_manager.setup_remote()
    
    elif choice == "4":
        # Xem trạng thái
        if not git_manager.is_git_repo():
            print("❌ Thư mục chưa phải Git repository!")
            return
        
        success, status = git_manager.get_status()
        if success:
            print("\n📊 Trạng thái Git:")
            print(status if status else "Không có thay đổi")
            
            # Hiển thị branch hiện tại
            branch = git_manager.get_current_branch()
            if branch:
                print(f"\n🌿 Branch hiện tại: {Colors.info(branch)}")
        else:
            print(f"❌ Lỗi: {status}")
    
    elif choice == "5":
        # Add files và commit
        if not git_manager.is_git_repo():
            print("❌ Thư mục chưa phải Git repository!")
            return
        
        # Xem trạng thái trước
        success, status = git_manager.get_status()
        if success and status:
            print("\n📊 Files thay đổi:")
            print(status)
        else:
            print("ℹ️  Không có files thay đổi")
            return
        
        # Add files
        pattern = get_user_input(
            "Nhập pattern files cần add (Enter để add tất cả)",
            default="."
        )
        if git_manager.add_files(pattern):
            # Commit
            commit_msg = get_user_input(
                "Nhập commit message",
                default="Update source code"
            )
            git_manager.commit(commit_msg)
    
    elif choice == "6":
        # Push code
        if not git_manager.is_git_repo():
            print("❌ Thư mục chưa phải Git repository!")
            return
        
        branch = git_manager.get_current_branch()
        if not branch:
            branch = get_user_input("Nhập tên branch", default="main")
        else:
            use_current = get_user_input(
                f"Sử dụng branch hiện tại '{branch}'? (y/n)",
                default="y"
            ).lower() == "y"
            if not use_current:
                branch = get_user_input("Nhập tên branch", default=branch)
        
        force = confirm_action("Force push? (Cẩn thận!)", require_yes=True)
        git_manager.push(branch=branch, force=force)
    
    elif choice == "7":
        # Tạo branch mới
        if not git_manager.is_git_repo():
            print("❌ Thư mục chưa phải Git repository!")
            return
        
        branch_name = get_user_input("Nhập tên branch mới")
        if branch_name:
            git_manager.create_branch(branch_name)
    
    elif choice == "8":
        # Thực hiện đầy đủ
        if not git_manager.is_git_repo():
            print("ℹ️  Thư mục chưa phải Git repository, đang khởi tạo...")
            if not git_manager.init_repo():
                return
            if not git_manager.setup_remote():
                return
        
        # Xem trạng thái
        success, status = git_manager.get_status()
        if success and status:
            print("\n📊 Files thay đổi:")
            print(status)
            
            if confirm_action("Tiếp tục add, commit và push?"):
                # Add files
                pattern = get_user_input(
                    "Nhập pattern files cần add (Enter để add tất cả)",
                    default="."
                )
                if git_manager.add_files(pattern):
                    # Commit
                    commit_msg = get_user_input(
                        "Nhập commit message",
                        default="Update source code"
                    )
                    if git_manager.commit(commit_msg):
                        # Push
                        branch = git_manager.get_current_branch() or "main"
                        use_current = get_user_input(
                            f"Push lên branch '{branch}'? (y/n)",
                            default="y"
                        ).lower() == "y"
                        if not use_current:
                            branch = get_user_input("Nhập tên branch", default=branch)
                        
                        git_manager.push(branch=branch)
        else:
            print("ℹ️  Không có files thay đổi để commit")


def main_cli(args):
    """
    Chế độ CLI
    
    Args:
        args: Arguments từ argparse
    """
    git_manager = GitManager(args.repo, args.path)
    
    # Kiểm tra Git
    if not git_manager.check_git_installed():
        print("❌ Git chưa được cài đặt!")
        return 1
    
    # Khởi tạo/clone nếu cần
    if args.clone:
        if not git_manager.is_git_repo():
            if not git_manager.clone_repo():
                return 1
        else:
            print("ℹ️  Thư mục đã là Git repository")
    
    if args.init:
        if not git_manager.is_git_repo():
            if not git_manager.init_repo():
                return 1
            if not git_manager.setup_remote():
                return 1
        else:
            print("ℹ️  Thư mục đã là Git repository")
    
    # Setup remote
    if args.setup_remote:
        if not git_manager.is_git_repo():
            print("❌ Thư mục chưa phải Git repository!")
            return 1
        if not git_manager.setup_remote():
            return 1
    
    # Add files
    if args.add:
        if not git_manager.is_git_repo():
            print("❌ Thư mục chưa phải Git repository!")
            return 1
        if not git_manager.add_files(args.add):
            return 1
    
    # Commit
    if args.commit:
        if not git_manager.is_git_repo():
            print("❌ Thư mục chưa phải Git repository!")
            return 1
        if not git_manager.commit(args.commit):
            return 1
    
    # Push
    if args.push:
        if not git_manager.is_git_repo():
            print("❌ Thư mục chưa phải Git repository!")
            return 1
        branch = args.branch or git_manager.get_current_branch() or "main"
        if not git_manager.push(branch=branch, force=args.force):
            return 1
    
    # Status
    if args.status:
        if not git_manager.is_git_repo():
            print("❌ Thư mục chưa phải Git repository!")
            return 1
        success, status = git_manager.get_status()
        if success:
            print(status if status else "Không có thay đổi")
        else:
            print(f"❌ Lỗi: {status}")
            return 1
    
    return 0


def main():
    """Hàm main"""
    # Setup logger
    setup_logger('git-push-source', log_to_console=False)
    
    # Argument parser
    parser = argparse.ArgumentParser(
        description='Tool kết nối Git và push source code lên repository',
        epilog="""
Ví dụ:
  # Interactive mode
  python git-push-source.py
  
  # Clone repository
  python git-push-source.py --clone --repo https://github.com/user/repo --path ./project
  
  # Add, commit và push
  python git-push-source.py --add . --commit "Update code" --push --branch main
  
  # Xem trạng thái
  python git-push-source.py --status
        """
    )
    
    parser.add_argument('--repo', default='https://github.com/VHN-DEV/laravel-botble-cms',
                       help='URL repository (mặc định: https://github.com/VHN-DEV/laravel-botble-cms)')
    parser.add_argument('--path', default='.',
                       help='Đường dẫn thư mục local (mặc định: thư mục hiện tại)')
    parser.add_argument('--clone', action='store_true',
                       help='Clone repository')
    parser.add_argument('--init', action='store_true',
                       help='Khởi tạo Git repository mới')
    parser.add_argument('--setup-remote', action='store_true',
                       help='Thiết lập remote')
    parser.add_argument('--add', metavar='PATTERN',
                       help='Add files (pattern, mặc định: .)')
    parser.add_argument('--commit', metavar='MESSAGE',
                       help='Commit với message')
    parser.add_argument('--push', action='store_true',
                       help='Push code lên remote')
    parser.add_argument('--branch', default='main',
                       help='Tên branch (mặc định: main)')
    parser.add_argument('--force', action='store_true',
                       help='Force push')
    parser.add_argument('--status', action='store_true',
                       help='Xem trạng thái Git')
    
    args, unknown = parser.parse_known_args()
    
    if any([args.clone, args.init, args.setup_remote, args.add, args.commit, args.push, args.status]):
        sys.exit(main_cli(args))
    else:
        try:
            main_interactive()
        except KeyboardInterrupt:
            print("\n\n❌ Đã hủy!")
        except Exception as e:
            print(f"\n❌ Lỗi: {e}")
            log_error(f"Exception: {e}", exc_info=True)


if __name__ == "__main__":
    main()

