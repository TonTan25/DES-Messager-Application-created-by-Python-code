import hashlib

def md5_hash(string):
    """
    Tạo mã băm MD5 cho chuỗi ký tự đầu vào.
    """
    # Chuyển đổi chuỗi thành dạng byte trước khi băm
    byte_string = string.encode('utf-8')
    # Tạo đối tượng băm MD5
    hash_object = hashlib.md5(byte_string)
    # Trả về giá trị băm dưới dạng chuỗi hex
    return hash_object.hexdigest()

