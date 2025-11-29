import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def decrypt_token(encrypted_data, encryption_key):
    clean_key = encryption_key.strip()
    key = hashlib.sha256(clean_key.encode()).digest()
    
    parts = encrypted_data.split(':')
    iv_hex = parts[0]
    encrypted = parts[1]
    
    iv = bytes.fromhex(iv_hex)
    encrypted_bytes = bytes.fromhex(encrypted)
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
    
    return decrypted.decode('utf-8')
