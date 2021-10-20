import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for letter in plaintext:
        if "A" <= letter <= "Z" or "a" <= letter <= "z":
            if "A" <= letter <= "Z" and chr(ord(letter) + shift) > "Z":
                letter = chr(ord(letter) - 26 + shift)
                ciphertext += letter
            elif "a" <= letter <= "z" and chr(ord(letter) + shift) > "z":
                letter = chr(ord(letter) - 26 + shift)
                ciphertext += letter
            else:
                letter = chr(ord(letter) + shift)
                ciphertext += letter
        else:
            ciphertext += letter
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for letter in ciphertext:
        if "A" <= letter <= "Z" or "a" <= letter <= "z":
            if "A" <= letter <= "Z" and chr(ord(letter) - shift) < "A":
                letter = chr(ord(letter) + 26 - shift)
                plaintext += letter
            elif "a" <= letter <= "z" and chr(ord(letter) - shift) < "a":
                letter = chr(ord(letter) + 26 - shift)
                plaintext += letter
            else:
                letter = chr(ord(letter) - shift)
                plaintext += letter
        else:
            plaintext += letter
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    for key in range(len(ciphertext)):
        translated = ""
        for symbol in dictionary:
            if symbol in ciphertext:
                num = ciphertext.find(symbol)
                num -= key
                if num < 0:
                    num += len(ciphertext)
                    translated += symbol
    return best_shift
