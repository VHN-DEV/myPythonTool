import subprocess

# Danh sách server cấu hình sẵn
servers = [
    {
        "name": "Server DEV",
        "user": "dev",
        "host": "192.168.10.163",
        "port": 1506,
        "password": None,  # Nếu có password thì điền vào đây, nếu dùng ssh key thì để None
        "ssh_key": None    # Nếu dùng key thì ghi đường dẫn, ví dụ: r"D:\IT\key\id_rsa"
    },
    {
        "name": "Server TEST",
        "user": "test",
        "host": "192.168.10.200",
        "port": 22,
        "password": "your_password_here",
        "ssh_key": None
    },
    {
        "name": "Server PROD (key)",
        "user": "prod",
        "host": "192.168.10.250",
        "port": 22,
        "password": None,
        "ssh_key": r"D:\IT\keys\prod_id_rsa"
    }
]

def connect_server(server):
    if server["ssh_key"]:  
        # Kết nối bằng ssh key
        cmd = [
            "ssh",
            "-i", server["ssh_key"],
            f"{server['user']}@{server['host']}",
            "-p", str(server["port"])
        ]
        subprocess.run(cmd)
    elif server["password"]:
        # Kết nối bằng password (yêu cầu cài sshpass trên Linux/Mac, Windows thì nhập tay)
        # Với Windows bạn thường phải nhập pass tay, sshpass không có sẵn
        print(f"Đang kết nối {server['name']} (yêu cầu nhập password thủ công nếu ssh không nhớ)...")
        cmd = [
            "ssh",
            f"{server['user']}@{server['host']}",
            "-p", str(server["port"])
        ]
        subprocess.run(cmd)
    else:
        # Mặc định SSH (sẽ hỏi password nếu cần)
        cmd = [
            "ssh",
            f"{server['user']}@{server['host']}",
            "-p", str(server["port"])
        ]
        subprocess.run(cmd)

def main():
    print("===== Danh sách SSH Server =====")
    for idx, server in enumerate(servers, start=1):
        print(f"{idx}. {server['name']} ({server['user']}@{server['host']}:{server['port']})")
    print("0. Thoát")

    try:
        choice = int(input("Chọn số để SSH: "))
        if choice == 0:
            print("Thoát.")
            return
        if 1 <= choice <= len(servers):
            connect_server(servers[choice - 1])
        else:
            print("Lựa chọn không hợp lệ.")
    except ValueError:
        print("Vui lòng nhập số.")

if __name__ == "__main__":
    main()
