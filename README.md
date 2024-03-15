## SECP256K1 Reference Implementation For Ethereum

This repository contains code for implementing ECDSA (Elliptic Curve Digital Signature Algorithm) and SECP256K1, specifically tailored for Ethereum blockchain development. It includes functionality for generating Ethereum-compatible public-private key pairs, signing Ethereum transactions, and verifying signatures.

## What is ECDSA?
ECDSA is a cryptographic algorithm used to create digital signatures. It is based on the mathematics of elliptic curves and provides a secure method for authenticating messages and transactions. ECDSA is widely used in blockchain technologies, digital currencies, and secure communication protocols.

## What is SECP256K1?
SECP256K1 is an elliptic curve commonly used in ECDSA-based cryptographic systems. It is defined over a finite field and offers a high level of security while maintaining efficiency in computation. SECP256K1 is particularly famous for its use in the Bitcoin and Ethereum protocol, where it is employed for generating public-private key pairs and signing transactions.

## Features

- **Key Generation**: Generate Ethereum-compatible public-private key pairs using SECP256K1.
- **Transaction Signing**: Sign Ethereum transactions using the private key.
- **Signature Verification**: Verify the authenticity of Ethereum transaction signatures using the corresponding public key.
- **Working Example**: Includes a working example demonstrating how to interact with Ethereum using the implemented ECDSA and SECP256K1 functionality.

## Code Content

- **ec.py**: Code for elliptic curve computation including jacobian operations.
- **point.py**: Codebase for curve point operations like addition, subtraction etc.
- **py2specials.py & py3specials.py**: Helper functions for encoding, base change, hex and bytes conversions.
- **rng.py**: Generate and store random number.
- **sig.py**: Implementation of key generation, signature and verification algorithms for Ethereum.
- **transaction.py**: Sample code to check transaction encoding.

## Example Usage

```
# Initialization
eth = Ethereum()
eth.init_infura()
eth.gen_acc()

# Sign check
# msg = "Hello Blockchain!"
# eth.sign(msg)
# eth.verify(msg,eth.r,eth.s)

# Sign and send transaction
eth.sign_tx(to='0x0aCA1E3f5e997295B3EF340f528E2B6a5970B6A9', value=10)
eth.send_tx()
```
