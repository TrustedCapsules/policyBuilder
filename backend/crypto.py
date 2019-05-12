from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA


# Encrypts @unencrypted_msg with @pub_key
def encrypt_rsa(unencrypted_msg: bytes, pub_key: str) -> bytes:
    public_key = RSA.importKey(pub_key)
    cipher_rsa = PKCS1_OAEP.new(public_key)
    return cipher_rsa.encrypt(unencrypted_msg)


# Decrypts @encrypted_msg with @priv_key
def decrypt_rsa(encrypted_msg: bytes, priv_key: str) -> bytes:
    private_key = RSA.importKey(priv_key)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    return cipher_rsa.decrypt(encrypted_msg)

