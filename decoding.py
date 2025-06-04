import json
import random
import string

from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from other import llm

vigenere_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
You are a helper who helps with the Vigenère  cipher.

Extract the following from the user's query:
- Operation: "encrypt" or "decrypt"
- Message: The full text to encrypt or decrypt. It will always be enclosed in double quotes ("") and will follow the word "message =" or appear inside quotes in a sentence.
- Key: The keyword to use. It will always follow the word 'key = ' and will be enclosed in double quotes ("").

If any values that should be enclosed in quotation marks are not, inform the user that the message must be written as "message here", and the key must be written after the word key and enclosed in quotation marks as key="key here".
This ensures the input is clear and properly formatted for accurate processing.
Example:
Encrypt me the message "Hello, I'll be happy to help you" using the Vigenère method with key="Cybersecurity".

Only respond in valid JSON format with the keys "operation", "message", and "key". If anything is missing, set to null.

User query:
{query}
"""
)

caesar_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
You are a helper who helps with a Caesar cipher.

Extract the following from the user's request:
- Operation: "encrypt" or "decrypt"
- Message: The full text to encrypt or decrypt. It will always be enclosed in double quotes ("") and will follow the word "message =" or appear inside quotes in a sentence.
- Step, or offset: The integer offset to use. It will always follow the word 'step = ' and will be enclosed in double quotes ("").

If any values that should be enclosed in quotation marks are not, inform the user that the message must be written as "message here", and the key must be written after the word key and enclosed in quotation marks as key="step oroffset here".
This ensures the input is clear and properly formatted for accurate processing.
Example:
Encrypt me the message "Hello, I'll be happy to help you" using the Caesar method with step = "5".

Reply only in valid JSON format with the keys "operation", "message", and "step". If anything is missing, set it to null.

User's request:
{query}
"""
)

defoe_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
You are a helper who assists with the Daniel Defoe cipher.

Extract the following from the user's request:
- Operation: "encrypt" or "decrypt"
- Message: The full text to encrypt or decrypt. It will always be enclosed in double quotes ("") and will follow the word "message =" or appear inside quotes in a sentence.
- Key: Either "even"  or "odd". It will always follow the word "key =" or appear as "even"/"odd" next to the text or in the request and will be enclosed in double quotes ("").

If any values that should be enclosed in quotation marks are not, inform the user that the message must be written as "message here", and the key must be written after the word key and enclosed in quotation marks as key="even or odd here".
This ensures the input is clear and properly formatted for accurate processing.
Example:
Encrypt me the message "Hello, I'll be happy to help you" using the Daniel Defoe method with key = "even".

Reply only in valid JSON format with the keys "operation", "message", and "key". If anything is missing, set it to null.

User's request:
{query}
"""
)

tritemius_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
You are a helper who assists with a Trithemius cipher.

Extract the following from the user's request:
- Operation: "encrypt" or "decrypt"
- Message: The full text to encrypt or decrypt. It will always be enclosed in double quotes ("") and will follow the word "message =" or appear inside quotes in a sentence.

If any values that should be enclosed in quotation marks are not, inform the user that the message must be written as "message here".

This ensures the input is clear and properly formatted for accurate processing.

Example:
Encrypt me the message "Hello, I'll be happy to help you" using the Trithemius method.

Reply only in valid JSON format with the keys "operation" and "message". If anything is missing, set it to null.

User's request:
{query}
"""
)


atbash_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
You are a helper who helps with the Atbash cipher.

Extract the following from the user's query:
- Operation: "encrypt" or "decrypt"
- Message: The full text to encrypt or decrypt. It will always be enclosed in double quotes ("") and will follow the word "message =" or appear inside quotes in a sentence.

If any values that should be enclosed in quotation marks are not, inform the user that the message must be written as "message here".
This ensures the input is clear and properly formatted for accurate processing.

Only respond in valid JSON format with the keys "operation" and "message". If anything is missing, set to null.

