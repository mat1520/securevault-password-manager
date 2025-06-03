import json
import os
from typing import Optional, Dict
from crypto_utils import CryptoManager

class AuthManager:
    def __init__(self, crypto_manager: CryptoManager):
        self.crypto_manager = crypto_manager
        self.auth_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "auth.json")
        self.max_login_attempts = 3
        self.current_attempts = 0
        self.user_data: Optional[Dict] = None
        # Asegurar que el directorio data existe
        os.makedirs(os.path.dirname(self.auth_file), exist_ok=True)

    def load_user_data(self) -> None:
        """Carga los datos del usuario desde el archivo."""
        if os.path.exists(self.auth_file):
            with open(self.auth_file, "r") as f:
                self.user_data = json.load(f)
        else:
            self.user_data = None

    def save_user_data(self) -> None:
        """Guarda los datos del usuario en el archivo."""
        os.makedirs(os.path.dirname(self.auth_file), exist_ok=True)
        with open(self.auth_file, "w") as f:
            json.dump(self.user_data, f)

    def register_user(self, master_password: str) -> bool:
        """Registra un nuevo usuario con la contraseña maestra."""
        if self.user_data is not None:
            return False

        password_strength = self.crypto_manager.check_password_strength(master_password)
        if password_strength["score"] < 3:
            raise ValueError("La contraseña maestra es demasiado débil")

        self.user_data = {
            "master_password_hash": self.crypto_manager.hash_password(master_password),
            "locked": False,
            "login_attempts": 0
        }
        self.save_user_data()
        return True

    def login(self, master_password: str) -> bool:
        """Intenta iniciar sesión con la contraseña maestra."""
        self.load_user_data()
        
        if self.user_data is None:
            raise ValueError("No hay usuario registrado")

        if self.user_data["locked"]:
            raise ValueError("La cuenta está bloqueada por múltiples intentos fallidos")

        if self.crypto_manager.verify_password(master_password, self.user_data["master_password_hash"]):
            self.user_data["login_attempts"] = 0
            self.save_user_data()
            self.crypto_manager.initialize_encryption(master_password)
            return True

        self.user_data["login_attempts"] += 1
        if self.user_data["login_attempts"] >= self.max_login_attempts:
            self.user_data["locked"] = True
        self.save_user_data()
        return False

    def unlock_account(self, master_password: str) -> bool:
        """Desbloquea una cuenta bloqueada si la contraseña es correcta."""
        if not self.user_data or not self.user_data["locked"]:
            return False

        if self.crypto_manager.verify_password(master_password, self.user_data["master_password_hash"]):
            self.user_data["locked"] = False
            self.user_data["login_attempts"] = 0
            self.save_user_data()
            return True
        return False

    def change_master_password(self, current_password: str, new_password: str) -> bool:
        """Cambia la contraseña maestra."""
        if not self.user_data:
            return False

        if not self.crypto_manager.verify_password(current_password, self.user_data["master_password_hash"]):
            return False

        password_strength = self.crypto_manager.check_password_strength(new_password)
        if password_strength["score"] < 3:
            raise ValueError("La nueva contraseña maestra es demasiado débil")

        self.user_data["master_password_hash"] = self.crypto_manager.hash_password(new_password)
        self.save_user_data()
        return True

    def reset_user_data(self, new_password: str) -> None:
        """Reinicia los datos del usuario con una nueva contraseña maestra."""
        # Verificar la fortaleza de la nueva contraseña
        password_strength = self.crypto_manager.check_password_strength(new_password)
        if password_strength["score"] < 3:
            raise ValueError("La nueva contraseña maestra es demasiado débil")

        # Limpiar archivos existentes
        vault_file = os.path.join("data", "vault.enc")
        if os.path.exists(vault_file):
            os.remove(vault_file)

        # Crear nuevos datos de usuario
        self.user_data = {
            "master_password_hash": self.crypto_manager.hash_password(new_password),
            "locked": False,
            "login_attempts": 0
        }

        # Guardar los nuevos datos
        self.save_user_data()

        # Inicializar la encriptación con la nueva contraseña
        self.crypto_manager.initialize_encryption(new_password) 