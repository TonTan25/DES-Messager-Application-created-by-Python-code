from Crypto.Cipher import DES
from secrets import token_bytes

key = token_bytes(8)
print(f"khóa được tạo ra: {key}\nkháo dưới dạng hexa: {key.hex()}\n")
cipher = DES.new(key, DES.MODE_ECB)  # sử dụng chế độ mã hóa ECB
plaintext = 'Tin nhan bi mat' 
ciphertext = cipher.encrypt(plaintext.encode())
deciphertext = cipher.decrypt(ciphertext.decode())

print(f"Tin nhắn được mã hóa : {ciphertext}")
print(f"Tin nhắn được giải mã : {deciphertext}")

