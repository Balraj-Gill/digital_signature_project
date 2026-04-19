import os

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding

from utils.file_utils import read_bytes, write_bytes, get_filename, file_exists


def sign_file(file_path, private_key_path, sig_dir, algorithm):
    """
    Sign a file using RSA-PSS or ECDSA with SHA-256.

    Args:
        file_path (str): Path to the file to sign
        private_key_path (str): Path to the private key (.pem)
        sig_dir (str): Directory where the signature will be saved
        algorithm (str): "RSA" or "ECDSA"

    Returns:
        str | None: Path to the generated signature file, or None on failure
    """

    algorithm = algorithm.upper()

    # Validate algorithm
    if algorithm not in ["RSA", "ECDSA"]:
        print("✘ Error: Unsupported algorithm. Use RSA or ECDSA.")
        return None

    # Validate inputs
    if not file_exists(file_path):
        print(f"✘ Error: File not found → {file_path}")
        return None

    if not file_exists(private_key_path):
        print(f"✘ Error: Private key not found → {private_key_path}")
        return None

    print("\n[1] Loading private key...")

    with open(private_key_path, "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None
        )

    print(f"[2] Reading file: {file_path}")
    data = read_bytes(file_path)

    print(f"[3] Creating {algorithm} digital signature...")

    if algorithm == "RSA":
        signature = private_key.sign(
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    elif algorithm == "ECDSA":
        signature = private_key.sign(
            data,
            ec.ECDSA(hashes.SHA256())
        )

    # Build signature file path
    filename = get_filename(file_path)
    base_name, _ = os.path.splitext(filename)
    sig_path = os.path.join(sig_dir, f"{base_name}_{algorithm.lower()}.sig")

    print(f"[4] Saving signature to: {sig_path}")
    write_bytes(sig_path, signature)

    print(f"✔ {algorithm} file signed successfully.\n")

    return sig_path