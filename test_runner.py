import os

from crypto.keygen import generate_keys
from crypto.signer import sign_file
from crypto.verifier import verify_file

from config import DOC_DIR, SIG_DIR
from utils.file_utils import ensure_directories, file_exists, require_files


def run_tests():
    print("\n=== Running Tests ===\n")

    ensure_directories()

    # Required test files
    rsa_file = os.path.join(DOC_DIR, "sample.txt")
    rsa_tampered_file = os.path.join(DOC_DIR, "tampered_sample.txt")
    ecdsa_file = os.path.join(DOC_DIR, "policy.txt")

    required_files = [rsa_file, rsa_tampered_file, ecdsa_file]

    if not require_files(required_files, "test file"):
        return

    # ---------------- RSA FLOW ----------------
    print("[Test 1] RSA Key Generation...")
    rsa_private_key, rsa_public_key = generate_keys("sample", "RSA")

    if rsa_private_key and rsa_public_key and file_exists(rsa_private_key) and file_exists(rsa_public_key):
        print("PASS: RSA keys generated\n")
    else:
        print("FAIL: RSA keys not generated\n")
        return

    print("[Test 2] RSA Signing...")
    rsa_sig_path = sign_file(rsa_file, rsa_private_key, SIG_DIR, "RSA")

    if rsa_sig_path and file_exists(rsa_sig_path):
        print("PASS: RSA signature created\n")
    else:
        print("FAIL: RSA signature not created\n")
        return

    print("[Test 3] RSA Valid Verification...")
    rsa_valid = verify_file(rsa_file, rsa_sig_path, rsa_public_key, "RSA")

    if rsa_valid:
        print("PASS: RSA valid signature verified\n")
    else:
        print("FAIL: RSA valid signature failed\n")
        return

    print("[Test 4] RSA Tampered Verification...")
    rsa_tampered = verify_file(rsa_tampered_file, rsa_sig_path, rsa_public_key, "RSA")

    if not rsa_tampered:
        print("PASS: RSA tampered file detected\n")
    else:
        print("FAIL: RSA tampered file incorrectly verified\n")
        return

    # ---------------- ECDSA FLOW ----------------
    print("[Test 5] ECDSA Key Generation...")
    ecdsa_private_key, ecdsa_public_key = generate_keys("policy", "ECDSA")

    if ecdsa_private_key and ecdsa_public_key and file_exists(ecdsa_private_key) and file_exists(ecdsa_public_key):
        print("PASS: ECDSA keys generated\n")
    else:
        print("FAIL: ECDSA keys not generated\n")
        return

    print("[Test 6] ECDSA Signing...")
    ecdsa_sig_path = sign_file(ecdsa_file, ecdsa_private_key, SIG_DIR, "ECDSA")

    if ecdsa_sig_path and file_exists(ecdsa_sig_path):
        print("PASS: ECDSA signature created\n")
    else:
        print("FAIL: ECDSA signature not created\n")
        return

    print("[Test 7] ECDSA Valid Verification...")
    ecdsa_valid = verify_file(ecdsa_file, ecdsa_sig_path, ecdsa_public_key, "ECDSA")

    if ecdsa_valid:
        print("PASS: ECDSA valid signature verified\n")
    else:
        print("FAIL: ECDSA valid signature failed\n")
        return

    print("[Test 8] Wrong Key Verification...")
    wrong_key_result = verify_file(ecdsa_file, ecdsa_sig_path, rsa_public_key, "ECDSA")

    if not wrong_key_result:
        print("PASS: Wrong key verification failed as expected\n")
    else:
        print("FAIL: Wrong key verification incorrectly succeeded\n")
        return

    print("=== ALL TESTS PASSED ===\n")


if __name__ == "__main__":
    run_tests()