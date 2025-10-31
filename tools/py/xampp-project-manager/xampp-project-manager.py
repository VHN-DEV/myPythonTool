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


def switch_php_version(version: str, xampp_path: str):
    """Chuyển đổi phiên bản PHP"""
    php_dir = os.path.join(xampp_path, 'php')
    target_php_path = os.path.join(php_dir, version, 'php.exe')
    
    if not os.path.exists(target_php_path):
        print(f"[X] Khong tim thay PHP version: {version}")
        return False
    
    # Tạo symlink hoặc copy php.exe (tùy vào XAMPP version)
    # Trên XAMPP, thường cần chỉnh sửa httpd.conf
    print(f"[>] Dang chuyen doi PHP version: {version}")
    print("[!] Can chinh sua thu cong file httpd.conf")
    print(f"    Tim dong 'LoadModule php_module' va sua duong dan:")
    print(f"    LoadModule php_module \"{target_php_path.replace('php.exe', 'php7apache2_4.dll')}\"")
    print(f"    PHPIniDir \"{os.path.join(php_dir, version)}\"")
    
    return True


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
                print("\nDanh sach PHP version:")
                for idx, version in enumerate(versions, start=1):
                    print(f"{idx}. {version}")
                
                version_choice = input("\nChon version de chuyen doi (so) hoac Enter de huy: ").strip()
                if version_choice:
                    try:
                        idx = int(version_choice)
                        if 1 <= idx <= len(versions):
                            switch_php_version(versions[idx - 1], xampp_path)
                        else:
                            print("[X] So thu tu khong hop le!")
                    except ValueError:
                        print("[X] Vui long nhap so hop le!")
            else:
                print("\n[!] Khong tim thay PHP version nao!")
                print(f"    Duong dan XAMPP: {xampp_path}")
        
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

