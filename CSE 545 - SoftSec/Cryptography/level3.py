#!/opt/pwn.college/python

import sys
import os
import string
import random
import pathlib
import base64
import json
import textwrap
import hashlib
from PIL import Image

from Crypto.Cipher import AES
from Crypto.Hash.SHA256 import SHA256Hash
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Random.random import getrandbits, randrange
from Crypto.Math import Primality
from Crypto.Util.strxor import strxor
from Crypto.Util.Padding import pad, unpad


flag = open("/flag", "rb").read()
config = (pathlib.Path(__file__).parent / ".config").read_text()
level = int(config)


def show(name, value, *, b64=True):
    print(f"{name}: {value}")


def show_b64(name, value):
    show(f"{name} (b64)", base64.b64encode(value).decode())


def show_b32(name, value):
    show(f"{name} (b64)", base64.b32encode(value).decode())


def show_hex(name, value):
    show(name, hex(value))


def input_(name):
    try:
        return input(f"{name}: ")
    except (KeyboardInterrupt, EOFError):
        print()
        exit(0)


def input_b64(name):
    data = input_(f"{name} (b64)")
    try:
        return base64.b64decode(data)
    except base64.binascii.Error:
        print(f"Failed to decode base64 input: {data!r}", file=sys.stderr)
        exit(1)


def input_hex(name):
    data = input_(name)
    try:
        return int(data, 16)
    except Exception:
        print(f"Failed to decode hex input: {data!r}", file=sys.stderr)
        exit(1)


def level1():
    """
    In this challenge you will decode some Base64-encoded data.
    Despite Base64-encoded data appearing "mangled", it is not an encryption scheme.
    It is an encoding, much like base2, base10, base16, and ascii.
    It is a popular way of encoding raw bytes.
    """
    show_b64("flag", flag)


def level2():
    """
    In this challenge you will decode some Base32-encoded data.
    """
    show_b32("flag", flag)


def level3():
    """
    In this challenge you will decrypt a secret encrypted with a one-time pad.
    Although simple, this is the most secure encryption mechanism, if you could just securely transfer the key.
    """
    key = get_random_bytes(len(flag))
    ciphertext = strxor(flag, key)
    show_b64("key", key)
    show_b64("secret ciphertext", ciphertext)


def level4():
    """
    In this challenge you will decrypt a secret encrypted with a one-time pad.
    You can encrypt arbitrary data, with the key being reused each time.
    """
    key = get_random_bytes(256)
    assert len(flag) <= len(key)

    ciphertext = strxor(flag, key[:len(flag)])
    show_b64("secret ciphertext", ciphertext)

    while True:
        plaintext = input_b64("plaintext")
        ciphertext = strxor(plaintext, key[:len(plaintext)])
        show_b64("ciphertext", ciphertext)


def level5():
    """
    In this challenge you will decrypt a secret encrypted with Advanced Encryption Standard (AES).
    The Electronic Codebook (ECB) block cipher mode of operation is used.
    """
    key = get_random_bytes(16)
    cipher = AES.new(key=key, mode=AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(flag, cipher.block_size))
    show_b64("key", key)
    show_b64("secret ciphertext", ciphertext)


def level6():
    """
    In this challenge you will decrypt a secret encrypted with Advanced Encryption Standard (AES).
    The Electronic Codebook (ECB) block cipher mode of operation is used.
    You can encrypt arbitrary data, which has the secret appended to it, with the key being reused each time.
    """
    key = get_random_bytes(16)
    cipher = AES.new(key=key, mode=AES.MODE_ECB)

    ciphertext = cipher.encrypt(pad(flag, cipher.block_size))
    show_b64("secret ciphertext", ciphertext)

    while True:
        plaintext_prefix = input_b64("plaintext prefix")
        ciphertext = cipher.encrypt(pad(plaintext_prefix + flag, cipher.block_size))
        show_b64("ciphertext", ciphertext)


def level7():
    """
    In this challenge you will decrypt a secret encrypted with RSA (Rivest–Shamir–Adleman).
    You will be provided with both the public key and private key.
    """
    key = RSA.generate(2048)
    assert len(flag) <= 256
    ciphertext = pow(int.from_bytes(flag, "little"), key.e, key.n).to_bytes(256, "little")
    show_hex("e", key.e)
    show_hex("d", key.d)
    show_hex("n", key.n)
    show_b64("Your encrypted flag", ciphertext)


