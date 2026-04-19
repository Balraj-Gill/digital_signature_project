# Digital Signature & Document Verification

## Overview

This project implements a digital signature and document verification system using public-key cryptography in Python.

It allows users to:
- Generate key pairs (RSA or ECDSA)
- Sign documents
- Verify document authenticity and integrity

If a document is modified after signing, verification will fail.

---

## Features

- RSA (2048-bit) and ECDSA (SECP256R1) support
- SHA-256 hashing
- Detached binary signature files (`.sig`)
- Support for text and PDF files (any file treated as bytes)
- CLI interface (`main.py`)
- Automated test runner
- Demo script

---

## Technologies Used

- Python 3.12
- `cryptography` library
- RSA (PSS padding)
- ECDSA
- SHA-256

---

## Project Structure

```text
digital_signature_project/
│
├── main.py
├── demo.py
├── test_runner.py
├── config.py
├── README.md
├── requirements.txt
│
├── crypto/
│   ├── keygen.py
│   ├── signer.py
│   ├── verifier.py
│
├── utils/
│   ├── file_utils.py
│
├── data/
│   ├── keys/
│   ├── documents/
│   │   ├── sample.txt
│   │   ├── sample_tampered.txt
│   │   └── policy.txt
│   ├── signatures/
```

---

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

### 1. Generate Keys

```bash
python main.py keygen <name> <algorithm>
```

Example:

```bash
python main.py keygen student RSA
python main.py keygen admin ECDSA
```

This creates:

```text
data/keys/student_rsa_private.pem
data/keys/student_rsa_public.pem
```

---

### 2. Sign a File

```bash
python main.py sign <file_path> <name> <algorithm>
```

Example:

```bash
python main.py sign data/documents/sample.txt student RSA
```

Creates:

```text
data/signatures/sample_rsa.sig
```

---

### 3. Verify a File

```bash
python main.py verify <file_path> <signature_path> <name> <algorithm>
```

Example:

```bash
python main.py verify data/documents/sample.txt data/signatures/sample_rsa.sig student RSA
```

---

## Demo

Run the full demonstration:

```bash
python demo.py
```

This will:

1. Generate RSA keys  
2. Sign a file  
3. Verify original file (valid)  
4. Verify tampered file (invalid)  
5. Repeat with ECDSA  

---

## Testing

Run all tests:

```bash
python test_runner.py
```

Tests include:
- RSA signing and verification
- Tampered file detection
- ECDSA signing and verification
- Wrong key verification failure

---

## Example Output

Valid file:

```text
VALID SIGNATURE
```

Tampered file:

```text
INVALID SIGNATURE (file may have been modified)
```

---

## How It Works

1. The file is read as binary data  
2. A SHA-256 hash is computed internally  
3. The hash is signed using the private key  
4. The signature is stored in a `.sig` file  
5. During verification:
   - The file is hashed again
   - The signature is verified using the public key  

If the file changes, verification fails.

---

## Limitations

- No Certificate Authority (CA)
- No identity binding beyond key ownership
- No web interface
- No large-scale key management

---

## Authors

- Balraj Gill
- Tarushi
