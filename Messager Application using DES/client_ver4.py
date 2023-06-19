import tkinter as tk
from tkinter import messagebox


class ChatGUI:
    def __init__(self, username):
        self.username = username
        self.window = tk.Tk()
        self.window.title("Chat Client")

        # Lấy kích thước màn hình
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Tính toán kích thước cửa sổ và vị trí để hiển thị giữa màn hình
        window_width = 400
        window_height = 300
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)

        # Đặt kích thước và vị trí cho cửa sổ
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Tên người nhận
        to_label = tk.Label(self.window, text="Người nhận:")
        to_label.grid(row=0, column=0)
        self.to_entry = tk.Entry(self.window, width=30)
        self.to_entry.grid(row=0, column=1)

        # Tin nhắn đã gửi
        message_label = tk.Label(self.window, text="Tin nhắn đã gửi:")
        message_label.grid(row=1, column=0)
        self.message_text = tk.Text(self.window, height=10, width=50)
        self.message_text.grid(row=2, column=0, columnspan=2)

        # Thông báo
        self.status_label = tk.Label(self.window, text="")
        self.status_label.grid(row=3, column=0, columnspan=2)

        # Nút gửi
        send_button = tk.Button(self.window, text="Gửi", command=self.send_message)
        send_button.grid(row=4, column=1)

        # Gửi tin nhắn khi nhấn Enter
        self.window.bind('<Return>', lambda event: self.send_message())

        # Thông báo trước khi đóng chương trình
        self.window.protocol("WM_DELETE_WINDOW", self.on_exit)

    def send_message(self):
        # Lấy dữ liệu từ các widgets
        to = self.to_entry.get()
        message = self.message_text.get("1.0", tk.END)

        # Xử lý và hiển thị thông báo
        if to and message:
            self.status_label.config(text="Đã gửi tin nhắn đến " + to)
            self.message_text.delete("1.0", tk.END)
        else:
            self.status_label.config(text="Vui lòng nhập đầy đủ thông tin")

    def on_exit(self):
        # Hiển thị messagebox khi thoát
        if messagebox.askokcancel("Thoát", "Bạn có muốn thoát chương trình?"):
            self.window.destroy()

    def run(self):
        self.window.mainloop()


# Sử dụng
chat_gui = ChatGUI("Alice")
chat_gui.run()
