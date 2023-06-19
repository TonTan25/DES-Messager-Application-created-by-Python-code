import socket as sk
import threading

def get_server_ip():
    # Lấy tên máy chủ
    hostname = sk.gethostname()
    # Lấy địa chỉ IP của máy chủ
    ip_address = sk.gethostbyname(hostname)
    return ip_address

HOST = get_server_ip()
PORT = 8080  # port có thể nằm trong 0 tới 65535

clients = []
nicknames = []

LISTENER_LIMIT = 10
active_client = [] # danh sách người dùng hiện tại  

# tạo socket server class obj
# AF_INET sử dụng địa chỉ IPv4
# SOCK_STREAM sử dụng TPC packets
server = sk.socket(sk.AF_INET,sk.SOCK_STREAM)
# tạo họp try - catch
try:
    server.bind((HOST,PORT))
    print(f"server đã hoạt động : {HOST} | {PORT}")
except:
    print(f"không thể kết nối tới {HOST} | {PORT}")

# set giới hạn server
server.listen(LISTENER_LIMIT)

# tạo hàm kiểm soát và gửi các tin nhắn tới các client
def client_handle(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(f"{message}")
            send_msg_to_all(message.encode('utf-8'))
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

# tạo hàm gửi tin nhắn tới mọi người trong client 
def send_msg_to_all(message):
   for client in clients:
       client.send(message)

# hàm nhận tin nhắn từ client
def listen_msg_from_client():
    while True:
        client, address = server.accept()
        print(f"Đã kết nối với {str(address)}")

        client.send("Neon".encode('utf-8'))
        nickname = client.recv(1024)

        nicknames.append(nickname)
        clients.append(client)

        print(f"Tên người dùng là {nickname}")
        send_msg_to_all(f"{nickname} đã kết nối đến server!\n".encode('utf-8'))
        client.send("đã kết nối tới server".encode('utf-8'))

        threading.Thread(target=client_handle, args=(client, )).start()

print("server đang chạy ... ")
listen_msg_from_client()