def level8():
    """
    In this challenge you will decrypt a secret encrypted with RSA (Rivest–Shamir–Adleman).
    You will be provided with the prime factors of n.
    """
    key = RSA.generate(2048)
    assert len(flag) <= 256
    ciphertext = pow(int.from_bytes(flag, "little"), key.e, key.n).to_bytes(256, "little")
    show_hex("e", key.e)
    show_hex("p", key.p)
    show_hex("q", key.q)
    show_b64("Your encrypted flag", ciphertext)


def level9():
    """
    In this challenge you will hash data with a Secure Hash Algorithm (SHA256).
    You will find a small hash collision.
    Your goal is to find data, which when hashed, has the same hash as the secret.
    Only the first 2 bytes of the SHA256 hash are considered.
    """
    prefix_length = 2
    sha256 = SHA256Hash(flag).digest()
    show_b64(f"secret sha256[:{prefix_length}]", sha256[:prefix_length])

    collision = input_b64("collision")
    if SHA256Hash(collision).digest()[:prefix_length] == sha256[:prefix_length]:
        show("flag", flag.decode())


def level10():
    """
    In this challenge you will hash data with a Secure Hash Algorithm (SHA256).
    You will compute a small proof-of-work.
    Your goal is to find response data, which when appended to the challenge data and hashed, begins with 3 null-bytes.
    """
    difficulty = 3

    challenge = get_random_bytes(32)
    show_b64("challenge", challenge)

    response = input_b64("response")
    if SHA256Hash(challenge + response).digest()[:difficulty] == (b'\0' * difficulty):
        show("flag", flag.decode())


def level11():
    """
    In this challenge, you will build an MD4 collision of a given string.

    You are strongly recommended to find an MD4 collision generator on the Internet or GitHub.
    You are not encouraged to implement the algorithm by yourself.
    """

    difficulty = 64

    m1 = input_b64(f"String 1 (Base64-encoded, {difficulty} bytes before encoding)")
    if len(m1) != difficulty:
        print(f"Incorrect: len(m1) != {difficulty}")
        return

    m1_hash = hashlib.new("md4")
    m1_hash.update(m1)
    show("String 1 MD4 hash", m1_hash.hexdigest())

    m2 = input_b64("String 2 (Base64-encoded, must be different from Sring 1)")
    if m1 == m2:
        print("Incorrect: m1 == m2")
        return

    m2_hash = hashlib.new("md4")
    m2_hash.update(m2)
    show("String 2 MD4 hash", m2_hash.hexdigest())

    if m1_hash.digest() == m2_hash.digest():
        show("Congratulations! Your flag", flag.decode())
    else:
        print("Incorrect: md4(m1) != md4(m2). Hashes do not match!")


