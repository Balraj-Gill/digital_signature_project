import sys

from crypto.keygen import generate_keys, get_key_paths
from crypto.signer import sign_file
from crypto.verifier import verify_file

from config import SIG_DIR
from utils.file_utils import ensure_directories


def print_usage():
    print("\nUsage:")
    print("  python main.py keygen <name> <algorithm>")
    print("  python main.py sign <file_path> <name> <algorithm>")
    print("  python main.py verify <file_path> <signature_path> <name> <algorithm>")
    print("\nExamples:")
    print("  python main.py keygen sample RSA")
    print("  python main.py keygen policy ECDSA")
    print("  python main.py sign data/documents/sample.txt sample RSA")
    print("  python main.py verify data/documents/sample.txt data/signatures/sample_rsa.sig sample RSA\n")


def main():
    ensure_directories()

    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1]

    # ---- KEY GENERATION ----
    if command == "keygen":
        if len(sys.argv) < 4:
            print("Missing arguments for key generation.")
            print_usage()
            return

        name = sys.argv[2]
        algorithm = sys.argv[3]

        generate_keys(name, algorithm)

    # ---- SIGN FILE ----
    elif command == "sign":
        if len(sys.argv) < 5:
            print("Missing arguments for signing.")
            print_usage()
            return

        file_path = sys.argv[2]
        name = sys.argv[3]
        algorithm = sys.argv[4]

        private_key_path, _ = get_key_paths(name, algorithm)
        sign_file(file_path, private_key_path, SIG_DIR, algorithm)

    # ---- VERIFY FILE ----
    elif command == "verify":
        if len(sys.argv) < 6:
            print("Missing arguments for verification.")
            print_usage()
            return

        file_path = sys.argv[2]
        signature_path = sys.argv[3]
        name = sys.argv[4]
        algorithm = sys.argv[5]

        _, public_key_path = get_key_paths(name, algorithm)
        verify_file(file_path, signature_path, public_key_path, algorithm)

    else:
        print(f"Unknown command: {command}")
        print_usage()


if __name__ == "__main__":
    main()