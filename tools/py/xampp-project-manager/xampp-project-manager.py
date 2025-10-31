#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool: Quản lý và cài đặt dự án (Windows)
Mục đích: Quản lý dự án XAMPP trên Windows, cấu hình hosts, PHP version, và mở dự án
"""

import subprocess
import os
import json
import sys
import shutil
import re
from pathlib import Path
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
    print("=" * 60)
    print("  TOOL QUAN LY VA CAI DAT DU AN (WINDOWS)")
    print("=" * 60)
    print()


def get_config_file():
    """Lấy đường dẫn file config"""
    script_dir = Path(__file__).resolve().parent
    config_file = script_dir / "xampp_config.json"
    return config_file


def load_config():
    """Load cấu hình từ file"""
    config_file = get_config_file()
    
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[!] Loi doc config: {e}")
            return get_default_config()
    else:
        config = get_default_config()
        save_config(config)
        return config


def save_config(config):
    """Lưu cấu hình vào file"""
    config_file = get_config_file()
    
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[X] Loi luu config: {e}")
        return False


def get_default_config():
    """Lấy cấu hình mặc định"""
    # Đường dẫn XAMPP mặc định trên Windows
    default_xampp = r"C:\xampp"
    default_htdocs = r"C:\xampp\htdocs"
    default_hosts = r"C:\Windows\System32\drivers\etc\hosts"
    
    return {
        'version': '1.0',
        'xampp_path': default_xampp,
        'htdocs_path': default_htdocs,
        'hosts_file': default_hosts,
        'apache_path': os.path.join(default_xampp, 'apache', 'bin', 'httpd.exe') if os.path.exists(default_xampp) else '',
        'default_editor': 'code',  # 'code' hoặc 'cursor'
        'php_versions': [],
        'hosts': []
    }


def list_projects(htdocs_path: str) -> List[str]:
    """Liệt kê các dự án trong htdocs"""
    projects = []
    
    if not os.path.exists(htdocs_path):
        return projects
    
    try:
        for item in os.listdir(htdocs_path):
            item_path = os.path.join(htdocs_path, item)
            if os.path.isdir(item_path):
                # Bỏ qua các thư mục đặc biệt
                if item.lower() not in ['cgi-bin', 'webalizer', 'usage']:
                    projects.append(item)
    except Exception as e:
        print(f"[!] Loi doc thu muc htdocs: {e}")
    
    return sorted(projects)


def open_project_in_editor(project_path: str, editor: str = 'code'):
    """Mở dự án trong VSCode hoặc Cursor"""
    if not os.path.exists(project_path):
        print(f"[X] Duong dan khong ton tai: {project_path}")
        return False
    
    try:
        if editor == 'cursor':
            # Thử mở bằng Cursor
            cmd = ['cursor', project_path]
        else:
            # Mở bằng VSCode
            cmd = ['code', project_path]
        
        print(f"\n[>] Dang mo du an trong {editor}...")
        subprocess.Popen(cmd, shell=True)
        print(f"[OK] Da mo du an: {project_path}")
        return True
    except FileNotFoundError:
        print(f"[X] Khong tim thay lenh '{editor}'")
        print(f"[i] Vui long cai dat {editor} hoac them vao PATH")
        return False
    except Exception as e:
        print(f"[X] Loi mo du an: {e}")
        return False


def clone_project(source: str, project_name: str, htdocs_path: str):
    """Clone dự án từ Git repository"""
    project_path = os.path.join(htdocs_path, project_name)
    
    if os.path.exists(project_path):
        print(f"[X] Du an '{project_name}' da ton tai!")
        return False
    
    try:
        print(f"\n[>] Dang clone du an tu: {source}")
        print(f"    Den: {project_path}")
        
        # Chạy lệnh git clone
        result = subprocess.run(
            ['git', 'clone', source, project_path],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"[OK] Da clone du an thanh cong!")
            return True
        else:
            print(f"[X] Loi khi clone:")
            print(result.stderr)
            return False
    except FileNotFoundError:
        print("[X] Khong tim thay lenh 'git'")
        print("[i] Vui long cai dat Git hoac them vao PATH")
        return False
    except Exception as e:
        print(f"[X] Loi: {e}")
        return False


def delete_project(project_name: str, htdocs_path: str):
    """Xóa dự án"""
    project_path = os.path.join(htdocs_path, project_name)
    
    if not os.path.exists(project_path):
        print(f"[X] Du an '{project_name}' khong ton tai!")
        return False
    
    try:
        print(f"\n[!] BAN SAP XOA DU AN: {project_name}")
        print(f"    Duong dan: {project_path}")
        confirm = input("Xac nhan xoa? (YES de xac nhan): ").strip()
        
        if confirm == "YES":
            shutil.rmtree(project_path)
            print(f"[OK] Da xoa du an: {project_name}")
            return True
        else:
            print("Da huy")
            return False
    except Exception as e:
        print(f"[X] Loi xoa du an: {e}")
        return False


def rename_project(old_name: str, new_name: str, htdocs_path: str):
    """Đổi tên dự án"""
    old_path = os.path.join(htdocs_path, old_name)
    new_path = os.path.join(htdocs_path, new_name)
    
    if not os.path.exists(old_path):
        print(f"[X] Du an '{old_name}' khong ton tai!")
        return False
    
    if os.path.exists(new_path):
        print(f"[X] Du an '{new_name}' da ton tai!")
        return False
    
    try:
        os.rename(old_path, new_path)
        print(f"[OK] Da doi ten du an: {old_name} -> {new_name}")
        return True
    except Exception as e:
        print(f"[X] Loi doi ten: {e}")
        return False


def read_hosts_file(hosts_file: str) -> List[str]:
    """Đọc nội dung file hosts"""
    if not os.path.exists(hosts_file):
        return []
    
    try:
        with open(hosts_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return [line.rstrip('\n') for line in lines]
    except PermissionError:
        print("[X] Khong co quyen doc file hosts!")
        print("[i] Can chay voi quyen Administrator")
        return []
    except Exception as e:
        print(f"[X] Loi doc file hosts: {e}")
        return []


def write_hosts_file(hosts_file: str, lines: List[str]):
    """Ghi nội dung vào file hosts"""
    try:
        with open(hosts_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines) + '\n')
        return True
    except PermissionError:
        print("[X] Khong co quyen ghi file hosts!")
        print("[i] Can chay voi quyen Administrator")
        return False
    except Exception as e:
        print(f"[X] Loi ghi file hosts: {e}")
        return False


def parse_hosts_lines(lines: List[str]) -> Dict[str, str]:
    """Parse các dòng hosts để lấy domain -> ip mapping"""
    hosts_map = {}
    
    for line in lines:
        line = line.strip()
        # Bỏ qua comment và dòng trống
        if not line or line.startswith('#'):
            continue
        
        # Parse dòng hosts: IP domain1 domain2 ...
        parts = line.split()
        if len(parts) >= 2:
            ip = parts[0]
            for domain in parts[1:]:
                if not domain.startswith('#'):
                    hosts_map[domain] = ip
                    break  # Chỉ lấy domain đầu tiên
    
    return hosts_map


def add_host_entry(domain: str, ip: str = '127.0.0.1', hosts_file: str = None):
    """Thêm entry vào hosts file"""
    if hosts_file is None:
        config = load_config()
        hosts_file = config.get('hosts_file', r"C:\Windows\System32\drivers\etc\hosts")
    
    lines = read_hosts_file(hosts_file)
    hosts_map = parse_hosts_lines(lines)
    
    # Kiểm tra domain đã tồn tại chưa
    if domain in hosts_map:
        print(f"[!] Domain '{domain}' da ton tai trong hosts file!")
        return False
    
    # Tìm vị trí chèn (sau các comment cuối cùng)
    insert_pos = len(lines)
    for i, line in enumerate(lines):
        if line.strip() and not line.strip().startswith('#'):
            insert_pos = i
            break
    
    # Thêm entry mới
    new_line = f"{ip}\t{domain}"
    lines.insert(insert_pos, new_line)
    
    if write_hosts_file(hosts_file, lines):
        print(f"[OK] Da them host: {domain} -> {ip}")
        return True
    return False


def delete_host_entry(domain: str, hosts_file: str = None):
    """Xóa entry khỏi hosts file"""
    if hosts_file is None:
        config = load_config()
        hosts_file = config.get('hosts_file', r"C:\Windows\System32\drivers\etc\hosts")
    
    lines = read_hosts_file(hosts_file)
    
    # Tìm và xóa dòng chứa domain
    new_lines = []
    found = False
    
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            new_lines.append(line)
            continue
        
        parts = stripped.split()
        if len(parts) >= 2 and parts[1] == domain:
            found = True
            continue  # Bỏ qua dòng này
        else:
            new_lines.append(line)
    
    if not found:
        print(f"[X] Khong tim thay domain '{domain}' trong hosts file!")
        return False
    
    if write_hosts_file(hosts_file, new_lines):
        print(f"[OK] Da xoa host: {domain}")
        return True
    return False


def edit_host_entry(old_domain: str, new_domain: str = None, new_ip: str = None, hosts_file: str = None):
    """Sửa entry trong hosts file"""
    if hosts_file is None:
        config = load_config()
        hosts_file = config.get('hosts_file', r"C:\Windows\System32\drivers\etc\hosts")
    
    lines = read_hosts_file(hosts_file)
    
    # Tìm và sửa dòng chứa domain
    new_lines = []
    found = False
    
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            new_lines.append(line)
            continue
        
        parts = stripped.split()
        if len(parts) >= 2 and parts[1] == old_domain:
            found = True
            ip = new_ip if new_ip else parts[0]
            domain = new_domain if new_domain else old_domain
            new_line = f"{ip}\t{domain}"
            new_lines.append(new_line)
        else:
            new_lines.append(line)
    
    if not found:
        print(f"[X] Khong tim thay domain '{old_domain}' trong hosts file!")
        return False
    
    if write_hosts_file(hosts_file, new_lines):
        print(f"[OK] Da sua host: {old_domain}")
        return True
    return False


def list_hosts(hosts_file: str = None):
    """Liệt kê các host entry"""
    if hosts_file is None:
        config = load_config()
        hosts_file = config.get('hosts_file', r"C:\Windows\System32\drivers\etc\hosts")
    
    hosts_map = parse_hosts_lines(read_hosts_file(hosts_file))
    
    if not hosts_map:
        print("\n[!] Khong co host entry nao")
        return
    
    print("\n" + "=" * 60)
    print("  DANH SACH HOSTS")
    print("=" * 60)
    
    for idx, (domain, ip) in enumerate(sorted(hosts_map.items()), start=1):
        print(f"{idx}. {ip:15} -> {domain}")


def get_php_versions(xampp_path: str) -> List[str]:
    """Lấy danh sách phiên bản PHP có sẵn"""
    php_dir = os.path.join(xampp_path, 'php')
    
    if not os.path.exists(php_dir):
        return []
    
    versions = []
    try:
        for item in os.listdir(php_dir):
            item_path = os.path.join(php_dir, item)
            if os.path.isdir(item_path):
                # Kiểm tra xem có file php.exe không
                php_exe = os.path.join(item_path, 'php.exe')
                if os.path.exists(php_exe):
                    versions.append(item)
    except Exception:
        pass
    
    return sorted(versions, reverse=True)


def show_add_php_version_guide(xampp_path: str):
    """Hiển thị hướng dẫn thêm PHP version mới"""
    print("\n" + "=" * 60)
    print("  HUONG DAN THEM PHP VERSION MOI VAO XAMPP")
    print("=" * 60)
    
    php_dir = os.path.join(xampp_path, 'php')
    print(f"\n📁 Thu muc PHP: {php_dir}")
    
    print("\n" + "-" * 60)
    print("CÁCH 1: Tải PHP từ Windows.php.net (Khuyên dùng)")
    print("-" * 60)
    print("""