def level12():
    """
    In this challenge, you will build an MD5 collision of two given PNG files.

    You are given `pic1.png` and `pic2.png`.
    Your goal is creating two files, `f1.png` and `f2.png`, that satisfy the following requirements:
    - `pic1.png` and `f1.png` look the same (have the same pixels at corresponding coordinates).
    - `pic2.png` and `f2.png` look the same (have the same pixels at corresponding coordinates).
    - `MD5(f1.png) == MD5(f2.png)`

    You are strongly recommended to find an MD5 collision generator on the Internet or GitHub.
    You are not encouraged to implement the algorithm by yourself.
    """

    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} filename1.png filename2.png")
        return

    fn1 = sys.argv[1]
    fn2 = sys.argv[2]
    if not os.path.isfile(fn1):
        print(f"File \"{fn1}\" is not found.")
        return
    if not os.path.isfile(fn2):
        print(f"File \"{fn2}\" is not found.")
        return

    data = {}
    for original_pic, input_pic in [("pic1.png", fn1), ("pic2.png", fn2)]:
        with open(original_pic, "rb") as f:
            pic_data = f.read()
        with open(input_pic, "rb") as f:
            f_data = f.read()
            data[input_pic] = f_data

        if f_data == pic_data:
            print(f"Incorrect: {original_pic} and {input_pic} are identical.")
            return

        try:
            pic = Image.open(original_pic)
        except Image.UnidentifiedImageError:
            print(f"Incorrect: {original_pic} is not a valid PNG file.")
            return
        try:
            pic_input = Image.open(input_pic)
        except Image.UnidentifiedImageError:
            print(f"Incorrect: {input_pic} is not a valid PNG file.")
            return
        if pic.size != pic_input.size:
            print(f"Incorrect: {original_pic} and {input_pic} have differet dimensions.")
            return
        # check every pixel
        for i in range(pic.size[0]):
            for j in range(pic.size[1]):
                if pic.getpixel((i, j)) != pic_input.getpixel((i, j)):
                    print(f"Incorrect: {orignal_pic} and {input_pic} have different pixels at position {i}, {j}.")
                    return
        print(f"{original_pic} and {input_pic} look the same.")

    # the two submission files should not be the same
    if data[fn1] == data[fn2]:
        print(f"The content of {fn1} and the content of {fn2} are the same. They cannot be the same file!")
        return
    else:
        print(f"The content of {fn1} is not the same as the content of {fn2}. Good.")

    # check MD5
    f1_md5 = hashlib.md5(data[fn1]).hexdigest()
    f2_md5 = hashlib.md5(data[fn2]).hexdigest()
    print(f"MD5({fn1}) = {f1_md5}")
    print(f"MD5({fn2}) = {f2_md5}")
    if f1_md5 != f2_md5:
        print(f"Incorrect: MD5({fn1}) != MD5({fn2})")
        return
    else:
        print(f"Collision found: MD5({fn1}) == MD5({fn2})")

    # checks passed
    show("Congratulations! Your flag", flag.decode())


def level13():
    """
    In this challenge, you will find the flag using the low-exponent attack.

    In the textbook implementation of RSA (when no padding is used), choosing an exponent that is sufficiently high is critical.
    Alice chose e = 3 and encrypted a flag.
    Please decrypt the message and obtain your flag.
    """

    key = RSA.generate(2048)
    assert len(flag) <= 256
    ciphertext = pow(int.from_bytes(flag, "little"), 3, key.n).to_bytes(256, "little")
    show_b64("Your encrypted flag", ciphertext)


def level14():
    """
    This challenge demonstrates insecure Ns in RSA.

    Factoring a large number `N` (where `N` = `p` * `q`, both `p` and `q` are prime numbers) is extremely difficult.
    However, the difficulty level is significantly reduced if `p` and `q` are too close to each other.
    Alice chose `p` and `q` that are too close.
    Please decrypt her RSA-encrypted message and obtain your flag.

    If you need to compute `d` from `p` and `q`, take a look at https://crypto.stackexchange.com/questions/19444/rsa-given-q-p-and-e
    """

    def egcd(a, b):
        """
        To make your life easier, you can use this function to compute d.

        Ref: https://crypto.stackexchange.com/questions/19444/rsa-given-q-p-and-e
        """
        x, y, u, v = 0, 1, 1, 0
        while a != 0:
            q, r = b // a, b % a
            m, n = x - u * q, y - v * q
            b, a, x, y, u, v = a, r, u, v, m, n
            gcd = b
        return gcd, x, y

    # generate p and q
    p = Primality.generate_probable_prime(exact_bits=1024)
    distance = random.randint(100000, 999999)
    q = (p + distance) | 1
    while Primality.test_probable_prime(q) == 0:
        q += 2
    p = int(p)
    q = int(q)
    n = p * q
    e = 0x10001

    # phi = (p - 1) * (q - 1)
    # d = egcd(e, phi)[1]

    # encrypt the flag
    ciphertext = pow(int.from_bytes(flag, "little"), e, n).to_bytes(256, "little")
    print("N =", n)
    print("e =", e)
    show_b64("Your encrypted flag", ciphertext)


def challenge():
    challenge_level = globals()[f"level{level}"]
    description = textwrap.dedent(challenge_level.__doc__)

    print("===== Welcome to Cryptography! =====")
    print("In this series of challenges, you will be working with various cryptographic mechanisms.")
    print(description)
    print()

    challenge_level()


challenge()

