import hashlib


def generate_id(*args):
    input_data = "-".join(map(str, args))
    hash_object = hashlib.sha256(input_data.encode())
    hash_hex = hash_object.hexdigest()
    return hash_hex[:40]