1. Truy cập: https://windows.php.net/download/
2. Tải phiên bản PHP phù hợp (Thread Safe, VC16 hoặc VC15):
   - VC16: cho PHP 7.2 trở lên (Apache 2.4)
   - VC15: cho PHP 7.1 trở xuống
   
3. Giải nén file ZIP vào thư mục php:
   {php_dir}\\php[version]
   
   Ví dụ: C:\\xampp\\php\\php8.4
    
4. Đảm bảo thư mục mới có các file:
   - php.exe
   - php8apache2_4.dll (hoặc php7apache2_4.dll)
   - php.ini
   - Các file DLL cần thiết

5. Sao chép php.ini từ thư mục PHP cũ (hoặc từ php.ini-development)
   và chỉnh sửa theo nhu cầu

6. Sau khi thêm xong, chạy lại tool và chọn 'php' để chuyển đổi version
""".format(php_dir=php_dir))
    
    print("-" * 60)
    print("CÁCH 2: Sử dụng XAMPP Add-on (nếu có)")
    print("-" * 60)
    print("""
1. Một số phiên bản XAMPP có add-on PHP riêng
2. Tải từ: https://www.apachefriends.org/download.html
3. Cài đặt add-on theo hướng dẫn
""")
    
    print("-" * 60)
    print("LƯU Ý QUAN TRỌNG:")
    print("-" * 60)
    print("""
