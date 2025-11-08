#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: Quản lý Database MySQL (Bản beta)
Mục đích: Quản lý Database MySQL (Bản beta), backup/restore, chạy SQL queries, export/import
"""

import os
import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass


def print_header():
    """In header của tool"""
    print("=" * 70)
    print("  TOOL QUAN LY DATABASE MYSQL")
    print("=" * 70)
    print()


def get_config_file():
    """Lấy đường dẫn file config"""
    script_dir = Path(__file__).resolve().parent
    config_file = script_dir / "database_config.json"
    return config_file


def load_config():
    """Load cấu hình từ file"""
    config_file = get_config_file()
    
    default_config = {
        'version': '1.0',
        'default_xampp_path': r'C:\xampp',
        'connections': [
            {
                'name': 'XAMPP Local',
                'host': 'localhost',
                'port': 3306,
                'user': 'root',
                'password': '',
                'default_db': '',
                'xampp_path': r'C:\xampp'
            }
        ],
        'backup_folder': 'database_backups',
        'default_connection': 0
    }
    
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)
                # Merge với default config
                for key in default_config:
                    if key not in loaded_config:
                        loaded_config[key] = default_config[key]
                return loaded_config
        except Exception as e:
            print(f"[!] Lỗi đọc config: {e}")
            return default_config
    else:
        save_config(default_config)
        return default_config


def save_config(config):
    """Lưu cấu hình vào file"""
    config_file = get_config_file()
    
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[X] Lỗi lưu config: {e}")
        return False


def get_mysql_path(connection):
    """Lấy đường dẫn MySQL từ XAMPP"""
    xampp_path = connection.get('xampp_path', r'C:\xampp')
    mysql_path = os.path.join(xampp_path, 'mysql', 'bin', 'mysql.exe')
    mysqldump_path = os.path.join(xampp_path, 'mysql', 'bin', 'mysqldump.exe')
    
    return mysql_path, mysqldump_path


def test_connection(connection):
    """Kiểm tra kết nối database"""
    mysql_path, _ = get_mysql_path(connection)
    
    if not os.path.exists(mysql_path):
        return False, "Không tìm thấy MySQL tại: " + mysql_path
    
    try:
        # Test connection bằng cách chạy lệnh mysql
        cmd = [
            mysql_path,
            '-h', connection['host'],
            '-P', str(connection['port']),
            '-u', connection['user']
        ]
        
        if connection.get('password'):
            cmd.extend(['-p' + connection['password']])  # -ppassword (no space)
        
        cmd.extend(['-e', 'SELECT 1'])
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            return True, "Kết nối thành công"
        else:
            return False, result.stderr or "Kết nối thất bại"
    except Exception as e:
        return False, str(e)


def list_databases(connection):
    """Liệt kê danh sách databases"""
    mysql_path, _ = get_mysql_path(connection)
    
    if not os.path.exists(mysql_path):
        return []
    
    try:
        cmd = [
            mysql_path,
            '-h', connection['host'],
            '-P', str(connection['port']),
            '-u', connection['user']
        ]
        
        if connection.get('password'):
            cmd.append('-p' + connection['password'])  # -ppassword (no space)
        
        cmd.extend([
            '-e', 'SHOW DATABASES;',
            '-s',  # Silent mode
            '-N'   # Skip column names
        ])
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            databases = [db.strip() for db in result.stdout.strip().split('\n') if db.strip()]
            # Bỏ qua system databases
            databases = [db for db in databases if db not in ['information_schema', 'performance_schema', 'mysql', 'sys']]
            return databases
        else:
            return []
    except Exception as e:
        print(f"[!] Lỗi: {e}")
        return []


def list_tables(connection, database):
    """Liệt kê danh sách tables trong database"""
    mysql_path, _ = get_mysql_path(connection)
    
    if not os.path.exists(mysql_path):
        return []
    
    try:
        cmd = [
            mysql_path,
            '-h', connection['host'],
            '-P', str(connection['port']),
            '-u', connection['user']
        ]
        
        if connection.get('password'):
            cmd.append('-p' + connection['password'])  # -ppassword (no space)
        
        cmd.extend([
            database,
            '-e', 'SHOW TABLES;',
            '-s',  # Silent mode
            '-N'   # Skip column names
        ])
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            tables = [table.strip() for table in result.stdout.strip().split('\n') if table.strip()]
            return tables
        else:
            return []
    except Exception as e:
        print(f"[!] Lỗi: {e}")
        return []


def get_table_structure(connection, database, table):
    """Lấy cấu trúc của table"""
    mysql_path, _ = get_mysql_path(connection)
    
    if not os.path.exists(mysql_path):
        return None
    
    try:
        cmd = [
            mysql_path,
            '-h', connection['host'],
            '-P', str(connection['port']),
            '-u', connection['user']
        ]
        
        if connection.get('password'):
            cmd.append('-p' + connection['password'])  # -ppassword (no space)
        
        cmd.extend([
            database,
            '-e', f'DESCRIBE {table};'
        ])
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            return result.stdout
        else:
            return None
    except Exception as e:
        print(f"[!] Lỗi: {e}")
        return None


def backup_database(connection, database, output_file):
    """Backup database"""
    _, mysqldump_path = get_mysql_path(connection)
    
    if not os.path.exists(mysqldump_path):
        return False, "Không tìm thấy mysqldump tại: " + mysqldump_path
    
    try:
        # Tạo thư mục backup nếu chưa có
        backup_dir = os.path.dirname(output_file)
        if backup_dir and not os.path.exists(backup_dir):
            os.makedirs(backup_dir, exist_ok=True)
        
        cmd = [
            mysqldump_path,
            '-h', connection['host'],
            '-P', str(connection['port']),
            '-u', connection['user']
        ]
        
        if connection.get('password'):
            cmd.append('-p' + connection['password'])  # -ppassword (no space)
        
        cmd.extend([
            '--single-transaction',
            '--routines',
            '--triggers',
            database
        ])
        
        with open(output_file, 'w', encoding='utf-8') as f:
            result = subprocess.run(
                cmd,
                stdout=f,
                stderr=subprocess.PIPE,
                text=True,
                timeout=300  # 5 minutes timeout
            )
        
        if result.returncode == 0:
            file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
            return True, f"Backup thành công! Kích thước: {file_size:.2f} MB"
        else:
            return False, result.stderr or "Backup thất bại"
    except Exception as e:
        return False, str(e)


def restore_database(connection, database, input_file):
    """Restore database từ file SQL"""
    mysql_path, _ = get_mysql_path(connection)
    
    if not os.path.exists(mysql_path):
        return False, "Không tìm thấy MySQL tại: " + mysql_path
    
    if not os.path.exists(input_file):
        return False, "File không tồn tại: " + input_file
    
    try:
        cmd = [
            mysql_path,
            '-h', connection['host'],
            '-P', str(connection['port']),
            '-u', connection['user']
        ]
        
        if connection.get('password'):
            cmd.append('-p' + connection['password'])  # -ppassword (no space)
        
        cmd.append(database)
        
        with open(input_file, 'r', encoding='utf-8') as f:
            result = subprocess.run(
                cmd,
                stdin=f,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=300  # 5 minutes timeout
            )
        
        if result.returncode == 0:
            return True, "Restore thành công!"
        else:
            return False, result.stderr or "Restore thất bại"
    except Exception as e:
        return False, str(e)


def execute_query(connection, database, query):
    """Chạy SQL query"""
    mysql_path, _ = get_mysql_path(connection)
    
    if not os.path.exists(mysql_path):
        return False, None, "Không tìm thấy MySQL tại: " + mysql_path
    
    try:
        cmd = [
            mysql_path,
            '-h', connection['host'],
            '-P', str(connection['port']),
            '-u', connection['user']
        ]
        
        if connection.get('password'):
            cmd.append('-p' + connection['password'])  # -ppassword (no space)
        
        cmd.extend([
            database,
            '-e', query
        ])
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return True, result.stdout, None
        else:
            return False, None, result.stderr or "Query thất bại"
    except Exception as e:
        return False, None, str(e)


def export_table(connection, database, table, output_file):
    """Export table ra file SQL"""
    _, mysqldump_path = get_mysql_path(connection)
    
    if not os.path.exists(mysqldump_path):
        return False, "Không tìm thấy mysqldump tại: " + mysqldump_path
    
    try:
        # Tạo thư mục nếu chưa có
        export_dir = os.path.dirname(output_file)
        if export_dir and not os.path.exists(export_dir):
            os.makedirs(export_dir, exist_ok=True)
        
        cmd = [
            mysqldump_path,
            '-h', connection['host'],
            '-P', str(connection['port']),
            '-u', connection['user']
        ]
        
        if connection.get('password'):
            cmd.append('-p' + connection['password'])  # -ppassword (no space)
        
        cmd.extend([
            '--single-transaction',
            database,
            table
        ])
        
        with open(output_file, 'w', encoding='utf-8') as f:
            result = subprocess.run(
                cmd,
                stdout=f,
                stderr=subprocess.PIPE,
                text=True,
                timeout=300
            )
        
        if result.returncode == 0:
            file_size = os.path.getsize(output_file) / 1024  # KB
            return True, f"Export thành công! Kích thước: {file_size:.2f} KB"
        else:
            return False, result.stderr or "Export thất bại"
    except Exception as e:
        return False, str(e)


def show_connections_menu(config):
    """Hiển thị menu quản lý connections"""
    while True:
        print("\n" + "=" * 70)
        print("  QUAN LY KET NOI DATABASE")
        print("=" * 70)
        
        connections = config.get('connections', [])
        
        if connections:
            print("\nDanh sách kết nối:")
            for idx, conn in enumerate(connections):
                default_marker = " (Mặc định)" if idx == config.get('default_connection', 0) else ""
                print(f"  {idx + 1}. {conn['name']}{default_marker}")
                print(f"     Host: {conn['host']}:{conn['port']}, User: {conn['user']}")
        else:
            print("\n[!] Chưa có kết nối nào")
        
        print("\n" + "-" * 70)
        print("LENH:")
        print("  a - Them ket noi moi")
        print("  e [so] - Sua ket noi")
        print("  d [so] - Xoa ket noi")
        print("  t [so] - Test ket noi")
        print("  s [so] - Dat lam mac dinh")
        print("  0 - Quay lai")
        print("=" * 70)
        
        choice = input("\nChon lenh: ").strip().lower()
        
        if choice == '0':
            break
        elif choice == 'a':
            add_connection(config, connections)
        elif choice.startswith('e '):
            idx_str = choice.replace('e ', '').strip()
            try:
                idx = int(idx_str) - 1
                if 0 <= idx < len(connections):
                    edit_connection(config, connections, idx)
                else:
                    print("[X] So thu tu khong hop le!")
            except ValueError:
                print("[X] Vui long nhap so hop le!")
        elif choice.startswith('d '):
            idx_str = choice.replace('d ', '').strip()
            try:
                idx = int(idx_str) - 1
                if 0 <= idx < len(connections):
                    delete_connection(config, connections, idx)
                else:
                    print("[X] So thu tu khong hop le!")
            except ValueError:
                print("[X] Vui long nhap so hop le!")
        elif choice.startswith('t '):
            idx_str = choice.replace('t ', '').strip()
            try:
                idx = int(idx_str) - 1
                if 0 <= idx < len(connections):
                    test_connection_result = test_connection(connections[idx])
                    if test_connection_result[0]:
                        print(f"[OK] {test_connection_result[1]}")
                    else:
                        print(f"[X] {test_connection_result[1]}")
                else:
                    print("[X] So thu tu khong hop le!")
            except ValueError:
                print("[X] Vui long nhap so hop le!")
        elif choice.startswith('s '):
            idx_str = choice.replace('s ', '').strip()
            try:
                idx = int(idx_str) - 1
                if 0 <= idx < len(connections):
                    config['default_connection'] = idx
                    save_config(config)
                    print(f"[OK] Da dat '{connections[idx]['name']}' lam ket noi mac dinh")
                else:
                    print("[X] So thu tu khong hop le!")
            except ValueError:
                print("[X] Vui long nhap so hop le!")
        else:
            print("[X] Lenh khong hop le!")


def add_connection(config, connections):
    """Thêm kết nối mới"""
    print("\n" + "=" * 70)
    print("  THEM KET NOI MOI")
    print("=" * 70)
    
    try:
        name = input("\nTen ket noi: ").strip()
        if not name:
            print("[X] Ten ket noi khong duoc de trong!")
            return
        
        host = input("Host (mặc định: localhost): ").strip() or 'localhost'
        port = input("Port (mặc định: 3306): ").strip() or '3306'
        try:
            port = int(port)
        except ValueError:
            print("[X] Port phai la so!")
            return
        
        user = input("Username (mặc định: root): ").strip() or 'root'
        password = input("Password (Enter de de trong): ").strip()
        
        xampp_path = input(f"Duong dan XAMPP (mặc định: {config.get('default_xampp_path', r'C:\xampp')}): ").strip()
        if not xampp_path:
            xampp_path = config.get('default_xampp_path', r'C:\xampp')
        
        default_db = input("Database mac dinh (Enter de de trong): ").strip()
        
        new_connection = {
            'name': name,
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'default_db': default_db,
            'xampp_path': xampp_path
        }
        
        connections.append(new_connection)
        config['connections'] = connections
        
        if save_config(config):
            print(f"\n[OK] Da them ket noi: {name}")
        else:
            print("[X] Loi luu config!")
            connections.pop()
    except Exception as e:
        print(f"[X] Loi: {e}")


def edit_connection(config, connections, idx):
    """Sửa kết nối"""
    conn = connections[idx]
    
    print("\n" + "=" * 70)
    print(f"  SUA KET NOI: {conn['name']}")
    print("=" * 70)
    print("(Nhan Enter de giu nguyen gia tri cu)\n")
    
    try:
        new_name = input(f"Ten ket noi [{conn['name']}]: ").strip()
        if new_name:
            conn['name'] = new_name
        
        new_host = input(f"Host [{conn['host']}]: ").strip()
        if new_host:
            conn['host'] = new_host
        
        new_port = input(f"Port [{conn['port']}]: ").strip()
        if new_port:
            try:
                conn['port'] = int(new_port)
            except ValueError:
                print("[!] Port khong hop le, giu nguyen gia tri cu")
        
        new_user = input(f"Username [{conn['user']}]: ").strip()
        if new_user:
            conn['user'] = new_user
        
        new_password = input("Password (Enter de giu nguyen, 'none' de xoa): ").strip()
        if new_password:
            if new_password.lower() == 'none':
                conn['password'] = ''
            else:
                conn['password'] = new_password
        
        new_xampp = input(f"Duong dan XAMPP [{conn.get('xampp_path', '')}]: ").strip()
        if new_xampp:
            conn['xampp_path'] = new_xampp
        
        new_db = input(f"Database mac dinh [{conn.get('default_db', '')}]: ").strip()
        if new_db:
            conn['default_db'] = new_db
        
        if save_config(config):
            print(f"\n[OK] Da luu thay doi!")
        else:
            print("[X] Loi luu config!")
    except Exception as e:
        print(f"[X] Loi: {e}")


def delete_connection(config, connections, idx):
    """Xóa kết nối"""
    conn = connections[idx]
    
    print(f"\n[!] Ban sap xoa ket noi: {conn['name']}")
    confirm = input("Xac nhan xoa? (YES de xac nhan): ").strip()
    
    if confirm == "YES":
        connections.pop(idx)
        config['connections'] = connections
        
        # Nếu xóa connection mặc định, chuyển sang connection đầu tiên
        if config.get('default_connection', 0) == idx:
            if connections:
                config['default_connection'] = 0
            else:
                config['default_connection'] = 0
        
        # Điều chỉnh default_connection nếu cần
        if config.get('default_connection', 0) > idx:
            config['default_connection'] -= 1
        
        if save_config(config):
            print(f"\n[OK] Da xoa ket noi: {conn['name']}")
        else:
            print("[X] Loi luu config!")
            connections.insert(idx, conn)
    else:
        print("[*] Da huy")


def show_databases_menu(connection, config):
    """Hiển thị menu quản lý databases"""
    while True:
        print("\n" + "=" * 70)
        print(f"  DATABASES - {connection['name']}")
        print("=" * 70)
        print(f"Host: {connection['host']}:{connection['port']}, User: {connection['user']}\n")
        
        databases = list_databases(connection)
        
        if databases:
            print("Danh sach databases:")
            for idx, db in enumerate(databases, start=1):
                print(f"  {idx}. {db}")
        else:
            print("[!] Khong tim thay database nao hoac khong the ket noi")
        
        print("\n" + "-" * 70)
        print("LENH:")
        print("  [so] - Chon database")
        print("  b [so] - Backup database")
        print("  r - Restore database")
        print("  q - Chay SQL query")
        print("  0 - Quay lai")
        print("=" * 70)
        
        choice = input("\nChon lenh: ").strip().lower()
        
        if choice == '0':
            break
        elif choice.startswith('b '):
            idx_str = choice.replace('b ', '').strip()
            try:
                idx = int(idx_str) - 1
                if 0 <= idx < len(databases):
                    backup_db_menu(connection, databases[idx], config)
                else:
                    print("[X] So thu tu khong hop le!")
            except ValueError:
                print("[X] Vui long nhap so hop le!")
        elif choice == 'r':
            restore_db_menu(connection, config)
        elif choice == 'q':
            query_menu(connection, config)
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(databases):
                    show_tables_menu(connection, databases[idx], config)
                else:
                    print("[X] So thu tu khong hop le!")
            except ValueError:
                print("[X] Lenh khong hop le!")


def backup_db_menu(connection, database, config):
    """Menu backup database"""
    print(f"\n[>] Backup database: {database}")
    
    # Tạo thư mục backup
    backup_folder = config.get('backup_folder', 'database_backups')
    backup_dir = os.path.join(os.path.expanduser('~'), backup_folder)
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir, exist_ok=True)
    
    # Tên file backup
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(backup_dir, f'{database}_{timestamp}.sql')
    
    print(f"[>] Dang backup...")
    success, message = backup_database(connection, database, backup_file)
    
    if success:
        print(f"[OK] {message}")
        print(f"     File: {backup_file}")
    else:
        print(f"[X] {message}")
    
    input("\nNhan Enter de tiep tuc...")


def restore_db_menu(connection, config):
    """Menu restore database"""
    print("\n" + "=" * 70)
    print("  RESTORE DATABASE")
    print("=" * 70)
    
    backup_folder = config.get('backup_folder', 'database_backups')
    backup_dir = os.path.join(os.path.expanduser('~'), backup_folder)
    
    # Hiển thị danh sách file backup
    if os.path.exists(backup_dir):
        backup_files = [f for f in os.listdir(backup_dir) if f.endswith('.sql')]
        if backup_files:
            print("\nDanh sach file backup:")
            for idx, file in enumerate(sorted(backup_files, reverse=True)[:20], start=1):
                file_path = os.path.join(backup_dir, file)
                file_size = os.path.getsize(file_path) / (1024 * 1024)
                print(f"  {idx}. {file} ({file_size:.2f} MB)")
        else:
            print("\n[!] Khong co file backup nao")
    else:
        print(f"\n[!] Thu muc backup khong ton tai: {backup_dir}")
    
    backup_file = input("\nNhap duong dan file SQL (hoac ten file): ").strip().strip('"')
    
    if not backup_file:
        print("[*] Da huy")
        return
    
    # Nếu chỉ là tên file, tìm trong thư mục backup
    if not os.path.isabs(backup_file) and os.path.exists(backup_dir):
        backup_file = os.path.join(backup_dir, backup_file)
    
    if not os.path.exists(backup_file):
        print(f"[X] File khong ton tai: {backup_file}")
        input("\nNhan Enter de tiep tuc...")
        return
    
    database = input("Nhap ten database de restore (se tao moi neu chua co): ").strip()
    if not database:
        print("[X] Ten database khong duoc de trong!")
        input("\nNhan Enter de tiep tuc...")
        return
    
    print(f"\n[!] Ban sap restore database '{database}' tu file: {backup_file}")
    print("[!] CANH BAO: Database hien tai se bi ghi de!")
    confirm = input("Xac nhan? (YES de xac nhan): ").strip()
    
    if confirm != "YES":
        print("[*] Da huy")
        return
    
    print(f"\n[>] Dang restore...")
    success, message = restore_database(connection, database, backup_file)
    
    if success:
        print(f"[OK] {message}")
    else:
        print(f"[X] {message}")
    
    input("\nNhan Enter de tiep tuc...")


def query_menu(connection, config):
    """Menu chạy SQL query"""
    print("\n" + "=" * 70)
    print("  CHAY SQL QUERY")
    print("=" * 70)
    
    database = input("\nNhap ten database: ").strip()
    if not database:
        print("[X] Ten database khong duoc de trong!")
        return
    
    print("\nNhap SQL query (ket thuc bang ';'):")
    print("(Nhan Enter de ket thuc nhap, 'exit' de thoat)")
    
    query_lines = []
    while True:
        line = input("SQL> " if not query_lines else "   > ").strip()
        if line.lower() == 'exit':
            return
        if not line and query_lines:
            break
        if line:
            query_lines.append(line)
    
    if not query_lines:
        print("[*] Khong co query nao")
        return
    
    query = ' '.join(query_lines)
    
    print(f"\n[>] Dang chay query...")
    success, output, error = execute_query(connection, database, query)
    
    if success:
        if output:
            print("\nKet qua:")
            print(output)
        else:
            print("[OK] Query da chay thanh cong")
    else:
        print(f"[X] Loi: {error}")
    
    input("\nNhan Enter de tiep tuc...")


def show_tables_menu(connection, database, config):
    """Hiển thị menu quản lý tables"""
    while True:
        print("\n" + "=" * 70)
        print(f"  TABLES - {database}")
        print("=" * 70)
        
        tables = list_tables(connection, database)
        
        if tables:
            print("\nDanh sach tables:")
            for idx, table in enumerate(tables, start=1):
                print(f"  {idx}. {table}")
        else:
            print("\n[!] Khong co table nao hoac khong the ket noi")
        
        print("\n" + "-" * 70)
        print("LENH:")
        print("  [so] - Xem cau truc table")
        print("  e [so] - Export table")
        print("  b - Backup toan bo database")
        print("  0 - Quay lai")
        print("=" * 70)
        
        choice = input("\nChon lenh: ").strip().lower()
        
        if choice == '0':
            break
        elif choice.startswith('e '):
            idx_str = choice.replace('e ', '').strip()
            try:
                idx = int(idx_str) - 1
                if 0 <= idx < len(tables):
                    export_table_menu(connection, database, tables[idx], config)
                else:
                    print("[X] So thu tu khong hop le!")
            except ValueError:
                print("[X] Vui long nhap so hop le!")
        elif choice == 'b':
            backup_db_menu(connection, database, config)
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(tables):
                    structure = get_table_structure(connection, database, tables[idx])
                    if structure:
                        print(f"\nCau truc table '{tables[idx]}':")
                        print(structure)
                    else:
                        print("[X] Khong the lay cau truc table")
                    input("\nNhan Enter de tiep tuc...")
                else:
                    print("[X] So thu tu khong hop le!")
            except ValueError:
                print("[X] Lenh khong hop le!")


def export_table_menu(connection, database, table, config):
    """Menu export table"""
    print(f"\n[>] Export table: {table}")
    
    # Tạo thư mục export
    backup_folder = config.get('backup_folder', 'database_backups')
    export_dir = os.path.join(os.path.expanduser('~'), backup_folder, 'exports')
    if not os.path.exists(export_dir):
        os.makedirs(export_dir, exist_ok=True)
    
    # Tên file export
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    export_file = os.path.join(export_dir, f'{database}_{table}_{timestamp}.sql')
    
    print(f"[>] Dang export...")
    success, message = export_table(connection, database, table, export_file)
    
    if success:
        print(f"[OK] {message}")
        print(f"     File: {export_file}")
    else:
        print(f"[X] {message}")
    
    input("\nNhan Enter de tiep tuc...")


def main():
    """Hàm chính của tool"""
    print_header()
    
    config = load_config()
    connections = config.get('connections', [])
    
    if not connections:
        print("[!] Chua co ket noi nao. Vui long them ket noi truoc.")
        show_connections_menu(config)
        config = load_config()
        connections = config.get('connections', [])
        
        if not connections:
            print("\n[!] Van chua co ket noi. Thoat tool.")
            return
    
    while True:
        # Lấy connection mặc định
        default_idx = config.get('default_connection', 0)
        if default_idx >= len(connections):
            default_idx = 0
            config['default_connection'] = 0
        
        current_connection = connections[default_idx]
        
        print("\n" + "=" * 70)
        print("  MENU CHINH")
        print("=" * 70)
        print(f"\nKet noi hien tai: {current_connection['name']}")
        print(f"Host: {current_connection['host']}:{current_connection['port']}")
        print(f"User: {current_connection['user']}")
        
        print("\n" + "-" * 70)
        print("LENH:")
        print("  1 - Quan ly databases")
        print("  2 - Quan ly ket noi")
        print("  s - Cai dat")
        print("  0 - Thoat")
        print("=" * 70)
        
        choice = input("\nChon lenh: ").strip().lower()
        
        if choice == '0':
            print("\n[*] Thoat tool")
            break
        elif choice == '1':
            show_databases_menu(current_connection, config)
        elif choice == '2':
            show_connections_menu(config)
            config = load_config()  # Reload config
            connections = config.get('connections', [])
        elif choice == 's':
            show_settings_menu(config)
            config = load_config()  # Reload config
        else:
            print("[X] Lenh khong hop le!")


def show_settings_menu(config):
    """Hiển thị menu cài đặt"""
    while True:
        print("\n" + "=" * 70)
        print("  CAI DAT")
        print("=" * 70)
        print(f"\n1. Duong dan XAMPP mac dinh: {config.get('default_xampp_path', 'Chua cau hinh')}")
        print(f"2. Thu muc backup: {config.get('backup_folder', 'database_backups')}")
        print("\n0. Quay lai")
        print("=" * 70)
        
        choice = input("\nChon muc can chinh sua (so): ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            new_path = input("Nhap duong dan XAMPP mac dinh: ").strip().strip('"')
            if new_path:
                config['default_xampp_path'] = new_path
                save_config(config)
                print("[OK] Da cap nhat!")
            else:
                print("[X] Duong dan khong hop le!")
        elif choice == '2':
            new_folder = input("Nhap ten thu muc backup: ").strip()
            if new_folder:
                config['backup_folder'] = new_folder
                save_config(config)
                print("[OK] Da cap nhat!")
            else:
                print("[X] Ten thu muc khong hop le!")
        else:
            print("[X] Lua chon khong hop le!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[X] Da huy!")
    except Exception as e:
        print(f"\n[X] Loi: {e}")
        import traceback
        traceback.print_exc()

