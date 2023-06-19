import socket as sk
import threading

from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad

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
connected_clients = {}

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


def decrypt(ciphertext, key):
    key = bytes.fromhex(key)
    cipher = DES.new(key, DES.MODE_ECB)
    ciphertext = bytes.fromhex(ciphertext)
    plaintext = cipher.decrypt(ciphertext)
    plaintext = unpad(plaintext, 8).decode('utf-8')
    return plaintext

# set giới hạn server
server.listen(LISTENER_LIMIT)

# hàm gửi tin nhắn tới một client nhất định
def send_msg_to_client(client_username, message):
    if client_username in connected_clients:
        client_socket = connected_clients[client_username]['socket']
        client_socket.send(message.encode('utf-8'))


# Khi server cần biết danh sách các client đang kết nối tới, truy xuất tất cả các key của connected_clients và trả về danh sách các username
def get_connected_clients():
    return list(connected_clients.keys())

# tạo hàm kiểm soát và gửi các tin nhắn tới các client
def client_handle(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
            encrypted_msg, key ,send_hash = message.split("::")
            msg_decrypt = decrypt(encrypted_msg,key)
            msg_sd, key, msg_str, receiver = msg_decrypt.split("::")
            receiver = decrypt(receiver,key)
            print(f"{nicknames[clients.index(client)]}: {message}")

            # Gửi tin nhắn đến người nhận
            send_msg_to_client(receiver, message)

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            # Xóa thông tin của client khỏi connected_clients
            if nickname in connected_clients:
                del connected_clients[nickname]
            break

def send_msg_to_client(receiver, message):
    # Tìm client của người nhận
    receiver_client = None
    for client in clients:
        if nicknames[clients.index(client)] == receiver:
            receiver_client = client
            break

    # Nếu không tìm thấy client của người nhận, báo lỗi
    if receiver_client is None:
        print(f"Error: {receiver} is not connected.")
        return

    # Gửi tin nhắn tới người nhận
    try:
        receiver_client.send(message.encode('utf-8'))
    except:
        print(f"Error sending message to {receiver}.")
