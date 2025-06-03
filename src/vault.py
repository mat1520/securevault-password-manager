import json
import os
from typing import Dict, List, Optional
from crypto_utils import CryptoManager

class PasswordVault:
    def __init__(self, crypto_manager: CryptoManager):
        self.crypto_manager = crypto_manager
        self.vault_file = os.path.join("data", "vault.enc")
        self.credentials: List[Dict] = []

    def load_vault(self) -> None:
        """Carga las credenciales encriptadas desde el archivo."""
        if os.path.exists(self.vault_file):
            with open(self.vault_file, "rb") as f:
                encrypted_data = f.read()
                if encrypted_data:
                    decrypted_data = self.crypto_manager.decrypt_data(encrypted_data)
                    self.credentials = json.loads(decrypted_data)
                else:
                    self.credentials = []
        else:
            self.credentials = []

    def save_vault(self) -> None:
        """Guarda las credenciales encriptadas en el archivo."""
        encrypted_data = self.crypto_manager.encrypt_data(json.dumps(self.credentials))
        os.makedirs(os.path.dirname(self.vault_file), exist_ok=True)
        with open(self.vault_file, "wb") as f:
            f.write(encrypted_data)

    def add_credentials(self, website: str, username: str, password: str) -> None:
        """Agrega nuevas credenciales al vault."""
        credential = {
            "id": len(self.credentials) + 1,
            "website": website,
            "username": username,
            "password": password
        }
        self.credentials.append(credential)
        self.save_vault()

    def get_credentials(self, website: Optional[str] = None) -> List[Dict]:
        """Obtiene todas las credenciales o filtra por sitio web."""
        if website:
            return [c for c in self.credentials if website.lower() in c["website"].lower()]
        return self.credentials

    def update_credentials(self, credential_id: int, website: str, username: str, password: str) -> bool:
        """Actualiza credenciales existentes."""
        for cred in self.credentials:
            if cred["id"] == credential_id:
                cred.update({
                    "website": website,
                    "username": username,
                    "password": password
                })
                self.save_vault()
                return True
        return False

    def delete_credentials(self, credential_id: int) -> bool:
        """Elimina credenciales por ID."""
        for i, cred in enumerate(self.credentials):
            if cred["id"] == credential_id:
                self.credentials.pop(i)
                self.save_vault()
                return True
        return False

    def search_credentials(self, query: str) -> List[Dict]:
        """Busca credenciales por sitio web o nombre de usuario."""
        query = query.lower()
        return [
            cred for cred in self.credentials
            if query in cred["website"].lower() or query in cred["username"].lower()
        ] 