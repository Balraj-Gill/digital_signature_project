import os

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa

from config import KEY_DIR
from utils.file_utils import write_bytes


def get_key_paths(name, algorithm="RSA"):
    """
    Build private/public key paths based on a user-provided name
    and algorithm.

    Args:
        name (str): Base name for key files (example: "student")
        algorithm (str): "RSA" or "ECDSA"

    Returns:
        tuple[str, str]: (private_key_path, public_key_path)
    """
    algorithm = algorithm.upper()

    private_path = os.path.join(KEY_DIR, f"{name}_{algorithm.lower()}_private.pem")
    public_path = os.path.join(KEY_DIR, f"{name}_{algorithm.lower()}_public.pem")

    return private_path, public_path


def generate_keys(name, algorithm="RSA"):
    """
    Generate an RSA or ECDSA key pair and save them as PEM files.

    Args:
        name (str): Base name for key files
        algorithm (str): "RSA" or "ECDSA"

    Returns:
        tuple[str, str] | tuple[None, None]:
            Paths to the generated private/public key files,
            or (None, None) if the algorithm is invalid.
    """
    algorithm = algorithm.upper()

    if algorithm not in ["RSA", "ECDSA"]:
        print("✘ Error: Unsupported algorithm. Use RSA or ECDSA.")
        return None, None

    private_path, public_path = get_key_paths(name, algorithm)

    print(f"\n[1] Generating {algorithm} key pair...")

    if algorithm == "RSA":
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
    else:  # ECDSA
        private_key = ec.generate_private_key(ec.SECP256R1())

    public_key = private_key.public_key()

    print("[2] Saving private key...")

    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    write_bytes(private_path, private_bytes)
    print(f"    → {private_path}")

    print("[3] Saving public key...")

    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    write_bytes(public_path, public_bytes)
    print(f"    → {public_path}")

    print(f"\n✔ {algorithm} key generation complete.\n")

    return private_path, public_path