Decode OpenTRV radio frames.

# Dependencies
- cryptography v2.0+ (https://cryptography.io/en/latest/)

# Changlog
- V1.1 (20170808)
    - DE20170808 Fixed issue with authentication due to incorrect aad data.
    - DE20170807 Switched decryption to new cryptography.hazmat.primitives.ciphers.aead.AESGCM API.
    - DE20170807 Fixed issue with decryption due to bad frame description.

# TODO
- Proper --help option.