⚠️  Phiên bản PHP phải tương thích với Apache:
   - PHP 7.2+ cần Apache 2.4 với VC16
   - PHP 7.1- cần Apache 2.4 với VC15

⚠️  Đảm bảo có file DLL Apache:
   - php8apache2_4.dll cho PHP 8.x
   - php7apache2_4.dll cho PHP 7.x
   
⚠️  File php.ini:
   - Sao chép từ version cũ hoặc từ php.ini-development
   - Chỉnh sửa extension_dir và các extension cần thiết
   
⚠️  Sau khi thêm:
   - Chạy tool và chọn 'php' để xem version mới
   - Chuyển đổi sang version mới bằng số thứ tự hoặc tên
   - Restart Apache để áp dụng (lệnh 'ra')
""")
    
    print("-" * 60)
    print("KIỂM TRA PHIÊN BẢN HIỆN TẠI:")
    print("-" * 60)
    versions = get_php_versions(xampp_path)
    if versions:
        print(f"\n✅ Tim thay {len(versions)} PHP version(s):")
        for idx, version in enumerate(versions, start=1):
            version_path = os.path.join(php_dir, version)
            php_exe = os.path.join(version_path, 'php.exe')
            if os.path.exists(php_exe):
                try:
                    # Lấy version từ php.exe
                    result = subprocess.run(
                        [php_exe, '-v'],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        first_line = result.stdout.split('\n')[0] if result.stdout else ''
                        print(f"   {idx}. {version}")
                        if first_line:
                            print(f"      {first_line.strip()}")
                    else:
                        print(f"   {idx}. {version} (khong the kiem tra)")
                except Exception:
                    print(f"   {idx}. {version}")
            else:
                print(f"   {idx}. {version} (thieu php.exe)")
    else:
        print(f"\n❌ Khong tim thay PHP version nao trong: {php_dir}")
    
    print("\n" + "=" * 60)
    input("\nNhan Enter de quay lai menu...")


def verify_php_version(version_dir: str) -> Dict[str, bool]:
    """Kiểm tra tính hợp lệ của PHP version"""
    checks = {
        'php_exe': False,
        'php_dll': False,
        'php_ini': False,
        'valid': False
    }
    
    if not os.path.exists(version_dir):
        return checks
    
    # Kiểm tra php.exe
    php_exe = os.path.join(version_dir, 'php.exe')
    checks['php_exe'] = os.path.exists(php_exe)
    
    # Kiểm tra PHP DLL
    php_dll = find_php_dll(version_dir)
    checks['php_dll'] = php_dll is not None
    
    # Kiểm tra php.ini
    php_ini = os.path.join(version_dir, 'php.ini')
    php_ini_dev = os.path.join(version_dir, 'php.ini-development')
    php_ini_prod = os.path.join(version_dir, 'php.ini-production')
    checks['php_ini'] = os.path.exists(php_ini) or os.path.exists(php_ini_dev) or os.path.exists(php_ini_prod)
    
    # Version hợp lệ nếu có php.exe và php_dll
    checks['valid'] = checks['php_exe'] and checks['php_dll']
    
    return checks


def find_php_dll(php_version_dir: str) -> Optional[str]:
    """Tìm file PHP Apache DLL trong thư mục PHP version"""
    if not os.path.exists(php_version_dir):
        return None
    
    # Các tên file DLL có thể có
    possible_dlls = [
        'php8apache2_4.dll',
        'php8ts.dll',
        'php7apache2_4.dll',
        'php7ts.dll',
        'php5apache2_4.dll',
        'php5ts.dll'
    ]
    
    # Tìm trong thư mục PHP
    for dll_name in possible_dlls:
        dll_path = os.path.join(php_version_dir, dll_name)
        if os.path.exists(dll_path):
            return dll_path
    
    # Nếu không tìm thấy, thử tìm bất kỳ file .dll nào có chứa "apache"
    try:
        for item in os.listdir(php_version_dir):
            if item.endswith('.dll') and 'apache' in item.lower():
                return os.path.join(php_version_dir, item)
    except Exception:
        pass
    
    return None


def get_current_php_version(xampp_path: str) -> Optional[str]:
    """Lấy phiên bản PHP hiện tại đang được sử dụng"""
    httpd_conf = os.path.join(xampp_path, 'apache', 'conf', 'httpd.conf')
    
    if not os.path.exists(httpd_conf):
        return None
    
    try:
        with open(httpd_conf, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        for line in lines:
            # Tìm dòng LoadModule php_module
            if 'LoadModule' in line and 'php_module' in line:
                # Extract đường dẫn
                match = re.search(r'["\']([^"\']+php[^"\']+\.dll)["\']', line)
                if match:
                    dll_path = match.group(1)
                    # Extract version từ đường dẫn
                    version_match = re.search(r'php[\\/]([^\\/]+)[\\/]', dll_path)
                    if version_match:
                        return version_match.group(1)
    except Exception:
        pass
    
    return None


def switch_php_version(version: str, xampp_path: str):
    """Chuyển đổi phiên bản PHP - tự động chỉnh sửa httpd.conf"""
    php_dir = os.path.join(xampp_path, 'php')
    php_version_dir = os.path.join(php_dir, version)
    target_php_path = os.path.join(php_version_dir, 'php.exe')
    
    if not os.path.exists(target_php_path):
        print(f"[X] Khong tim thay PHP version: {version}")
        return False
    
    # Tìm file DLL
    php_dll = find_php_dll(php_version_dir)
    if not php_dll:
        print(f"[!] Khong tim thay PHP Apache DLL trong {php_version_dir}")
        print(f"[i] Can kiem tra thu muc PHP version va chinh sua thu cong")
        return False
    
    httpd_conf = os.path.join(xampp_path, 'apache', 'conf', 'httpd.conf')
    
    if not os.path.exists(httpd_conf):
        print(f"[X] Khong tim thay file httpd.conf!")
        print(f"    Tim tai: {httpd_conf}")
        return False
    
    try:
        # Đọc file httpd.conf
        with open(httpd_conf, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        # Backup file
        backup_path = httpd_conf + '.backup'
        with open(backup_path, 'w', encoding='utf-8', errors='ignore') as f:
            f.writelines(lines)
        print(f"[i] Da backup httpd.conf -> {backup_path}")
        
        # Tìm và thay thế các dòng liên quan đến PHP
        new_lines = []
        found_php_module = False
        found_phpinidir = False
        
        for line in lines:
            original_line = line
            
            # Tìm và thay thế LoadModule php_module
            if 'LoadModule' in line and 'php_module' in line:
                found_php_module = True
                # Thay thế đường dẫn DLL
                new_dll_path = php_dll.replace('\\', '/')  # Normalize path
                line = re.sub(
                    r'LoadModule\s+php_module\s+["\'][^"\']+["\']',
                    f'LoadModule php_module "{new_dll_path}"',
                    line
                )
            
            # Tìm và thay thế PHPIniDir
            elif 'PHPIniDir' in line:
                found_phpinidir = True
                new_php_dir = php_version_dir.replace('\\', '/')  # Normalize path
                line = re.sub(
                    r'PHPIniDir\s+["\'][^"\']+["\']',
                    f'PHPIniDir "{new_php_dir}"',
                    line
                )
            
            new_lines.append(line)
        
        # Nếu không tìm thấy LoadModule php_module, thêm vào
        if not found_php_module:
            # Tìm vị trí thích hợp để chèn (sau các LoadModule khác)
            insert_pos = len(new_lines)
            for i, line in enumerate(new_lines):
                if 'LoadModule' in line and i < len(new_lines) - 1:
                    insert_pos = i + 1
            
            dll_path = php_dll.replace('\\', '/')
            new_lines.insert(insert_pos, f'LoadModule php_module "{dll_path}"\n')
            found_php_module = True
        
        # Nếu không tìm thấy PHPIniDir, thêm vào
        if not found_phpinidir:
            # Thêm sau LoadModule php_module
            for i, line in enumerate(new_lines):
                if 'LoadModule' in line and 'php_module' in line:
                    php_dir_path = php_version_dir.replace('\\', '/')
                    new_lines.insert(i + 1, f'PHPIniDir "{php_dir_path}"\n')
                    break
        
        # Ghi file mới
        with open(httpd_conf, 'w', encoding='utf-8', errors='ignore') as f:
            f.writelines(new_lines)
        
        print(f"\n[OK] Da chuyen doi PHP version thanh cong: {version}")
        print(f"    PHP DLL: {php_dll}")
        print(f"    PHP Directory: {php_version_dir}")
        print(f"\n[i] Can restart Apache de ap dung thay doi!")
        print(f"    Su dung lenh 'ra' de restart Apache")
        
        return True
        
    except PermissionError:
        print("[X] Khong co quyen chinh sua file httpd.conf!")
        print("[i] Can chay tool voi quyen Administrator")
        return False
    except Exception as e:
        print(f"[X] Loi khi chinh sua httpd.conf: {e}")
        # Khôi phục từ backup nếu có lỗi
        if os.path.exists(backup_path):
            try:
                with open(backup_path, 'r', encoding='utf-8', errors='ignore') as f:
                    backup_lines = f.readlines()
                with open(httpd_conf, 'w', encoding='utf-8', errors='ignore') as f:
                    f.writelines(backup_lines)
                print("[i] Da khoi phuc httpd.conf tu backup")
            except Exception:
                pass
        return False


def restart_xampp(xampp_path: str):
    """Restart XAMPP"""
    xampp_control = os.path.join(xampp_path, 'xampp-control.exe')
    
    if not os.path.exists(xampp_control):
        print(f"[X] Khong tim thay xampp-control.exe!")
        return False
    
    try:
        print("\n[>] Dang mo XAMPP Control Panel...")
        print("[i] Vui long restart Apache va MySQL tu XAMPP Control Panel")
        subprocess.Popen([xampp_control])
        return True
    except Exception as e:
        print(f"[X] Loi mo XAMPP Control: {e}")
        return False


def restart_apache(xampp_path: str):
    """Restart Apache"""
    apache_stop = os.path.join(xampp_path, 'apache_stop.bat')
    apache_start = os.path.join(xampp_path, 'apache_start.bat')
    
    if not os.path.exists(apache_start):
        print("[X] Khong tim thay apache_start.bat!")
        return False
    
    try:
        print("\n[>] Dang restart Apache...")
        
        # Dừng Apache
        if os.path.exists(apache_stop):
            subprocess.run([apache_stop], shell=True, capture_output=True)
        
        # Khởi động lại Apache
        subprocess.run([apache_start], shell=True, capture_output=True)
        
        print("[OK] Da restart Apache!")
        return True
    except Exception as e:
        print(f"[X] Loi restart Apache: {e}")
        return False


def show_settings_menu(config):
    """Hiển thị menu cài đặt"""
    while True:
        print("\n" + "=" * 60)
        print("  CAI DAT")
        print("=" * 60)
        print(f"\n1. Duong dan XAMPP: {config.get('xampp_path', 'Chua cau hinh')}")
        print(f"2. Duong dan htdocs: {config.get('htdocs_path', 'Chua cau hinh')}")
        print(f"3. Duong dan hosts file: {config.get('hosts_file', 'Chua cau hinh')}")
        print(f"4. Duong dan Apache: {config.get('apache_path', 'Chua cau hinh')}")
        print(f"5. Editor mac dinh: {config.get('default_editor', 'code')}")
        print("\n0. Quay lai menu chinh")
        print("=" * 60)
        
        choice = input("\nChon muc can chinh sua (so): ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            new_path = input("Nhap duong dan XAMPP moi: ").strip()
            if new_path and os.path.exists(new_path):
                config['xampp_path'] = new_path
                save_config(config)
                print("[OK] Da cap nhat!")
            else:
                print("[X] Duong dan khong hop le!")
        elif choice == '2':
            new_path = input("Nhap duong dan htdocs moi: ").strip()
            if new_path and os.path.exists(new_path):
                config['htdocs_path'] = new_path
                save_config(config)
                print("[OK] Da cap nhat!")
            else:
                print("[X] Duong dan khong hop le!")
        elif choice == '3':
            new_path = input("Nhap duong dan hosts file moi: ").strip()
            if new_path:
                config['hosts_file'] = new_path
                save_config(config)
                print("[OK] Da cap nhat!")
            else:
                print("[X] Duong dan khong hop le!")
        elif choice == '4':
            new_path = input("Nhap duong dan Apache moi: ").strip()
            if new_path:
                config['apache_path'] = new_path
                save_config(config)
                print("[OK] Da cap nhat!")
            else:
                print("[X] Duong dan khong hop le!")
        elif choice == '5':
            editor = input("Chon editor (code/cursor): ").strip().lower()
            if editor in ['code', 'cursor']:
                config['default_editor'] = editor
                save_config(config)
                print("[OK] Da cap nhat!")
            else:
                print("[X] Editor khong hop le!")
        else:
            print("[X] Lua chon khong hop le!")


def main():
    """Hàm chính của tool"""
    print_header()
    
    config = load_config()
    xampp_path = config.get('xampp_path', '')
    htdocs_path = config.get('htdocs_path', '')
    hosts_file = config.get('hosts_file', r"C:\Windows\System32\drivers\etc\hosts")
    default_editor = config.get('default_editor', 'code')
    
    while True:
        projects = list_projects(htdocs_path) if htdocs_path and os.path.exists(htdocs_path) else []
        
        print("\n" + "=" * 60)
        print("  DANH SACH DU AN")
        print("=" * 60)
        
        if projects:
            for idx, project in enumerate(projects, start=1):
                project_path = os.path.join(htdocs_path, project)
                print(f"{idx}. {project}")
        else:
            print("\n[!] Chua co du an nao hoac khong tim thay thu muc htdocs")
        
        print("\n" + "-" * 60)
        print("QUAN LY DU AN:")
        print("  [so]      - Mo du an trong editor")
        print("  o [so]    - Mo du an (chon editor)")
        print("  c          - Clone du an moi")
        print("  d [so]     - Xoa du an")
        print("  r [so]     - Doi ten du an")
        print("\nQUAN LY HOSTS:")
        print("  h          - Xem danh sach hosts")
        print("  ha         - Them host moi")
        print("  hd [domain]- Xoa host")
        print("  he [domain]- Sua host")
        print("\nPHP & XAMPP:")
        print("  php        - Xem/chuyen doi PHP version")
        print("  rx         - Restart XAMPP")
        print("  ra         - Restart Apache")
        print("\nKHAC:")
        print("  s          - Cai dat")
        print("  0          - Thoat")
        print("=" * 60)
        
        choice = input("\nChon lenh: ").strip().lower()
        
        if choice == '0':
            print("\n[*] Thoat tool")
            break
        
        elif choice == 's':
            show_settings_menu(config)
            config = load_config()  # Reload config sau khi thay đổi
        
        elif choice == 'c':
            print("\n" + "=" * 60)
            print("  CLONE DU AN MOI")
            print("=" * 60)
            source = input("\nNhap Git repository URL: ").strip()
            if source:
                project_name = input("Nhap ten du an: ").strip()
                if project_name:
                    clone_project(source, project_name, htdocs_path)
                else:
                    print("[X] Ten du an khong duoc de trong!")
            else:
                print("[X] URL khong hop le!")
        
        elif choice.startswith('d '):
            project_idx = choice.replace('d ', '').strip()
            try:
                idx = int(project_idx)
                if 1 <= idx <= len(projects):
                    delete_project(projects[idx - 1], htdocs_path)
                else:
                    print("[X] So thu tu khong hop le!")
            except ValueError:
                print("[X] Vui long nhap so hop le!")
        
        elif choice.startswith('r '):
            project_idx = choice.replace('r ', '').strip()
            try:
                idx = int(project_idx)
                if 1 <= idx <= len(projects):
                    old_name = projects[idx - 1]
                    new_name = input(f"Nhap ten moi cho '{old_name}': ").strip()
                    if new_name:
                        rename_project(old_name, new_name, htdocs_path)
                    else:
                        print("[X] Ten moi khong duoc de trong!")
                else:
                    print("[X] So thu tu khong hop le!")
            except ValueError:
                print("[X] Vui long nhap so hop le!")
        
        elif choice.startswith('o '):
            project_idx = choice.replace('o ', '').strip()
            try:
                idx = int(project_idx)
                if 1 <= idx <= len(projects):
                    project_name = projects[idx - 1]
                    project_path = os.path.join(htdocs_path, project_name)
                    editor = input("Chon editor (code/cursor) [Enter=mac dinh]: ").strip().lower()
                    if not editor or editor not in ['code', 'cursor']:
                        editor = default_editor
                    open_project_in_editor(project_path, editor)
                else:
                    print("[X] So thu tu khong hop le!")
            except ValueError:
                print("[X] Vui long nhap so hop le!")
        
        elif choice == 'h':
            list_hosts(hosts_file)
            input("\nNhan Enter de quay lai...")
        
        elif choice == 'ha':
            print("\n" + "=" * 60)
            print("  THEM HOST MOI")
            print("=" * 60)
            domain = input("\nNhap domain (vd: mysite.local): ").strip()
            if domain:
                ip = input("Nhap IP (Enter = 127.0.0.1): ").strip() or '127.0.0.1'
                add_host_entry(domain, ip, hosts_file)
            else:
                print("[X] Domain khong duoc de trong!")
        
        elif choice.startswith('hd '):
            domain = choice.replace('hd ', '').strip()
            if domain:
                delete_host_entry(domain, hosts_file)
            else:
                print("[X] Vui long nhap domain can xoa!")
        
        elif choice.startswith('he '):
            domain = choice.replace('he ', '').strip()
            if domain:
                print("\n" + "=" * 60)
                print("  SUA HOST")
                print("=" * 60)
                new_domain = input(f"Domain moi (Enter = giu nguyen '{domain}'): ").strip() or None
                new_ip = input("IP moi (Enter = giu nguyen): ").strip() or None
                if new_domain or new_ip:
                    edit_host_entry(domain, new_domain, new_ip, hosts_file)
                else:
                    print("[X] Can thay doi it nhat 1 truong!")
            else:
                print("[X] Vui long nhap domain can sua!")
        
        elif choice == 'php':
            print("\n" + "=" * 60)
            print("  QUAN LY PHP VERSION")
            print("=" * 60)
            versions = get_php_versions(xampp_path)
            
            if versions:
                # Hiển thị version hiện tại nếu có
                current_version = get_current_php_version(xampp_path)
                if current_version:
                    print(f"\n[i] PHP version hien tai: {current_version}")
                
                print("\nDanh sach PHP version co san:")
                for idx, version in enumerate(versions, start=1):
                    marker = " <-- dang su dung" if version == current_version else ""
                    print(f"{idx}. {version}{marker}")
                
                print("\n" + "-" * 60)
                print("Lenh:")
                print("  [so/ten]  - Chuyen doi PHP version")
                print("  add       - Huong dan them PHP version moi")
                print("  check     - Kiem tra cac PHP version")
                print("  Enter     - Quay lai")
                print("-" * 60)
                
                version_choice = input("\nChon lenh: ").strip().lower()
                
                if version_choice == 'add':
                    show_add_php_version_guide(xampp_path)
                    continue
                elif version_choice == 'check':
                    print("\n" + "=" * 60)
                    print("  KIEM TRA PHP VERSIONS")
                    print("=" * 60)
                    php_dir = os.path.join(xampp_path, 'php')
                    
                    for version in versions:
                        version_path = os.path.join(php_dir, version)
                        checks = verify_php_version(version_path)
                        
                        print(f"\n📦 {version}:")
                        status = "✅" if checks['valid'] else "❌"
                        print(f"   {status} php.exe: {'Co' if checks['php_exe'] else 'Thieu'}")
                        print(f"   {status} PHP DLL: {'Co' if checks['php_dll'] else 'Thieu'}")
                        print(f"   {'✅' if checks['php_ini'] else '⚠️ '} php.ini: {'Co' if checks['php_ini'] else 'Thieu'}")
                        
                        if checks['valid']:
                            try:
                                php_exe = os.path.join(version_path, 'php.exe')
                                result = subprocess.run(
                                    [php_exe, '-v'],
                                    capture_output=True,
                                    text=True,
                                    timeout=5
                                )
                                if result.returncode == 0:
                                    first_line = result.stdout.split('\n')[0] if result.stdout else ''
                                    if first_line:
                                        print(f"   📝 {first_line.strip()}")
                            except Exception:
                                pass
                    
                    input("\nNhan Enter de quay lai...")
                    continue
                elif version_choice:
                    selected_version = None
                    
                    # Thử nhập là số thứ tự
                    try:
                        idx = int(version_choice)
                        if 1 <= idx <= len(versions):
                            selected_version = versions[idx - 1]
                        else:
                            print("[X] So thu tu khong hop le!")
                            continue
                    except ValueError:
                        # Không phải số, thử tìm theo tên version
                        version_choice_lower = version_choice.lower()
                        for version in versions:
                            if version.lower() == version_choice_lower or version_choice_lower in version.lower():
                                selected_version = version
                                break
                        
                        if not selected_version:
                            print(f"[X] Khong tim thay PHP version: {version_choice}")
                            print("[i] Vui long nhap so thu tu hoac ten version chinh xac")
                            continue
                    
                    # Thực hiện chuyển đổi
                    if selected_version:
                        if selected_version == current_version:
                            print(f"\n[i] PHP version '{selected_version}' dang duoc su dung!")
                        else:
                            switch_php_version(selected_version, xampp_path)
            else:
                print("\n[!] Khong tim thay PHP version nao!")
                print(f"    Duong dan XAMPP: {xampp_path}")
                print(f"    Kiem tra thu muc: {os.path.join(xampp_path, 'php')}")
                
                add_choice = input("\nBan co muon xem huong dan them PHP version? (y/N): ").strip().lower()
                if add_choice == 'y':
                    show_add_php_version_guide(xampp_path)
        
        elif choice == 'rx':
            restart_xampp(xampp_path)
        
        elif choice == 'ra':
            restart_apache(xampp_path)
        
        else:
            # Thử chọn số để mở dự án
            try:
                idx = int(choice)
                if 1 <= idx <= len(projects):
                    project_name = projects[idx - 1]
                    project_path = os.path.join(htdocs_path, project_name)
                    open_project_in_editor(project_path, default_editor)
                else:
                    print("[X] So thu tu khong hop le!")
            except ValueError:
                print("[X] Lenh khong hop le!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[X] Da huy!")
    except Exception as e:
        print(f"\n[X] Loi: {e}")
        import traceback
        traceback.print_exc()

