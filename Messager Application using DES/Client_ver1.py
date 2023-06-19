import tkinter as tk
import socket
import threading
import json
from tkinter import messagebox, simpledialog
from tkinter import *
from PIL import Image, ImageTk
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from hash import md5_hash

def get_server_ip():
    # Lấy tên máy chủ
    hostname = socket.gethostname()
    # Lấy địa chỉ IP của máy chủ
    ip_address = socket.gethostbyname(hostname)
    return ip_address

HOST = get_server_ip()
PORT = 8080  # post có thể nằm trong 0 tới 65535

class Client:
    def __init__(self, host, port):
        self.nickname = None
        self.key = None
        self.nickname = simpledialog.askstring("Tên đăng nhập", "Vui lòng điền tên sử dụng bạn")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host,port))
        self.gui_done = False
        self.running = True
        gui_thread = threading.Thread(target=self.GUI)
        receive_thread = threading.Thread(target=self.receive)
        gui_thread.start()
        receive_thread.start()


    def GUI(self):
        self.win = tk.Tk()
        self.win.title("DES MESSAGE ")

        # Lấy kích thước màn hình
        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()

        # Tính toán kích thước cửa sổ và vị trí để hiển thị giữa màn hình
        window_width = 500
        window_height = 700

        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)

        # Đặt kích thước và vị trí cho cửa sổ
        self.win.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.win.iconbitmap("./img/icon.ico")
        self.win.resizable(width=False, height=False)
        self.win.configure(width=500, height=700)

        load_bg = Image.open("./img/Bg_1.png")
        img_bg = ImageTk.PhotoImage(load_bg)
        img = Label(self.win, image=img_bg)
        img.place(x=0, y=0)

        name_sys = Label(self.win, text=f"[{self.nickname}]", fg="#000000", bd=0, bg="#DFFFFF")
        name_sys.config(font=("Times New Roman", 20, "bold"))
        name_sys.place(y=11, x=11)

        name_sys = Label(self.win, text="DES Message", fg="#000000", bd=0, bg="#DFFFFF")
        name_sys.config(font=("Bookman Old Style", 25, "bold"))
        name_sys.place(y=11, x=250)

        self.chat_box = Text(self.win, width=43, height=21, font=("Arial", 14), bd=1, bg="#FAFAFA")
        self.chat_box.place(y=65, x=11)
        self.chat_box.config(state=DISABLED)

        self.lable_reciver = Label(self.win, text=f"Send to :", fg="#000000", bd=0, bg="#DFFFFF")
        self.lable_reciver.config(font=("Times New Roman", 15, "bold"))
        self.lable_reciver.place(y=545, x=11)

        self.name_reciver = Text(self.win, width=20, height=1, font=("Arial", 14), bd=0, bg="#FAFAFA")
        self.name_reciver.place(y=545, x=100)

        self.send_box = Text(self.win, width=35, height=4, font=("Arial", 14), bd=1, bg="#FAFAFA")
        self.send_box.place(y=580, x=11)
        self.send_box.bind("<Return>", lambda x: self.send_msg())

        send_bg = Image.open("./img/sendbtn.png")
        send = ImageTk.PhotoImage(send_bg)
        sendbtn = Button(self.win, bg="#DFFFFF", bd=0, image=send, width=75, height=75, command=self.send_msg)
        sendbtn.place(y=586, x=410)

        self.gui_done = True
        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()


    def encrypt(self, plaintext, key):
        # Tạo đối tượng DES cipher với khóa key
        self.cipher = DES.new(key, DES.MODE_ECB)
        plaintext = self.pad(plaintext)
        ciphertext = self.cipher.encrypt(plaintext.encode('utf-8'))
        return ciphertext.hex()

    def decrypt(self, ciphertext, key):
        key = bytes.fromhex(key)
        self.cipher = DES.new(key, DES.MODE_ECB)
        ciphertext = bytes.fromhex(ciphertext)
        plaintext = self.cipher.decrypt(ciphertext).decode('utf-8')
        plaintext = self.unpad(plaintext)
        return plaintext

    def pad(self, s):
        bs = DES.block_size
        return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

    def unpad(self, s):
        return s[:-ord(s[len(s)-1:])] 
    
    def find_user_in_list(self, receiver):
        with open('users.json', 'r') as f:
            user_data = json.load(f)
            found_user = None
            found_id = ""
            founded = False
            for user in user_data:
                if user['username'] == receiver:
                    found_user = user['username']
                    found_id = user['id']
                    print(found_user, found_id)
                    founded = True
                    break
            return found_user, found_id, founded



    def send_msg(self):
        # Generate a random key
        key = get_random_bytes(8)
        
        # Create a DES cipher object
        cipher = DES.new(key, DES.MODE_ECB)
        
        # Get the message from the send_box and pad it
        message = self.send_box.get("1.0", tk.END)
        reciver = self.name_reciver.get("1.0", tk.END).strip()
        padded_message = self.pad(message)
        padded_reciver = self.pad(reciver)

        # Tìm kiếm người dùng trong danh sách
        found_user, found_id, founded = self.find_user_in_list(reciver)
        # print(found_user, found_id)
        # Xử lý và hiển thị thông báo
        if founded == True:
            # messagebox.showinfo("Thông báo", "Đã gửi tin nhắn thành công!")
            # Encrypt the padded message, reciver, sender and convert to hexadecimal
            sender = f"{self.nickname}"
            padded_sender = self.pad(sender)
            cipher_sender = cipher.encrypt(padded_sender.encode("utf-8"))
            sender = cipher_sender.hex()
            cipher_message = cipher.encrypt(padded_message.encode("utf-8"))
            encrypted_msg = cipher_message.hex()
            cipher_reciver = cipher.encrypt(padded_reciver.encode("utf-8"))
            encrypted_reciver = cipher_reciver.hex()
            
            # Encode the message with nickname, key, and encrypted message
            msg = f"{sender}::{key.hex()}::{encrypted_msg}::{encrypted_reciver}"
            msg_DES_2 = self.pad(msg)
            msg_DES_2 = cipher.encrypt(msg_DES_2.encode('utf-8'))
            msg_2 = msg_DES_2.hex()
            msg_hash = md5_hash(msg)
            msg = f"{msg_2}::{key.hex()}::{msg_hash}"
            # Send the message to the server
            self.sock.send(msg.encode("utf-8"))
            
            # stop cipher
            self.cipher = None

            # Clear the send_box
            self.send_box.delete("1.0", "end")

        elif founded == False:
            messagebox.showerror("Lỗi", f"Không tìm thấy người dùng {reciver}!")
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")

    def stop(self):
        if messagebox.showwarning("THOÁT ỨNG DỤNG","Bạn có chắc chắn là muốn thoát ?") :
            # self.sock.sendall(f"{self.nickname} Đã ngắt kết nối !".encode('utf-8'))
            self.running = False
            self.win.destroy()
            self.sock.close()
            exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                print(message)
                if message == 'Neon':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        # Giải mã tin nhắn bằng DES
                        encrypted_msg, key, send_hash = message.split("::")
                        msg_decrypt = self.decrypt(encrypted_msg,key)
                        encrypted_sender, key, encrypted_msg, encrypted_reciver = msg_decrypt.split("::")
                        check_hash = md5_hash(f"{encrypted_sender}::{key}::{encrypted_msg}::{encrypted_reciver}")
                        if check_hash == send_hash :
                            print('Tin nhắn đã chứng thực')
                            sender = self.decrypt(encrypted_sender, key)
                            decrypted_msg = self.decrypt(encrypted_msg, key)
                            decrypted_reciver = self.decrypt(encrypted_reciver, key)
                            self.cipher = None
                            # Hiển thị tin nhắn
                            self.chat_box.config(state=tk.NORMAL)
                            self.chat_box.insert(tk.END,f"{sender} send to {decrypted_reciver}:\n{decrypted_msg}\n" )
                            self.chat_box.config(state=tk.DISABLED)
                            self.chat_box.yview(tk.END)
                        else:
                            print(check_hash)
                            print('Tin nhắn đã bị thay đổi')
            except Exception as e:
                print("[EXCEPTION]", e)
                break
            except :
                print("Đã xảy ra lỗi!!")
                self.sock.close()
                break


if __name__ == "__main__":
    client = Client(HOST,PORT)