from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

class DES_RSA:
    def Create_RSA():
        # Tạo một đối tượng key RSA với độ dài key là 2048 bits
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        # Lấy khóa công khai từ khóa RSA
        public_key = key.public_key()

        # Serialize khóa RSA để lưu trữ hoặc truyền qua mạng
        private_key_pem = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # In khóa để kiểm tra
        print(private_key_pem.decode('utf-8'))
        print(public_key_pem.decode('utf-8'))
        return private_key_pem.decode('utf-8'),public_key_pem.decode('utf-8')