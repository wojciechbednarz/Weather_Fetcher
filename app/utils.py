import logging
import os
import re
import json
from dotenv import load_dotenv
from cryptography.fernet import Fernet


load_dotenv()
data = []
logger = logging.getLogger("weather_fetcher")

def encrypt_api_key(api_key) -> bytes:
    cipher_suite = Fernet(os.getenv("ENCRYPTION_KEY").encode())
    encrypted_api_key=cipher_suite.encrypt(api_key.encode())
    return encrypted_api_key

def decrypt_api_key() -> str:
    cipher_suite = Fernet(os.getenv("ENCRYPTION_KEY").encode())
    decrypted_api_key = cipher_suite.decrypt(os.getenv("ENCRYPTED_API_KEY")).decode()
    return decrypted_api_key

def validate_user_input_for_city_name(city_name: str) -> bool:
    pattern = r"^[A-Za-zÀ-ÿ]+(?:[ '-][A-Za-zÀ-ÿ]+)*$"
    return bool(re.match(pattern, city_name))

def save_weather_output_to_file(response, output_file):
    try:
        with open(output_file, "w") as file:
            json.dump(response.json(), file, indent=4)
        logger.info(f"Weather output saved to a file: {output_file}")
    except json.JSONDecodeError as err:
        logger.error(f"Error decoding JSON response: {err}.")
