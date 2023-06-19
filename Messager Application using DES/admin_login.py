import random
import sqlite3
import json
from PyQt5.QtWidgets import QApplication, QInputDialog
# Kết nối đến cơ sở dữ liệu
conn = sqlite3.connect('HumanID.db')
cursor = conn.cursor()

# Tạo bảng để lưu trữ thông tin người dùng
# cursor.execute('''CREATE TABLE IF NOT EXISTS users
# (username TEXT PRIMARY KEY, id INT, num_failed_logins INT DEFAULT 0, login_status VARCHAR(10) DEFAULT 'pending')''')

# Thêm dữ liệu mẫu cho bảng users
# cursor.execute("INSERT INTO users (username, id) VALUES ('beKien', 654321)")
# cursor.execute("INSERT INTO users (username, id) VALUES ('beMinh', 123456)")
# cursor.execute("INSERT INTO users (username, id) VALUES ('jane', 789012)")
# cursor.execute("INSERT INTO users (username, id) VALUES ('doe', 345678)")

app = QApplication([])
username, ok_pressed = QInputDialog.getText(None, "Tên người gửi" , "Nhập tên đăng nhập:")
if ok_pressed:
    id, ok_pressed = QInputDialog.getText(None, "Mã định " + username, "Nhập mã định danh:")
    if ok_pressed:
        if username == "admin" and id == "101010":
            # Lấy toàn bộ thông tin người dùng từ database
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            user_data = []
            for user in users:
                # Thêm thông tin của từng người dùng vào list user_data
                user_data.append({
                    "username": user[0],
                    "id": user[1],
                    "num_failed_logins": user[2],
                    "login_status": user[3]
                })
            # Lưu thông tin người dùng vào file JSON
            with open('users.json', 'w') as f:
                f.write('[\n{"username": "admin", "id": 101010, "num_failed_logins": 0, "login_status": "success"}')
                for user in user_data:
                    f.write(',\n')
                    json.dump(user, f)
                f.write('\n]')
            # In danh sách người dùng
            print("Danh sách người dùng:")
            for user in user_data:
                print(user["username"], user["id"])


        # kiểm tra tài khoản có đăng nhập được không ! 
        else:
            # Kiểm tra thông tin đăng nhập của người dùng
            cursor.execute("SELECT id, login_status FROM users WHERE username=?", (username,))
            user = cursor.fetchone()
            if user is None:
                # Thêm người dùng mới với ID mới nếu tên đăng nhập không tồn tại trong database
                new_user_id = random.randint(100000, 999999)
                cursor.execute("INSERT INTO users (username, id, num_failed_logins, login_status) VALUES (?, ?, 0, 'success')", (username, new_user_id))
                print("Tài khoản mới đã được tạo với mã định danh:", new_user_id)
            elif user[1] == "failed":
                print("Tài khoản của bạn đã bị khóa do nhập sai quá số lần cho phép")
            elif int(id) == user[0]:
                print("Đăng nhập thành công")
                cursor.execute("UPDATE users SET num_failed_logins = 0, login_status = 'success' WHERE username=?", (username,))
            else:
                print("Mã định danh không đúng")
                cursor.execute("UPDATE users SET num_failed_logins = num_failed_logins + 1 WHERE username=?", (username,))
                cursor.execute("SELECT num_failed_logins FROM users WHERE username = ?", (username,))
                num_failed_logins = cursor.fetchone()[0]
                if num_failed_logins >= 3:
                    # Nếu người dùng nhập sai quá 3 lần, đặt login_status của người dùng thành 'failed' và cấp lại mã định danh mới
                    cursor.execute("UPDATE users SET login_status = 'failed' WHERE username=?", (username,))
                    new_user_id = random.randint(100000, 999999)
                    cursor.execute("UPDATE users SET id = ?, num_failed_logins = 0, login_status = 'failed' WHERE username=?", (new_user_id, username))
                    print("Bạn đã nhập sai quá số lần cho phép, vui lòng nhập lại tên đăng nhập và mã định danh mới")


# Lưu các thay đổi vào cơ sở dữ liệu và đóng kết nối
conn.commit()
conn.close()
