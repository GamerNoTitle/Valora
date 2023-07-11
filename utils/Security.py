from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


def generate():
    # Generate RSA Keys Pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    # Save Private Key
    pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open('private_key.pem', 'wb') as f:
        f.write(pem_private_key)

    # Save Public Key
    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open('public_key.pem', 'wb') as f:
        f.write(pem_public_key)


def read_key():
    # Read Private key
    with open('private_key.pem', 'rb') as f:
        pem_private_key = f.read()

    # Read Public Key
    with open('public_key.pem', 'rb') as f:
        pem_public_key = f.read()

    # Convert Private key to correct type
    private_key = serialization.load_pem_private_key(
        pem_private_key, password=None
    )

    # Convert Public key to correct type
    public_key = serialization.load_pem_public_key(pem_public_key)
    return public_key, private_key

def encrypt(message):
    # 加密
    public_key, private_key = read_key()
    ciphertext = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext


def decrypt(ciphertext):
    # 解密
    public_key, private_key = read_key()
    decrypted_message = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_message.decode()