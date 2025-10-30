#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: Backup thư mục với timestamp và tính năng nâng cao

Mục đích: Sao lưu dữ liệu quan trọng
Lý do: Bảo vệ dữ liệu khỏi mất mát
"""

import os
import sys
import shutil
import datetime
import json
import argparse
from pathlib import Path
from typing import List, Optional, Tuple

# Thêm thư mục cha vào sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    print_header, format_size, get_user_input, confirm_action,
    get_folder_size, ensure_directory_exists, ProgressBar,
    log_info, log_error, setup_logger
)


class BackupManager:
    """
    Class quản lý backup
    
    Mục đích: Tập trung logic backup, dễ mở rộng và maintain
    """
    
    def __init__(self, source_folder: str, backup_location: str):
        """
        Khởi tạo BackupManager
        
        Args:
            source_folder: Thư mục nguồn cần backup
            backup_location: Vị trí lưu backup
        """
        self.source_path = Path(source_folder).resolve()
        self.backup_location = Path(backup_location).resolve()
        self.metadata_file = self.backup_location / "backup_metadata.json"
        
        # Đảm bảo thư mục backup tồn tại
        ensure_directory_exists(str(self.backup_location))
    
    def get_backup_metadata(self) -> dict:
        """
        Đọc metadata của các backup trước
        
        Returns:
            dict: Metadata của các backup
        
        Giải thích:
        - Lưu thông tin các lần backup (timestamp, size, file count...)
        - Hỗ trợ incremental backup trong tương lai
        """
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {'backups': []}
        return {'backups': []}
    
    def save_backup_metadata(self, backup_info: dict):
        """
        Lưu metadata của backup mới
        
        Args:
            backup_info: Thông tin backup (timestamp, size, path...)
        
        Giải thích:
        - Append backup info vào metadata file
        - Giúp tracking lịch sử backup
        """
        metadata = self.get_backup_metadata()
        metadata['backups'].append(backup_info)
        
        # Giữ tối đa 50 records gần nhất
        if len(metadata['backups']) > 50:
            metadata['backups'] = metadata['backups'][-50:]
        
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    def list_previous_backups(self) -> List[dict]:
        """
        Liệt kê các backup trước
        
        Returns:
            list: Danh sách backup info
        """
        metadata = self.get_backup_metadata()
        return metadata.get('backups', [])
    
    def create_backup(
        self,
        compression_format: str = 'zip',
        exclude_patterns: Optional[List[str]] = None,
        show_progress: bool = True
    ) -> Tuple[bool, str, dict]:
        """
        Tạo backup thư mục
        
        Args:
            compression_format: Định dạng nén (zip, tar, gztar, bztar, xztar)
            exclude_patterns: Danh sách pattern cần loại trừ
            show_progress: Hiển thị progress bar
        
        Returns:
            tuple: (success, backup_file_path, backup_info)
        
        Giải thích:
        - Tính dung lượng thư mục nguồn
        - Copy file với exclude patterns
        - Nén thành archive
        - Lưu metadata
        """
        try:
            # Kiểm tra thư mục nguồn
            if not self.source_path.exists():
                return False, "", {"error": "Thư mục nguồn không tồn tại"}
            
            # Tạo tên backup
            folder_name = self.source_path.name
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{folder_name}_backup_{timestamp}"
            
            log_info(f"Bắt đầu backup: {self.source_path}")
            
            # Tính dung lượng (với progress)
            print(f"📊 Đang tính dung lượng...")
            total_size = get_folder_size(str(self.source_path))
            print(f"   Dung lượng: {format_size(total_size)}")
            log_info(f"Dung lượng nguồn: {format_size(total_size)}")
            
            # Nếu có exclude patterns
            if exclude_patterns:
                print(f"\n📦 Đang copy và loại trừ...")
                backup_file = self._backup_with_exclude(
                    backup_name, exclude_patterns, compression_format, show_progress
                )
            else:
                print(f"\n📦 Đang nén...")
                backup_file = self._backup_full(
                    backup_name, compression_format, show_progress
                )
            
            if not backup_file:
                return False, "", {"error": "Lỗi khi tạo backup"}
            
            # Lấy thông tin backup
            backup_size = os.path.getsize(backup_file)
            compression_ratio = (backup_size / total_size * 100) if total_size > 0 else 0
            
            # Tạo backup info
            backup_info = {
                'timestamp': timestamp,
                'source_path': str(self.source_path),
                'backup_file': os.path.basename(backup_file),
                'original_size': total_size,
                'compressed_size': backup_size,
                'compression_ratio': compression_ratio,
                'format': compression_format,
                'excluded_patterns': exclude_patterns or []
            }
            
            # Lưu metadata
            self.save_backup_metadata(backup_info)
            
            # Hiển thị kết quả
            print(f"\n✅ Backup thành công!")
            print(f"   📁 Thư mục nguồn: {self.source_path}")
            print(f"   💾 File backup: {backup_file}")
            print(f"   📊 Kích thước gốc: {format_size(total_size)}")
            print(f"   📊 Kích thước nén: {format_size(backup_size)}")
            print(f"   💯 Tỷ lệ nén: {compression_ratio:.1f}%")
            
            log_info(f"Backup thành công: {backup_file}")
            
            return True, backup_file, backup_info
            
        except Exception as e:
            error_msg = f"Lỗi khi backup: {e}"
            print(f"❌ {error_msg}")
            log_error(error_msg, exc_info=True)
            return False, "", {"error": str(e)}
    
    def _backup_full(
        self,
        backup_name: str,
        compression_format: str,
        show_progress: bool
    ) -> Optional[str]:
        """
        Backup toàn bộ không có exclude
        
        Args:
            backup_name: Tên backup
            compression_format: Format nén
            show_progress: Hiển thị progress
        
        Returns:
            str: Đường dẫn file backup
        
        Giải thích:
        - Sử dụng shutil.make_archive cho backup nhanh
        - Không cần copy trung gian
        """
        backup_file_base = self.backup_location / backup_name
        
        try:
            backup_file = shutil.make_archive(
                str(backup_file_base),
                compression_format,
                self.source_path.parent,
                self.source_path.name
            )
            return backup_file
        except Exception as e:
            log_error(f"Lỗi khi nén: {e}")
            return None
    
    def _backup_with_exclude(
        self,
        backup_name: str,
        exclude_patterns: List[str],
        compression_format: str,
        show_progress: bool
    ) -> Optional[str]:
        """
        Backup với exclude patterns
        
        Args:
            backup_name: Tên backup
            exclude_patterns: Danh sách patterns cần loại trừ
            compression_format: Format nén
            show_progress: Hiển thị progress
        
        Returns:
            str: Đường dẫn file backup
        
        Giải thích:
        - Copy file vào thư mục tạm với ignore patterns
        - Nén thư mục tạm
        - Xóa thư mục tạm
        """
        temp_folder = self.backup_location / f"temp_{backup_name}"
        
        try:
            # Hàm ignore patterns
            def ignore_patterns(directory, contents):
                ignored = set()
                for pattern in exclude_patterns:
                    for item in contents:
                        # Khớp pattern trong tên file/folder
                        if pattern.lower() in item.lower():
                            ignored.add(item)
                return ignored
            
            # Copy với progress
            if show_progress:
                # Đếm số file để hiển thị progress
                total_files = sum(1 for _ in self.source_path.rglob('*') if _.is_file())
                progress = ProgressBar(total_files, prefix="Copy file:")
                
                # Custom copytree với callback
                self._copytree_with_progress(
                    self.source_path,
                    temp_folder,
                    ignore=ignore_patterns,
                    progress=progress
                )
                progress.finish("Copy hoàn thành")
            else:
                shutil.copytree(self.source_path, temp_folder, ignore=ignore_patterns)
            
            # Nén thư mục tạm
            backup_file = shutil.make_archive(
                str(self.backup_location / backup_name),
                compression_format,
                temp_folder.parent,
                temp_folder.name
            )
            
            # Xóa thư mục tạm
            shutil.rmtree(temp_folder)
            
            return backup_file
            
        except Exception as e:
            # Cleanup thư mục tạm nếu lỗi
            if temp_folder.exists():
                try:
                    shutil.rmtree(temp_folder)
                except Exception:
                    pass
            
            log_error(f"Lỗi khi backup với exclude: {e}")
            return None
    
    def _copytree_with_progress(
        self,
        src: Path,
        dst: Path,
        ignore=None,
        progress: Optional[ProgressBar] = None
    ):
        """
        Copy tree với progress tracking
        
        Args:
            src: Source path
            dst: Destination path
            ignore: Ignore function
            progress: Progress bar instance
        
        Giải thích:
        - Custom implementation của copytree
        - Cập nhật progress sau mỗi file copy
        """
        dst.mkdir(parents=True, exist_ok=True)
        
        for item in src.iterdir():
            s = src / item.name
            d = dst / item.name
            
            # Check ignore
            if ignore:
                ignored = ignore(str(src), [item.name])
                if item.name in ignored:
                    continue
            
            if s.is_dir():
                self._copytree_with_progress(s, d, ignore, progress)
            else:
                shutil.copy2(str(s), str(d))
                if progress:
                    progress.update()
    
    def restore_backup(self, backup_file: str, restore_location: str) -> bool:
        """
        Khôi phục từ backup
        
        Args:
            backup_file: File backup cần restore
            restore_location: Vị trí restore
        
        Returns:
            bool: Thành công hay không
        
        Giải thích:
        - Giải nén backup vào vị trí chỉ định
        - Hỗ trợ restore từ các backup cũ
        """
        try:
            print(f"📦 Đang giải nén...")
            shutil.unpack_archive(backup_file, restore_location)
            print(f"✅ Restore thành công vào: {restore_location}")
            log_info(f"Restore thành công: {backup_file} -> {restore_location}")
            return True
        except Exception as e:
            print(f"❌ Lỗi khi restore: {e}")
            log_error(f"Lỗi restore: {e}", exc_info=True)
            return False


def main_interactive():
    """
    Chế độ interactive
    
    Giải thích:
    - Hỏi người dùng từng bước
    - Hiển thị menu lựa chọn
    """
    print_header("TOOL BACKUP THƯ MỤC")
    
    # Menu chính
    print("===== MENU CHÍNH =====")
    print("1. Tạo backup mới")
    print("2. Xem lịch sử backup")
    print("3. Restore từ backup")
    print("0. Thoát")
    
    choice = get_user_input("\nChọn chức năng (0-3)", default="1")
    
    if choice == "0":
        print("Thoát chương trình.")
        return
    
    # Nhập thư mục nguồn
    source_input = get_user_input("Nhập đường dẫn thư mục cần backup")
    if not source_input or not os.path.isdir(source_input):
        print("❌ Thư mục không tồn tại!")
        return
    
    # Nhập vị trí backup
    backup_input = get_user_input(
        "Nhập vị trí lưu backup (Enter để lưu tại thư mục hiện tại)",
        default="."
    )
    
    # Khởi tạo BackupManager
    manager = BackupManager(source_input, backup_input)
    
    if choice == "1":
        # Tạo backup mới
        print("\n===== CHẾ ĐỘ BACKUP =====")
        print("1. Backup toàn bộ")
        print("2. Backup có loại trừ (exclude)")
        
        mode = get_user_input("Chọn chế độ (1-2)", default="1")
        
        # Chọn định dạng nén
        print("\n===== ĐỊNH DẠNG NÉN =====")
        print("1. ZIP (phổ biến, nhanh)")
        print("2. TAR")
        print("3. TAR.GZ (nén cao hơn)")
        print("4. TAR.BZ2 (nén cao nhất, chậm hơn)")
        
        format_choice = get_user_input("Chọn định dạng (1-4, Enter để mặc định ZIP)", default="1")
        
        format_map = {
            "1": "zip",
            "2": "tar",
            "3": "gztar",
            "4": "bztar"
        }
        
        compression = format_map.get(format_choice, "zip")
        
        # Exclude patterns
        exclude_patterns = None
        if mode == "2":
            exclude_input = get_user_input(
                "\nNhập các pattern cần loại trừ (cách nhau bởi dấu phẩy, vd: node_modules,.git,__pycache__)",
                default="node_modules,.git,__pycache__,.vscode,.idea,venv,env,dist,build"
            )
            exclude_patterns = [p.strip() for p in exclude_input.split(',') if p.strip()]
            
            if exclude_patterns:
                print(f"\n🚫 Loại trừ: {', '.join(exclude_patterns)}")
        
        # Xác nhận
        if not confirm_action("Bắt đầu backup?"):
            print("❌ Đã hủy")
            return
        
        # Thực hiện backup
        print(f"\n🚀 Bắt đầu backup...\n")
        success, backup_file, info = manager.create_backup(
            compression_format=compression,
            exclude_patterns=exclude_patterns,
            show_progress=True
        )
        
        if success:
            print(f"\n🎉 Backup đã được lưu tại: {backup_file}")
    
    elif choice == "2":
        # Xem lịch sử backup
        print("\n===== LỊCH SỬ BACKUP =====")
        backups = manager.list_previous_backups()
        
        if not backups:
            print("Chưa có backup nào.")
            return
        
        for idx, backup in enumerate(backups[-10:], 1):  # 10 backup gần nhất
            print(f"\n{idx}. {backup['timestamp']}")
            print(f"   File: {backup['backup_file']}")
            print(f"   Kích thước: {format_size(backup['compressed_size'])}")
            print(f"   Tỷ lệ nén: {backup['compression_ratio']:.1f}%")
            if backup.get('excluded_patterns'):
                print(f"   Loại trừ: {', '.join(backup['excluded_patterns'])}")
    
    elif choice == "3":
        # Restore từ backup
        print("\n===== RESTORE TỪ BACKUP =====")
        
        backup_file = get_user_input("Nhập đường dẫn file backup")
        if not os.path.isfile(backup_file):
            print("❌ File backup không tồn tại!")
            return
        
        restore_location = get_user_input("Nhập vị trí restore", default="./restored")
        
        if not confirm_action("Bắt đầu restore?", require_yes=True):
            print("❌ Đã hủy")
            return
        
        manager.restore_backup(backup_file, restore_location)


def main_cli(args):
    """
    Chế độ CLI
    
    Args:
        args: Arguments từ argparse
    """
    manager = BackupManager(args.source, args.output)
    
    exclude_patterns = None
    if args.exclude:
        exclude_patterns = [p.strip() for p in args.exclude.split(',')]
    
    success, backup_file, info = manager.create_backup(
        compression_format=args.format,
        exclude_patterns=exclude_patterns,
        show_progress=not args.quiet
    )
    
    if success:
        print(f"✅ Backup: {backup_file}")
        return 0
    else:
        print(f"❌ Lỗi: {info.get('error', 'Unknown')}")
        return 1


def main():
    """Hàm main"""
    # Setup logger
    setup_logger('backup-folder', log_to_console=False)
    
    # Argument parser
    parser = argparse.ArgumentParser(
        description='Tool backup thư mục với nén',
        epilog="""
Ví dụ:
  # Interactive mode
  python backup-folder.py
  
  # Backup với ZIP
  python backup-folder.py -s ./project -o ./backups
  
  # Backup với exclude
  python backup-folder.py -s ./project -o ./backups -e "node_modules,.git,__pycache__"
  
  # Backup với TAR.GZ
  python backup-folder.py -s ./project -o ./backups -f gztar
        """
    )
    
    parser.add_argument('-s', '--source', help='Thư mục nguồn')
    parser.add_argument('-o', '--output', help='Thư mục đầu ra')
    parser.add_argument('-f', '--format', default='zip',
                       choices=['zip', 'tar', 'gztar', 'bztar', 'xztar'],
                       help='Định dạng nén (mặc định: zip)')
    parser.add_argument('-e', '--exclude', help='Patterns loại trừ (phân cách bởi dấu phẩy)')
    parser.add_argument('-q', '--quiet', action='store_true', help='Không hiển thị progress')
    
    args, unknown = parser.parse_known_args()
    
    if args.source:
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
