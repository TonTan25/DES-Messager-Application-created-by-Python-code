import tkinter as tk
import socket
import threading
import base64
from tkinter import messagebox, simpledialog
from tkinter import *
from PIL import Image, ImageTk
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes


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
        self.win.iconbitmap("./img/icon.ico")
        self.win.resizable(width=False, height=False)
        self.win.configure(width=500, height=650)

        load_bg = Image.open("./img/Bg_1.png")
        img_bg = ImageTk.PhotoImage(load_bg)
        img = Label(self.win, image=img_bg)
        img.place(x=0, y=0)

        name_sys = Label(self.win, text=f"[{self.nickname}]", fg="#000000", bd=0, bg="#DFFFFF")
        name_sys.config(font=("Times New Roman", 20, "bold"))
        name_sys.place(y=10, x=10)

        name_sys = Label(self.win, text="DES Message", fg="#000000", bd=0, bg="#DFFFFF")
        name_sys.config(font=("Bookman Old Style", 25, "bold"))
        name_sys.place(y=10, x=155)

        self.chat_box = Text(self.win, width=43, height=21, font=("Arial", 14), bd=1, bg="#FAFAFA")
        self.chat_box.place(y=65, x=11)
        self.chat_box.config(state=DISABLED)

        self.send_box = Text(self.win, width=35, height=4, font=("Arial", 14), bd=1, bg="#FAFAFA")
        self.send_box.place(y=540, x=11)
        self.send_box.bind("<Return>", lambda x: self.send_msg())

        send_bg = Image.open("./img/sendbtn.png")
        send = ImageTk.PhotoImage(send_bg)
        sendbtn = Button(self.win, bg="#DFFFFF", bd=0, image=send, width=75, height=75, command=self.send_msg)
        sendbtn.place(y=547, x=410)

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
    

    def send_msg(self):
        # Generate a random key
        key = get_random_bytes(8)
        
        # Create a DES cipher object
        cipher = DES.new(key, DES.MODE_ECB)
        
        # Get the message from the send_box and pad it
        message = self.send_box.get("1.0", "end-1c")
        padded_message = self.pad(message)
        
        # Encrypt the padded message and convert to hexadecimal
        ciphertext = cipher.encrypt(padded_message.encode("utf-8"))
        encrypted_msg = ciphertext.hex()
        
        # Encode the message with nickname, key, and encrypted message
        msg = f"{self.nickname}::{key.hex()}::{encrypted_msg}"
        
        # Send the message to the server
        self.sock.send(msg.encode("utf-8"))
        
        # stop cipher
        self.cipher = None
        # Clear the send_box
        self.send_box.delete("1.0", "end")


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
                        nickname, key, encrypted_msg = message.split("::")
                        decrypted_msg = self.decrypt(encrypted_msg, key)
                        self.cipher = None
                        # Hiển thị tin nhắn
                        self.chat_box.config(state=tk.NORMAL)
                        self.chat_box.insert(tk.END,f"{nickname}: {decrypted_msg}\n" )
                        self.chat_box.config(state=tk.DISABLED)
                        self.chat_box.yview(tk.END)
            except Exception as e:
                print("[EXCEPTION]", e)
                break
            except :
                print("Đã xảy ra lỗi!!")
                self.sock.close()
                break


if __name__ == "__main__":
    client = Client(HOST,PORT)