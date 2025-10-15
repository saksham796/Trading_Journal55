import base64
import secrets
from dataclasses import dataclass
from typing import List

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

from .models import Trade


# ---------- Encryption helpers ----------
PBKDF2_ITERATIONS = 210_000  # reasonably strong default
SALT_BYTES = 16


def _derive_key(password: str, salt: bytes, iterations: int = PBKDF2_ITERATIONS) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )
    key = kdf.derive(password.encode('utf-8'))
    return base64.urlsafe_b64encode(key)  # Fernet expects base64 key


@dataclass
class EncryptedPayload:
    salt_b64: str
    iterations: int
    blob_b64: str


def encrypt_payload(password: str, data_json: str) -> EncryptedPayload:
    import os
    salt = os.urandom(SALT_BYTES)
    key = _derive_key(password, salt)
    f = Fernet(key)
    token = f.encrypt(data_json.encode('utf-8'))
    return EncryptedPayload(
        salt_b64=base64.b64encode(salt).decode('ascii'),
        iterations=PBKDF2_ITERATIONS,
        blob_b64=base64.b64encode(token).decode('ascii'),
    )


def decrypt_payload(password: str, payload: EncryptedPayload) -> str:
    salt = base64.b64decode(payload.salt_b64)
    token = base64.b64decode(payload.blob_b64)
    key = _derive_key(password, salt, payload.iterations)
    f = Fernet(key)
    decrypted = f.decrypt(token)
    return decrypted.decode('utf-8')


# ---------- Journal-specific storage using Django ORM ----------

def save_encrypted_trade(user_id: int, encrypted: EncryptedPayload) -> int:
    trade = Trade.objects.create(
        user_id=user_id,
        salt_b64=encrypted.salt_b64,
        iterations=encrypted.iterations,
        blob_b64=encrypted.blob_b64,
    )
    return trade.pk


def list_encrypted_trades(user_id: int) -> List[dict]:
    qs = Trade.objects.filter(user_id=user_id).order_by('-id')
    # Return dicts similar to the previous Mongo shape to minimize changes elsewhere
    return [
        {
            '_id': t.pk,
            'salt_b64': t.salt_b64,
            'iterations': t.iterations,
            'blob_b64': t.blob_b64,
        }
        for t in qs
    ]
