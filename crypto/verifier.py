from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa

from utils.file_utils import read_bytes, file_exists


def verify_file(file_path, signature_path, public_key_path, algorithm):
    """
    Verify a file signature using RSA-PSS or ECDSA with SHA-256.

    Args:
        file_path (str): Path to the file to verify
        signature_path (str): Path to the signature file (.sig)
        public_key_path (str): Path to the public key (.pem)
        algorithm (str): "RSA" or "ECDSA"

    Returns:
        bool: True if signature is valid, False otherwise
    """

    algorithm = algorithm.upper()

    # Validate algorithm
    if algorithm not in ["RSA", "ECDSA"]:
        print("Error: Unsupported algorithm. Use RSA or ECDSA.")
        return False

    # Validate inputs
    if not file_exists(file_path):
        print(f"Error: File not found -> {file_path}")
        return False

    if not file_exists(signature_path):
        print(f"Error: Signature not found -> {signature_path}")
        return False

    if not file_exists(public_key_path):
        print(f"Error: Public key not found -> {public_key_path}")
        return False

    print("\n[1] Loading public key...")

    with open(public_key_path, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    print(f"[2] Reading file: {file_path}")
    data = read_bytes(file_path)

    print(f"[3] Reading signature: {signature_path}")
    signature = read_bytes(signature_path)

    print(f"[4] Verifying {algorithm} signature...")

    try:
        if algorithm == "RSA":
            if not isinstance(public_key, rsa.RSAPublicKey):
                print("Error: Public key is not an RSA key.")
                return False

            public_key.verify(
                signature,
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

        elif algorithm == "ECDSA":
            if not isinstance(public_key, ec.EllipticCurvePublicKey):
                print("Error: Public key is not an ECDSA key.")
                return False

            public_key.verify(
                signature,
                data,
                ec.ECDSA(hashes.SHA256())
            )

        print("VALID SIGNATURE\n")
        return True

    except InvalidSignature:
        print("INVALID SIGNATURE (file may have been modified)\n")
        return False

    except Exception as e:
        print(f"Verification error: {e}\n")
        return False