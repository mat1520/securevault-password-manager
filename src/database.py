import sqlite3
import os
from typing import List, Dict, Optional
from crypto_utils import CryptoManager

class DatabaseManager:
    def __init__(self, crypto_manager: CryptoManager):
        self.crypto_manager = crypto_manager
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "vault.db")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_database()

    def init_database(self):
        """Inicializa la base de datos y crea las tablas necesarias."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS credentials (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        website TEXT NOT NULL,
                        username TEXT NOT NULL,
                        encrypted_password BLOB NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
        except Exception as e:
            print(f"Error al inicializar la base de datos: {e}")
            raise

    def add_credential(self, website: str, username: str, password: str) -> bool:
        """Agrega una nueva credencial a la base de datos."""
        try:
            # Verificar que la encriptación está inicializada
            if not self.crypto_manager or not self.crypto_manager.fernet:
                print("Error: La encriptación no está inicializada")
                raise ValueError("La encriptación no está inicializada correctamente")

            # Intentar encriptar la contraseña
            try:
                encrypted_password = self.crypto_manager.encrypt_data(password)
            except Exception as e:
                print(f"Error al encriptar la contraseña: {e}")
                raise ValueError(f"Error al encriptar la contraseña: {str(e)}")

            # Intentar guardar en la base de datos
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO credentials (website, username, encrypted_password)
                    VALUES (?, ?, ?)
                ''', (website, username, encrypted_password))
                conn.commit()
            return True
        except Exception as e:
            print(f"Error al agregar credencial: {e}")
            raise ValueError(f"Error al guardar la credencial: {str(e)}")

    def get_credentials(self) -> List[Dict]:
        """Obtiene todas las credenciales almacenadas."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id, website, username, encrypted_password FROM credentials')
                rows = cursor.fetchall()
                
                credentials = []
                for row in rows:
                    try:
                        decrypted_password = self.crypto_manager.decrypt_data(row[3])
                        credentials.append({
                            'id': row[0],
                            'website': row[1],
                            'username': row[2],
                            'password': decrypted_password
                        })
                    except Exception as e:
                        print(f"Error al desencriptar contraseña: {e}")
                        continue
                return credentials
        except Exception as e:
            print(f"Error al obtener credenciales: {e}")
            return []

    def update_credential(self, credential_id: int, website: str, username: str, password: str) -> bool:
        """Actualiza una credencial existente."""
        try:
            # Verificar que la encriptación está inicializada
            if not self.crypto_manager or not self.crypto_manager.fernet:
                print("Error: La encriptación no está inicializada")
                raise ValueError("La encriptación no está inicializada correctamente")

            # Intentar encriptar la contraseña
            try:
                encrypted_password = self.crypto_manager.encrypt_data(password)
            except Exception as e:
                print(f"Error al encriptar la contraseña: {e}")
                raise ValueError(f"Error al encriptar la contraseña: {str(e)}")

            # Intentar actualizar en la base de datos
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE credentials 
                    SET website = ?, username = ?, encrypted_password = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (website, username, encrypted_password, credential_id))
                conn.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar credencial: {e}")
            raise ValueError(f"Error al actualizar la credencial: {str(e)}")

    def delete_credential(self, credential_id: int) -> bool:
        """Elimina una credencial de la base de datos."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM credentials WHERE id = ?', (credential_id,))
                conn.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar credencial: {e}")
            return False

    def search_credentials(self, query: str) -> List[Dict]:
        """Busca credenciales que coincidan con la consulta."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                search_query = f"%{query}%"
                cursor.execute('''
                    SELECT id, website, username, encrypted_password 
                    FROM credentials 
                    WHERE website LIKE ? OR username LIKE ?
                ''', (search_query, search_query))
                rows = cursor.fetchall()
                
                credentials = []
                for row in rows:
                    try:
                        decrypted_password = self.crypto_manager.decrypt_data(row[3])
                        credentials.append({
                            'id': row[0],
                            'website': row[1],
                            'username': row[2],
                            'password': decrypted_password
                        })
                    except Exception as e:
                        print(f"Error al desencriptar contraseña: {e}")
                        continue
                return credentials
        except Exception as e:
            print(f"Error al buscar credenciales: {e}")
            return [] 