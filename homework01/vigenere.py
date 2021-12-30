def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    while len(keyword) < len(plaintext):
        keyword += keyword
    keyword = keyword.upper()

    ciphertext = ""
    
    for num, symbol in enumerate(plaintext):
        if 'A' <= symbol <= 'Z' or 'a' <= symbol <= 'z':
            shift = ord(keyword[num % len(keyword)])
            shift -= ord('a') if 'z' >= symbol >= 'a' else ord('A')
            symbol_code = ord(symbol) + shift
        if 'a' <= symbol <= 'z' and symbol_code > ord('z'):
            symbol_code -= 26
        elif 'A' <= symbol <= 'Z' and symbol_code > ord('Z'):
            symbol_code -= 26
            ciphertext += chr(symbol_code)
    
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    while len(keyword) < len(ciphertext):
        keyword += keyword
    keyword = keyword.upper()

    plaintext = ""

    for num, symbol in enumerate(ciphertext):
        if 'A' <= symbol <= 'Z' or 'a' <= symbol <= 'z':
            shift = ord(keyword[num % len(keyword)])
            shift -= ord('a') if 'z' >= symbol >= 'a' else ord('A')
            symbol_code = ord(symbol) - shift
        if 'a' <= symbol <= 'z' and symbol_code < ord('a'):
            symbol_code += 26
        elif 'A' <= symbol <= 'Z' and symbol_code < ord('A'):
            symbol_code += 26
            plaintext += chr(symbol_code)

    return plaintext
