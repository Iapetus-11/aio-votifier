def ensure_pem_format(key: str) -> str:
    """Creates a properly formatted RSA public key from the unformatted data usually passed"""

    key = key.strip()

    if not key.startswith("-----BEGIN PUBLIC KEY-----") and not key.startswith("-----BEGIN RSA PUBLIC KEY-----"):
        key = key.replace("\r", "").replace("\n", "")
        key = "\n".join([key[i : i + 64] for i in range(0, len(key), 64)])
        key = "-----BEGIN PUBLIC KEY-----\n" + key + "\n-----END PUBLIC KEY-----\n"

    return key
