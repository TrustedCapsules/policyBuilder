import crypto

import pytest

from backend import keyserver



def test_crypto():
    pubkey = open("backend_tests/demo_rsakey_pem.pub", "r").read()
    msg = "I met aliens in UFO. Here is the map.".encode("utf-8")
    encrypted = crypto.encrypt_rsa(msg, pubkey)
    # print(encrypted)

    privkey = open("backend_tests/demo_rsakey", "r").read()
    decrypted = crypto.decrypt_rsa(encrypted, privkey)
    assert msg == decrypted
    # print(decrypted)
