import base64
import hashlib
from cryptography.fernet import Fernet
from typing import Union

class CryptoManager:
    def __init__(self):
        self.fernet = None

    def generate_key_from_password(self, master_password: str) -> bytes:
        """Genera una clave Fernet a partir de la contraseña maestra."""
        # Usa SHA-256 para crear una clave de 32 bytes a partir de la contraseña
        key = hashlib.sha256(master_password.encode()).digest()
        # Codifica la clave en base64 (requerido por Fernet)
        return base64.urlsafe_b64encode(key)

    def initialize_encryption(self, master_password: str) -> None:
        """Inicializa el sistema de encriptación con la contraseña maestra."""
        key = self.generate_key_from_password(master_password)
        self.fernet = Fernet(key)

    def encrypt_data(self, data: str) -> bytes:
        """Encripta una cadena de texto."""
        if not self.fernet:
            raise ValueError("Encryption not initialized")
        return self.fernet.encrypt(data.encode())

    def decrypt_data(self, encrypted_data: bytes) -> str:
        """Desencripta datos encriptados."""
        if not self.fernet:
            raise ValueError("Encryption not initialized")
        return self.fernet.decrypt(encrypted_data).decode()

    def hash_password(self, password: str) -> str:
        """Genera un hash seguro de la contraseña."""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verifica si una contraseña coincide con su hash."""
        return self.hash_password(password) == hashed_password

    def check_password_strength(self, password: str) -> dict:
        """Evalúa la fortaleza de una contraseña."""
        score = 0
        feedback = []

        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
        else:
            feedback.append("La contraseña debe tener al menos 8 caracteres")

        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append("Incluye al menos una letra mayúscula")

        if any(c.islower() for c in password):
            score += 1
        else:
            feedback.append("Incluye al menos una letra minúscula")

        if any(c.isdigit() for c in password):
            score += 1
        else:
            feedback.append("Incluye al menos un número")

        if any(not c.isalnum() for c in password):
            score += 1
        else:
            feedback.append("Incluye al menos un carácter especial")

        strength = {
            0: "Muy débil",
            1: "Débil",
            2: "Regular",
            3: "Buena",
            4: "Fuerte",
            5: "Muy fuerte"
        }.get(score, "Muy débil")

        return {
            "score": score,
            "strength": strength,
            "feedback": feedback
        } 