from Crypto.Cipher import DES
from secrets import token_bytes
class MyDES:
    def __init__(self, key):
        self.key = key
        self.cipher = DES.new(self.key, DES.MODE_ECB)

    def encrypt(self, plaintext):
        plaintext = self.pad(plaintext)
        ciphertext = self.cipher.encrypt(plaintext.encode('utf-8'))
        return ciphertext.hex()

    def decrypt(self, ciphertext):
        ciphertext = bytes.fromhex(ciphertext)
        plaintext = self.cipher.decrypt(ciphertext).decode('utf-8')
        plaintext = self.unpad(plaintext)
        return plaintext

    def pad(self, s):
        bs = DES.block_size
        return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

    def unpad(self, s):
        return s[:-ord(s[len(s)-1:])]


# Example usage
key = token_bytes(8)
print(key)
des = MyDES(key)

plaintext = 'Tin nhan bi mat'
ciphertext = des.encrypt(plaintext)
print(ciphertext)

decrypted_plaintext = des.decrypt(ciphertext)
print(decrypted_plaintext)

