## SECP256K1 Reference Implementation For Ethereum

This repository provides reference implementation for getting started with key generation, signing, verification, and a working example for Ethereum.

## Overview

This repository contains code for implementing ECDSA (Elliptic Curve Digital Signature Algorithm) and SECP256K1, specifically tailored for Ethereum blockchain development. It includes functionality for generating Ethereum-compatible public-private key pairs, signing Ethereum transactions, and verifying signatures.

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

- **eth.py**: This file contains code to connect to Ethereum blockchain via Infura, generate keys and accounts for Ethereum, create a sample transaction, sign and verify the transaction, and finally send the transaction to blockchain.
