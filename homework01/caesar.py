def encrypt_caesar(plaintext: str, shift: int) -> str:
    """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for sumb in plaintext:
        if "A" <= sumb <= "Z":
            code_sumb = ord(sumb) + shift
            if ord("A") > code_sumb or code_sumb > ord("Z"):
                code_sumb -= 26
            ciphertext += chr(code_sumb)

        elif "a" <= sumb <= "z":
            code_sumb = ord(sumb) + shift
            if ord("a") > code_sumb or code_sumb > ord("z"):
                code_sumb -= 26
            ciphertext += chr(code_sumb)
        else:
            ciphertext += sumb

    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int) -> str:
    """
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for sumb in ciphertext:
        if "A" <= sumb <= "Z":
            code_sumb = ord(sumb) - shift
            if code_sumb > ord("Z") or code_sumb < ord("A"):
                code_sumb += 26
            plaintext += chr(code_sumb)

        elif "a" <= sumb <= "z":
            code_sumb = ord(sumb) - shift
            if code_sumb > ord("z") or code_sumb < ord("a"):
                code_sumb += 26
            plaintext += chr(code_sumb)
        else:
            plaintext += sumb

    return plaintext


if __name__ == "__main__":
    print(encrypt_caesar("python", 0))
