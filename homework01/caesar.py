def encrypt_caesar(plaintext: str)->str:
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
        if 'A' <= sumb <= 'Z' or 'a' <= sumb <= 'z':
            code_sumb = ord(sumb) + 3
            if code_sumb > ord('Z') and code_sumb < ord('a') or code_sumb > ord('z'):
                code_sumb -= 26
            ciphertext += chr(code_sumb)
        else:
            ciphertext += sumb
    return ciphertext


def decrypt_caesar(ciphertext: str)->str:
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
        if 'A' <= sumb <= 'Z' or 'a' <= sumb <= 'z':
            code_sumb = ord(sumb) - 3
            if code_sumb > ord('Z') and code_sumb < ord('a') or code_sumb < ord('A'):
                code_sumb += 26
            plaintext += chr(code_sumb)
        else:
            plaintext += sumb

    return plaintext
