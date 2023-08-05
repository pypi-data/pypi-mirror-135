from Crypto.Cipher import AES
from binascii import b2a_base64, a2b_base64

def rpad(text, divisor: int, suffix):
    remain = len(text) % divisor
    if remain > 0:
        text += suffix * (divisor - remain)
    return text

def encrypt(text, salt, key):
    fmtkey, fmtiv = map(lambda s: s.encode()[:16].ljust(16, b'\0'), (key, salt))
    cryptor = AES.new(fmtkey, AES.MODE_CBC, fmtiv)
    fmttext = rpad(text.encode(), 16, b'\0')
    ciphertext = cryptor.encrypt(fmttext)
    return str(b2a_base64(ciphertext))[2:-3].rstrip('=')

def decrypt(text, salt="resset", key= "hello"):
    fmtkey, fmtiv = map(lambda s: s.encode()[:16].ljust(16, b'\0'), (key, salt))
    cryptor = AES.new(fmtkey, AES.MODE_CBC, fmtiv)
    fmttext = rpad(text, 4, '=')
    return cryptor.decrypt(a2b_base64(fmttext)).rstrip(b'\0').decode()

if __name__ == "__main__":
    print(decrypt('BV4L6rzB5zITUPK+IeApvkXu++2pLno6nj3cXSPKyha1t+vkWeZ5VGBdNb5KpnGtVKHMl/Tq73EqPtWA5AnPIg'))
    # key,salt应为16字节(汉字3字节，字母1字节)，不足的自动补空格，超过的取前16字节
    ciphertext = encrypt('mssql+pymssql://lixinapi:lixinapi@192.168.1.38:14333/JYDB', "lixinapi", "hello")
    print(ciphertext)
    plaintext = decrypt(ciphertext, "lixinapi", "hello")
    print(plaintext)