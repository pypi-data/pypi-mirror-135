import os
import jwt
from jwt.exceptions import PyJWTError, DecodeError, ExpiredSignatureError
import base64
from math import ceil, log
from Crypto.Cipher import AES


BLOCK_SIZE = AES.block_size


def pad(s):
    return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(
        BLOCK_SIZE - len(s) % BLOCK_SIZE
    )


def unpad(s):
    return s[: -ord(s[len(s) - 1 :])]


def encrypt(raw, password):
    private_key = password.encode("utf-8")
    raw = pad(raw)
    cipher = AES.new(private_key, AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(raw))


def decrypt(enc, password):
    private_key = password.encode("utf-8")
    enc = base64.b64decode(enc)
    cipher = AES.new(private_key, AES.MODE_ECB)
    return unpad(cipher.decrypt(enc))


def read_key_from_env(key: str, linebreakword: str = "_LINEBREAK_") -> str:
    content = os.getenv(key)
    if content.startswith(linebreakword):
        content = content[len(linebreakword) :]
    if content.endswith(linebreakword):
        content = content[: -len(linebreakword)]
    return content.replace(linebreakword, "\n")


def decrypt_aes_encoding(token, secret):
    try:
        return decrypt(token, secret).decode("utf-8")
    except ValueError:
        raise Exception("Impossible to decode token with given secret")


def ensure_token_validity(token):
    try:
        payload = jwt.decode(
            token,
            os.getenv("PUBLIC_KEY").replace("_LINEBREAK_", "\n"),
            algorithms=["RS256"],
        )
        if "sub" not in payload:
            raise Exception("sub key is missing")
    except DecodeError:
        raise Exception("token is not an encoded JWT")
    except ExpiredSignatureError:
        raise Exception("token is expired")
    except Exception:
        raise Exception("unknown error")


def get_payload(token, safe=True):
    if safe:
        ensure_token_validity(token)
    return jwt.decode(
        token,
        os.getenv("PUBLIC_KEY").replace("_LINEBREAK_", "\n"),
        algorithms=["RS256"],
    )


def nanoid_algorithm(random_bytes):
    """From https://github.com/puyuan/py-nanoid"""
    return bytearray(os.urandom(random_bytes))


def generate_session_id(
    alphabet="_-0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", size=8
):
    """Adapted from https://github.com/puyuan/py-nanoid"""
    alphabet_len = len(alphabet)
    mask = 1
    if alphabet_len > 1:
        mask = (2 << int(log(alphabet_len - 1) / log(2))) - 1
    step = int(ceil(1.6 * mask * size / alphabet_len))
    session_id = ""
    while True:
        random_bytes = nanoid_algorithm(step)
        for i in range(step):
            random_byte = random_bytes[i] & mask
            if random_byte < alphabet_len and alphabet[random_byte]:
                session_id += alphabet[random_byte]
                if len(session_id) == size:
                    return session_id


# First let us encrypt secret message
if __name__ == "__main__":
    password = input("Enter encryption password: ")
    if len(password) != 32:
        print("must be at least 32 char long")
        exit(1)
    encrypted = encrypt("This is a secret message", password)
    print(encrypted)
    print(base64.b64encode(encrypted))

    # Let us decrypt using our original password
    decrypted = decrypt(encrypted, password)
    print(bytes.decode(decrypted))