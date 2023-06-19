import socket

def get_server_ip():
    # Lấy tên máy chủ
    hostname = socket.gethostname()
    # Lấy địa chỉ IP của máy chủ
    ip_address = socket.gethostbyname(hostname)
    return ip_address
print(get_server_ip())
