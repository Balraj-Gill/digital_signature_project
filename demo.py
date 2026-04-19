import os

from crypto.keygen import generate_keys
from crypto.signer import sign_file
from crypto.verifier import verify_file

from config import DOC_DIR, SIG_DIR
from utils.file_utils import ensure_directories, require_files


def run_demo():
    print("\n==============================")
    print(" Digital Signature Demo")
    print("==============================\n")

    ensure_directories()

    # File paths
    rsa_file = os.path.join(DOC_DIR, "sample.txt")
    rsa_tampered_file = os.path.join(DOC_DIR, "tampered_sample.txt")
    ecdsa_file = os.path.join(DOC_DIR, "policy.txt")

    required_files = [rsa_file, rsa_tampered_file, ecdsa_file]

    if not require_files(required_files, "demo file"):
        return

    # ---------------- RSA DEMO ----------------
    print("[1] Generating RSA keys...")
    rsa_private_key, rsa_public_key = generate_keys("sample", "RSA")

    print("[2] Signing sample file with RSA...")
    rsa_sig_path = sign_file(rsa_file, rsa_private_key, SIG_DIR, "RSA")

    print("[3] Verifying original file with RSA...")
    verify_file(rsa_file, rsa_sig_path, rsa_public_key, "RSA")

    print("[4] Verifying tampered file with RSA...")
    verify_file(rsa_tampered_file, rsa_sig_path, rsa_public_key, "RSA")

    # ---------------- ECDSA DEMO ----------------
    print("[5] Generating ECDSA keys...")
    ecdsa_private_key, ecdsa_public_key = generate_keys("policy", "ECDSA")

    print("[6] Signing policy file with ECDSA...")
    ecdsa_sig_path = sign_file(ecdsa_file, ecdsa_private_key, SIG_DIR, "ECDSA")

    print("[7] Verifying original file with ECDSA...")
    verify_file(ecdsa_file, ecdsa_sig_path, ecdsa_public_key, "ECDSA")

    print("==============================")
    print(" Demo Complete")
    print("==============================\n")


if __name__ == "__main__":
    run_demo()