User query:
{query}
"""
)



# ШИФР ВІЖЕНЕРА



def vigenere_encrypt(plaintext: str, key: str) -> str:
    encrypted = []
    key = key.lower()
    key_index = 0
    for char in plaintext:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('a')
            base = ord('A') if char.isupper() else ord('a')
            encrypted_char = chr((ord(char) - base + shift) % 26 + base)
            encrypted.append(encrypted_char)
            key_index += 1
        else:
            encrypted.append(char)

    return ''.join(encrypted)

def vigenere_decrypt(ciphertext: str, key: str) -> str:
    decrypted = []
    key = key.lower()
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('a')
            base = ord('A') if char.isupper() else ord('a')
            decrypted_char = chr((ord(char) - base - shift + 26) % 26 + base)
            decrypted.append(decrypted_char)
            key_index += 1
        else:
            decrypted.append(char)

    return ''.join(decrypted)

vigenere_chain = LLMChain(
    llm=llm,
    prompt=vigenere_prompt
)

def vigenere_logic(query: str) -> str:
    parsed = vigenere_chain.run(query)
    try:
        data = json.loads(parsed)
    except json.JSONDecodeError:
        return f"Sorry, I didn't quite understand. If you're trying to encrypt or decrypt something, please provide the message like this: message = \"your message here\" and the key like this: key = \"your key here\"."
    operation = data.get("operation")
    message = data.get("message")
    key = data.get("key")
    if message is None or not any(c.isalpha() for c in message):
        return "Sorry, the message must contain at least one letter for encryption/decryption."
    if not operation or not message or not key:
        return f"Sorry, I didn't quite understand. If you're trying to encrypt or decrypt something, please provide the message like this: message = \"your message here\" and the key like this: key = \"your key here\"."
    if operation.lower() == "encrypt":
        return vigenere_encrypt(message, key)
    elif operation.lower() == "decrypt":
        return vigenere_decrypt(message, key)
    else:
        return f"Sorry, I didn't quite understand. If you're trying to encrypt or decrypt something, please provide the message like this: message = \"your message here\" and the key like this: key = \"your key here\"."



# ШИФР ЦЕЗАРЯ



def caesar_encrypt(plaintext: str, shift: int) -> str:
    encrypted = []
    for char in plaintext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            encrypted.append(chr((ord(char) - base + shift) % 26 + base))
        else:
            encrypted.append(char)
    return ''.join(encrypted)

def caesar_decrypt(ciphertext: str, shift: int) -> str:
    return caesar_encrypt(ciphertext, -shift)

caesar_chain = LLMChain(
    llm=llm,
    prompt=caesar_prompt
)

def caesar_logic(query: str) -> str:
    parsed = caesar_chain.run(query)
    try:
        data = json.loads(parsed)
    except json.JSONDecodeError:
        return f"Sorry, I didn't quite understand. If you're trying to encrypt or decrypt something, please provide the message like this: message = \"your message here\" and the step like this: key = \"your step here\"."
    operation = data.get("operation")
    message = data.get("message")
    step = data.get("step")
    if message is None or not any(c.isalpha() for c in message):
        return "Sorry, the message must contain at least one letter for encryption/decryption."
    if not operation or not message or step is None:
        return f"Sorry, I didn't quite understand. If you're trying to encrypt or decrypt something, please provide the message like this: message = \"your message here\" and the step like this: key = \"your step here\"."
    try:
        shift = int(step)
    except ValueError:
        return f"Sorry, I didn't quite understand. If you're trying to encrypt or decrypt something, please provide the message like this: message = \"your message here\" and the step like this: key = \"your step here\"."
    if operation.lower() == "encrypt":
        return caesar_encrypt(message, shift)
    elif operation.lower() == "decrypt":
        return caesar_decrypt(message, shift)
    else:
        return f"Sorry, I didn't quite understand. If you're trying to encrypt or decrypt something, please provide the message like this: message = \"your message here\" and the step like this: key = \"your step here\"."



# МЕТОД ДАНІЕЛЯ ДЕФО



def defoe_encrypt(plaintext: str, key: str) -> str:
    length = len(plaintext)
    cipher_len = length * 2
    cipher = [''] * cipher_len
    if key.lower() == "even":
        message_positions = range(0, cipher_len, 2)
    elif key.lower() == "odd":
        message_positions = range(1, cipher_len, 2)
    else:
        raise ValueError("The key must be 'even' or 'odd'.")
    for i, pos in enumerate(message_positions):
        if i < length:
            cipher[pos] = plaintext[i]
    for i in range(cipher_len):
        if cipher[i] == '':
            cipher[i] = random.choice(string.ascii_letters)
    return ''.join(cipher)

def defoe_decrypt(ciphertext: str, key: str) -> str:
    if key.lower() == "even":
        message = [ciphertext[i] for i in range(len(ciphertext)) if i % 2 == 0]
    elif key.lower() == "odd":
        message = [ciphertext[i] for i in range(len(ciphertext)) if i % 2 == 1]
    else:
        raise ValueError("The key must be 'even' or 'odd'.")

    return ''.join(message)

defoe_chain = LLMChain(
    llm=llm,
    prompt=defoe_prompt
)

def defoe_logic(query: str) -> str:
    parsed = defoe_chain.run(query)
    try:
        data = json.loads(parsed)
    except json.JSONDecodeError:
        return f"Sorry, I didn't quite understand. If you're trying to encrypt or decrypt something, please provide the message like this: message = \"your message here\" and the key like this: key = \"your key here\"."
    operation = data.get("operation")
    message = data.get("message")
    keyword = data.get("key")
    if message is None or not any(c.isalpha() for c in message):
        return "Sorry, the message must contain at least one letter for encryption/decryption."
    if not operation or not message or not keyword:
        return f"Sorry, I didn't quite understand. If you're trying to encrypt or decrypt something, please provide the message like this: message = \"your message here\" and the key like this: key = \"your key here\"."
    if operation.lower() == "encrypt":
        return defoe_encrypt(message, keyword)
    elif operation.lower() == "decrypt":
        return defoe_decrypt(message, keyword)
    else:
        return f"Sorry, I didn't quite understand. If you're trying to encrypt or decrypt something, please provide the message like this: message = \"your message here\" and the key like this: key = \"your key here\"."



# МЕТОД ТРИТЕМІЯ



def tritemius_encrypt(plaintext: str) -> str:
    encrypted = []
    for index, char in enumerate(plaintext):
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = index % 26
            encrypted.append(chr((ord(char) - base + shift) % 26 + base))
        else:
            encrypted.append(char)
    return ''.join(encrypted)

def tritemius_decrypt(ciphertext: str) -> str:
    decrypted = []
    for index, char in enumerate(ciphertext):
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = index % 26
            decrypted.append(chr((ord(char) - base - shift) % 26 + base))
        else:
            decrypted.append(char)
    return ''.join(decrypted)

tritemius_chain = LLMChain(
    llm=llm,
    prompt=tritemius_prompt
)

def tritemius_logic(query: str) -> str:
    parsed = tritemius_chain.run(query)
    try:
        data = json.loads(parsed)
    except json.JSONDecodeError:
        return "Sorry, I didn't quite understand. Please provide the message like this: message = \"your message here\" and the operation like this: operation = \"encrypt\" or \"decrypt\"."

    operation = data.get("operation")
    message = data.get("message")

    if message is None or not any(c.isalpha() for c in message):
        return "Sorry, the message must contain at least one letter for encryption/decryption."
    if not operation or not message:
        return "Sorry, I didn't quite understand. Please provide the message like this: message = \"your message here\" and the operation like this: operation = \"encrypt\" or \"decrypt\"."

    if operation.lower() == "encrypt":
        return tritemius_encrypt(message)
    elif operation.lower() == "decrypt":
        return tritemius_decrypt(message)
    else:
        return "Sorry, I didn't quite understand. Please provide the message like this: message = \"your message here\" and the operation like this: operation = \"encrypt\" or \"decrypt\"."



# МЕТОД АТБАШ



def atbash_cipher(text: str) -> str:
    result = []
    for char in text:
        if char.isalpha():
            if char.isupper():
                result.append(chr(ord('Z') - (ord(char) - ord('A'))))
            else:
                result.append(chr(ord('z') - (ord(char) - ord('a'))))
        else:
            result.append(char)
    return ''.join(result)

atbash_chain = LLMChain(
    llm=llm,
    prompt=atbash_prompt
)

def atbash_logic(query: str) -> str:
    parsed = atbash_chain.run(query)
    try:
        data = json.loads(parsed)
    except json.JSONDecodeError:
        return f"Sorry, I didn't quite understand. If you're trying to encrypt or decrypt something, please provide the message like this: message = \"your message here\"."
    operation = data.get("operation")
    message = data.get("message")
    if message is None or not any(c.isalpha() for c in message):
        return f"Sorry, I didn't quite understand. If you're trying to encrypt or decrypt something, please provide the message like this: message = \"your message here\"."
    if not operation or not message:
        return f"Sorry, I didn't quite understand. If you're trying to encrypt or decrypt something, please provide the message like this: message = \"your message here\"."
    if operation.lower() in ["encrypt", "decrypt"]:
        return atbash_cipher(message)
    else:
        return f"Sorry, I didn't quite understand. If you're trying to encrypt or decrypt something, please provide the message like this: message = \"your message here\"."