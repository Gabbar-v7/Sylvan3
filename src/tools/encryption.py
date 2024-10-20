import hmac
import hashlib
from keys import HASH_KEY  # Importing the key from the specified module


def hash(data: str) -> str:
    # Encode the data and the key
    key = HASH_KEY.encode()
    data = data.encode()

    # Create a new HMAC object using the key and the SHA-256 hash function
    hashed = hmac.new(key, data, hashlib.sha256)

    # Return the hash as a hexadecimal string
    return hashed.hexdigest()
