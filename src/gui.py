import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import pyperclip
import random
import string
from typing import Callable, Optional
from PIL import Image
import os
from crypto_utils import CryptoManager
from vault import PasswordVault
from auth import AuthManager
from database import DatabaseManager

class SecureVaultGUI:
    def __init__(self):
        self.crypto_manager = CryptoManager()
        self.auth_manager = AuthManager(self.crypto_manager)
        self.db_manager = None
        self.vault = None
        self.password_vars = {}  # Para manejar la visibilidad de las contraseñas

        # Configuración de tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Ventana principal
        self.root = ctk.CTk()
        self.root.title("SecureVault")
        self.root.geometry("1200x800")  # Ventana más grande por defecto
        self.root.minsize(1000, 600)

        # Centrar la ventana en la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 1200) // 2
        y = (screen_height - 800) // 2
        self.root.geometry(f"1200x800+{x}+{y}")

        # Cargar el logo
        try:
            logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Logo.ps.png")
            self.logo_image = ctk.CTkImage(
                light_image=Image.open(logo_path),
                dark_image=Image.open(logo_path),
                size=(200, 200)  # Logo más grande
            )
            self.logo_small = ctk.CTkImage(
                light_image=Image.open(logo_path),
                dark_image=Image.open(logo_path),
                size=(100, 100)  # Versión pequeña para el sidebar
            )
        except Exception as e:
            print(f"Error al cargar el logo: {e}")
            self.logo_image = None
            self.logo_small = None

        # Variables
        self.current_frame = None
        self.setup_login_frame()

    def setup_login_frame(self):
        """Configura la pantalla de inicio de sesión."""
        if self.current_frame:
            self.current_frame.destroy()

        frame = ctk.CTkFrame(self.root)
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

        # Contenedor central
        center_frame = ctk.CTkFrame(frame, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Logo y título
        if self.logo_image:
            logo_label = ctk.CTkLabel(
                center_frame,
                image=self.logo_image,
                text=""
            )
            logo_label.pack(pady=(0, 30))

        title = ctk.CTkLabel(
            center_frame,
            text="SecureVault",
            font=("Roboto", 48, "bold"),  # Título más grande
            text_color="#00FFE0"  # Color cyan más brillante
        )
        title.pack(pady=(0, 10))
        
        subtitle = ctk.CTkLabel(
            center_frame,
            text="Tu gestor de contraseñas seguro",
            font=("Roboto", 16),
            text_color="#888888"
        )
        subtitle.pack(pady=(0, 40))

        # Campo de contraseña con mejor estilo
        password_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        password_frame.pack(pady=20)

        password_label = ctk.CTkLabel(
            password_frame,
            text="Contraseña Maestra:",
            font=("Roboto", 14, "bold"),
            text_color="#00FFE0"
        )
        password_label.pack()

        self.password_entry = ctk.CTkEntry(
            password_frame,
            show="•",
            width=400,  # Entrada más ancha
            height=45,  # Entrada más alta
            font=("Roboto", 14),
            placeholder_text="Ingresa tu contraseña maestra"
        )
        self.password_entry.pack(pady=10)

        # Botones con mejor estilo
        button_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        button_frame.pack(pady=20)

        login_button = ctk.CTkButton(
            button_frame,
            text="Iniciar Sesión",
            command=self.handle_login,
            width=200,
            height=45,
            font=("Roboto", 14, "bold"),
            fg_color="#00FFE0",
            text_color="black",
            hover_color="#00CCB4"
        )
        login_button.pack(pady=10)

        register_button = ctk.CTkButton(
            button_frame,
            text="Registrarse",
            command=self.handle_register,
            width=200,
            height=45,
            font=("Roboto", 14, "bold"),
            fg_color="#333333",
            hover_color="#444444"
        )
        register_button.pack(pady=10)

        # Botón de recuperación de contraseña
        forgot_button = ctk.CTkButton(
            button_frame,
            text="¿Olvidaste tu contraseña?",
            command=self.show_reset_password_dialog,
            width=200,
            height=35,
            font=("Roboto", 12),
            fg_color="transparent",
            hover_color="#2d2d2d",
            text_color="#00FFE0"
        )
        forgot_button.pack(pady=5)

    def show_reset_password_dialog(self):
        """Muestra el diálogo para reiniciar la contraseña maestra."""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Recuperar Contraseña")
        dialog.geometry("450x500")
        dialog.resizable(False, False)  # Hacer la ventana no redimensionable
        
        # Configurar el tema del diálogo
        dialog.configure(fg_color="#1a1a1a")
        
        # Centrar el diálogo
        dialog.update_idletasks()
        width = 450
        height = 500
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.focus_set()

        # Contenedor principal con padding
        main_frame = ctk.CTkFrame(dialog, fg_color="#1a1a1a")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Logo pequeño en la parte superior
        if self.logo_small:
            logo_label = ctk.CTkLabel(
                main_frame,
                image=self.logo_small,
                text=""
            )
            logo_label.pack(pady=(0, 20))

        # Título
        title = ctk.CTkLabel(
            main_frame,
            text="Recuperar Contraseña",
            font=("Roboto", 24, "bold"),
            text_color="#00FFE0"
        )
        title.pack(pady=(0, 20))

        # Instrucciones
        instructions = ctk.CTkLabel(
            main_frame,
            text="Para recuperar tu contraseña, ingresa el código\nde recuperación y tu nueva contraseña.",
            font=("Roboto", 13),
            justify="center",
            text_color="#FFFFFF"
        )
        instructions.pack(pady=(0, 30))

        # Campo para el código de recuperación
        code_label = ctk.CTkLabel(
            main_frame,
            text="Código de recuperación:",
            font=("Roboto", 13, "bold"),
            text_color="#00FFE0"
        )
        code_label.pack(anchor="w", pady=(0, 5))
        
        code_entry = ctk.CTkEntry(
            main_frame,
            width=390,
            height=40,
            font=("Roboto", 13),
            placeholder_text="Ingresa el código de recuperación",
            fg_color="#2d2d2d",
            border_color="#00FFE0",
            border_width=1
        )
        code_entry.pack(pady=(0, 20))

        # Campo para la nueva contraseña
        new_pass_label = ctk.CTkLabel(
            main_frame,
            text="Nueva contraseña:",
            font=("Roboto", 13, "bold"),
            text_color="#00FFE0"
        )
        new_pass_label.pack(anchor="w", pady=(0, 5))
        
        new_pass_entry = ctk.CTkEntry(
            main_frame,
            show="•",
            width=390,
            height=40,
            font=("Roboto", 13),
            placeholder_text="Ingresa tu nueva contraseña",
            fg_color="#2d2d2d",
            border_color="#00FFE0",
            border_width=1
        )
        new_pass_entry.pack(pady=(0, 30))

        # Botón para reiniciar
        reset_btn = ctk.CTkButton(
            main_frame,
            text="Restablecer Contraseña",
            command=lambda: self.handle_password_reset(
                code_entry.get(),
                new_pass_entry.get(),
                dialog
            ),
            width=390,
            height=45,
            font=("Roboto", 14, "bold"),
            fg_color="#00FFE0",
            text_color="black",
            hover_color="#00CCB4"
        )
        reset_btn.pack(pady=(0, 20))

        # Botón para cancelar
        cancel_btn = ctk.CTkButton(
            main_frame,
            text="Cancelar",
            command=dialog.destroy,
            width=390,
            height=45,
            font=("Roboto", 14, "bold"),
            fg_color="#333333",
            hover_color="#444444"
        )
        cancel_btn.pack()

    def handle_password_reset(self, code: str, new_password: str, dialog: ctk.CTkToplevel):
        """Maneja el proceso de reinicio de contraseña."""
        if not code or not new_password:
            messagebox.showerror("Error", "Por favor completa todos los campos")
            return

        try:
            if code == "admin123":
                # Verificar la fortaleza de la nueva contraseña
                password_strength = self.crypto_manager.check_password_strength(new_password)
                if password_strength["score"] < 3:
                    messagebox.showerror(
                        "Error",
                        "La contraseña es demasiado débil.\n" + "\n".join(password_strength["feedback"])
                    )
                    return

                # Reiniciar los datos del usuario
                self.auth_manager.reset_user_data(new_password)
                
                # Crear un nuevo vault vacío
                self.vault = PasswordVault(self.crypto_manager)
                self.vault.credentials = []
                self.vault.save_vault()
                
                messagebox.showinfo(
                    "Éxito",
                    "Contraseña reiniciada correctamente.\nPor favor, inicia sesión con tu nueva contraseña."
                )
                dialog.destroy()
                self.setup_login_frame()
            else:
                messagebox.showerror("Error", "Código de recuperación inválido")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def setup_main_frame(self):
        """Configura la pantalla principal con el dashboard."""
        if self.current_frame:
            self.current_frame.destroy()

        # Frame principal con dos columnas
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True)
        self.current_frame = main_frame

        # Barra lateral con mejor estilo
        sidebar = ctk.CTkFrame(main_frame, width=250, fg_color="#1a1a1a")
        sidebar.pack(side="left", fill="y", padx=0, pady=0)
        sidebar.pack_propagate(False)

        # Logo en el sidebar
        if self.logo_small:
            sidebar_logo = ctk.CTkLabel(
                sidebar,
                image=self.logo_small,
                text=""
            )
            sidebar_logo.pack(pady=20)

        # Título del sidebar
        sidebar_title = ctk.CTkLabel(
            sidebar,
            text="SecureVault",
            font=("Roboto", 20, "bold"),
            text_color="#00FFE0"
        )
        sidebar_title.pack(pady=20)

        # Contenedor para botones del sidebar
        buttons_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        buttons_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Botones de la barra lateral con iconos
        add_btn = ctk.CTkButton(
            buttons_frame,
            text="➕ Agregar Credencial",
            command=self.show_add_credential_dialog,
            height=40,
            font=("Roboto", 12),
            fg_color="#00FFE0",
            text_color="black",
            hover_color="#00CCB4"
        )
        add_btn.pack(pady=5, fill="x")

        view_btn = ctk.CTkButton(
            buttons_frame,
            text="👁️ Ver Credenciales",
            command=self.refresh_credentials,
            height=40,
            font=("Roboto", 12),
            fg_color="#333333",
            hover_color="#444444"
        )
        view_btn.pack(pady=5, fill="x")

        generate_btn = ctk.CTkButton(
            buttons_frame,
            text="🔑 Generar Contraseña",
            command=self.show_password_generator,
            height=40,
            font=("Roboto", 12),
            fg_color="#333333",
            hover_color="#444444"
        )
        generate_btn.pack(pady=5, fill="x")

        # Botón de cerrar sesión en la parte inferior
        logout_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        logout_frame.pack(fill="x", side="bottom", padx=10, pady=10)

        logout_btn = ctk.CTkButton(
            logout_frame,
            text="🚪 Cerrar Sesión",
            command=self.handle_logout,
            height=40,
            font=("Roboto", 12),
            fg_color="#661111",
            hover_color="#801515"
        )
        logout_btn.pack(fill="x")

        # Área principal
        content_frame = ctk.CTkFrame(main_frame, fg_color="#2d2d2d")
        content_frame.pack(side="right", fill="both", expand=True, padx=0, pady=0)

        # Barra superior
        top_bar = ctk.CTkFrame(content_frame, height=60, fg_color="#1a1a1a")
        top_bar.pack(fill="x", padx=0, pady=0)
        top_bar.pack_propagate(False)

        # Barra de búsqueda con mejor estilo
        search_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        search_frame.pack(side="left", fill="y", padx=20)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Buscar credenciales...",
            width=300,
            height=35
        )
        self.search_entry.pack(side="left", padx=(0, 10), pady=12)

        search_btn = ctk.CTkButton(
            search_frame,
            text="Buscar",
            width=100,
            height=35,
            command=self.search_credentials
        )
        search_btn.pack(side="left", pady=12)

        # Lista de credenciales con scroll
        credentials_container = ctk.CTkFrame(content_frame, fg_color="transparent")
        credentials_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Título de la sección
        section_title = ctk.CTkLabel(
            credentials_container,
            text="Tus Credenciales",
            font=("Roboto", 20, "bold"),
            text_color="#00FFE0"
        )
        section_title.pack(anchor="w", pady=(0, 10))

        # Frame scrollable para las credenciales
        self.credentials_frame = ctk.CTkScrollableFrame(
            credentials_container,
            fg_color="transparent"
        )
        self.credentials_frame.pack(fill="both", expand=True)

        # Cargar las credenciales
        self.refresh_credentials()

    def create_credential_card(self, credential: dict) -> ctk.CTkFrame:
        """Crea una tarjeta para mostrar las credenciales con mejor estilo."""
        card = ctk.CTkFrame(self.credentials_frame, fg_color="#2d2d2d", corner_radius=10)
        card.pack(fill="x", padx=10, pady=5)

        # Contenedor principal de la tarjeta
        main_content = ctk.CTkFrame(card, fg_color="transparent")
        main_content.pack(fill="both", expand=True, padx=15, pady=10)

        # Información
        website_label = ctk.CTkLabel(
            main_content,
            text=f"🌐 {credential['website']}",
            font=("Roboto", 14, "bold"),
            text_color="#00FFE0"
        )
        website_label.pack(anchor="w")

        # Frame para usuario y botón de copiar
        username_frame = ctk.CTkFrame(main_content, fg_color="transparent")
        username_frame.pack(fill="x", pady=5)
        
        username_label = ctk.CTkLabel(
            username_frame,
            text=f"👤 Usuario: {credential['username']}",
            font=("Roboto", 12)
        )
        username_label.pack(side="left")
        
        copy_user_btn = ctk.CTkButton(
            username_frame,
            text="📋",
            width=30,
            height=30,
            font=("Roboto", 14),
            fg_color="#404040",
            hover_color="#505050",
            command=lambda: self.copy_to_clipboard(credential['username'])
        )
        copy_user_btn.pack(side="right")

        # Frame para contraseña
        password_frame = ctk.CTkFrame(main_content, fg_color="transparent")
        password_frame.pack(fill="x", pady=5)
        
        self.password_vars[credential['id']] = tk.StringVar(value="•" * 12)
        password_label = ctk.CTkLabel(
            password_frame,
            text="🔑 Contraseña: ",
            font=("Roboto", 12)
        )
        password_label.pack(side="left")
        
        password_display = ctk.CTkLabel(
            password_frame,
            textvariable=self.password_vars[credential['id']],
            font=("Roboto", 12)
        )
        password_display.pack(side="left")

        # Botones para la contraseña
        show_hide_btn = ctk.CTkButton(
            password_frame,
            text="👁️",
            width=30,
            height=30,
            font=("Roboto", 14),
            fg_color="#404040",
            hover_color="#505050",
            command=lambda: self.toggle_password_visibility(credential['id'], credential['password'])
        )
        show_hide_btn.pack(side="right", padx=5)
        
        copy_pass_btn = ctk.CTkButton(
            password_frame,
            text="📋",
            width=30,
            height=30,
            font=("Roboto", 14),
            fg_color="#404040",
            hover_color="#505050",
            command=lambda: self.copy_to_clipboard(credential['password'])
        )
        copy_pass_btn.pack(side="right", padx=5)

        # Contenedor para los botones de acción
        button_frame = ctk.CTkFrame(main_content, fg_color="transparent")
        button_frame.pack(fill="x", pady=(10, 0))

        # Botones con iconos
        edit_btn = ctk.CTkButton(
            button_frame,
            text="✏️ Editar",
            command=lambda: self.show_edit_credential_dialog(credential),
            width=100,
            height=32,
            font=("Roboto", 12),
            fg_color="#00FFE0",
            text_color="black",
            hover_color="#00CCB4"
        )
        edit_btn.pack(side="left", padx=5)

        delete_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Eliminar",
            command=lambda: self.delete_credential(credential['id']),
            width=100,
            height=32,
            font=("Roboto", 12),
            fg_color="#661111",
            hover_color="#801515"
        )
        delete_btn.pack(side="left", padx=5)

        return card

    def toggle_password_visibility(self, credential_id: int, password: str):
        """Alterna la visibilidad de la contraseña."""
        current_value = self.password_vars[credential_id].get()
        if current_value == "•" * 12:
            self.password_vars[credential_id].set(password)
        else:
            self.password_vars[credential_id].set("•" * 12)

    def show_add_credential_dialog(self):
        """Muestra el diálogo para agregar nuevas credenciales."""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Agregar Credencial")
        dialog.geometry("450x650")  # Altura aumentada para acomodar el botón
        dialog.resizable(False, False)
        
        # Configurar el tema del diálogo
        dialog.configure(fg_color="#1a1a1a")
        
        # Centrar el diálogo
        dialog.update_idletasks()
        width = 450
        height = 650
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.focus_set()

        # Contenedor principal con padding
        main_frame = ctk.CTkFrame(dialog, fg_color="#1a1a1a")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Logo pequeño en la parte superior
        if self.logo_small:
            logo_label = ctk.CTkLabel(
                main_frame,
                image=self.logo_small,
                text=""
            )
            logo_label.pack(pady=(0, 20))

        # Título
        title = ctk.CTkLabel(
            main_frame,
            text="Agregar Nueva Credencial",
            font=("Roboto", 24, "bold"),
            text_color="#00FFE0"
        )
        title.pack(pady=(0, 30))

        # Campo Sitio Web
        website_label = ctk.CTkLabel(
            main_frame,
            text="Sitio Web:",
            font=("Roboto", 13, "bold"),
            text_color="#00FFE0"
        )
        website_label.pack(anchor="w")
        
        website_entry = ctk.CTkEntry(
            main_frame,
            width=390,
            height=40,
            font=("Roboto", 13),
            placeholder_text="Ejemplo: www.ejemplo.com",
            fg_color="#2d2d2d",
            border_color="#00FFE0",
            border_width=1
        )
        website_entry.pack(pady=(5, 15))

        # Campo Usuario
        username_label = ctk.CTkLabel(
            main_frame,
            text="Usuario:",
            font=("Roboto", 13, "bold"),
            text_color="#00FFE0"
        )
        username_label.pack(anchor="w")
        
        username_entry = ctk.CTkEntry(
            main_frame,
            width=390,
            height=40,
            font=("Roboto", 13),
            placeholder_text="Ingresa tu nombre de usuario",
            fg_color="#2d2d2d",
            border_color="#00FFE0",
            border_width=1
        )
        username_entry.pack(pady=(5, 15))

        # Campo Contraseña
        password_label = ctk.CTkLabel(
            main_frame,
            text="Contraseña:",
            font=("Roboto", 13, "bold"),
            text_color="#00FFE0"
        )
        password_label.pack(anchor="w")
        
        # Frame para contraseña y botones
        password_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        password_frame.pack(fill="x", pady=(5, 15))
        
        password_entry = ctk.CTkEntry(
            password_frame,
            show="•",
            width=310,
            height=40,
            font=("Roboto", 13),
            placeholder_text="Ingresa o genera una contraseña",
            fg_color="#2d2d2d",
            border_color="#00FFE0",
            border_width=1
        )
        password_entry.pack(side="left")

        # Frame para botones de contraseña
        pass_buttons_frame = ctk.CTkFrame(password_frame, fg_color="transparent")
        pass_buttons_frame.pack(side="right")

        show_hide_btn = ctk.CTkButton(
            pass_buttons_frame,
            text="🔒",
            width=35,
            height=40,
            font=("Roboto", 16),
            fg_color="#2d2d2d",
            hover_color="#404040",
            command=lambda: password_entry.configure(show="" if password_entry.cget("show") == "•" else "•")
        )
        show_hide_btn.pack(side="left", padx=5)

        copy_btn = ctk.CTkButton(
            pass_buttons_frame,
            text="📋",
            width=35,
            height=40,
            font=("Roboto", 16),
            fg_color="#2d2d2d",
            hover_color="#404040",
            command=lambda: self.copy_to_clipboard(password_entry.get())
        )
        copy_btn.pack(side="left")

        # Botón para generar contraseña
        generate_btn = ctk.CTkButton(
            main_frame,
            text="🔑 Generar Contraseña Segura",
            command=lambda: password_entry.delete(0, 'end') or password_entry.insert(0, self.generate_password()),
            width=390,
            height=40,
            font=("Roboto", 13),
            fg_color="#2d2d2d",
            hover_color="#404040"
        )
        generate_btn.pack(pady=(0, 20))

        # Separador
        separator = ctk.CTkFrame(main_frame, height=2, fg_color="#333333")
        separator.pack(fill="x", pady=20)

        # Botones de acción
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(0, 10))

        def animate_save():
            if not website_entry.get() or not username_entry.get() or not password_entry.get():
                messagebox.showerror("Error", "Por favor completa todos los campos")
                return
            
            save_btn.configure(
                text="💾 Guardando...",
                state="disabled",
                fg_color="#808080"
            )
            dialog.after(500, lambda: save_and_close())

        def save_and_close():
            if self.add_credential(
                website_entry.get(),
                username_entry.get(),
                password_entry.get(),
                dialog
            ):
                save_btn.configure(
                    text="✅ ¡Guardado!",
                    fg_color="#00CC00"
                )
                dialog.after(1000, dialog.destroy)
            else:
                save_btn.configure(
                    text="💾 Guardar Credencial",
                    state="normal",
                    fg_color="#00FFE0"
                )

        # Botón grande de guardar
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 Guardar Credencial",
            command=animate_save,
            width=390,
            height=50,  # Botón más alto
            font=("Roboto", 16, "bold"),  # Fuente más grande
            fg_color="#00FFE0",
            text_color="black",
            hover_color="#00CCB4",
            corner_radius=10
        )
        save_btn.pack(pady=(0, 10))

        # Botón de cancelar
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ Cancelar",
            command=dialog.destroy,
            width=390,
            height=45,
            font=("Roboto", 14, "bold"),
            fg_color="#333333",
            hover_color="#444444"
        )
        cancel_btn.pack()

        # Atajo de teclado para guardar (Ctrl+S)
        dialog.bind('<Control-s>', lambda e: animate_save())
        dialog.bind('<Return>', lambda e: animate_save())

        # Dar foco al primer campo
        website_entry.focus()

    def show_password_generator(self):
        """Muestra el diálogo del generador de contraseñas."""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Generador de Contraseñas")
        dialog.geometry("450x600")
        dialog.resizable(False, False)
        dialog.configure(fg_color="#1a1a1a")
        
        # Centrar el diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"450x600+{x}+{y}")
        
        dialog.transient(self.root)
        dialog.grab_set()

        # Contenedor principal
        main_frame = ctk.CTkFrame(dialog, fg_color="#1a1a1a")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Logo y título
        if self.logo_small:
            logo_label = ctk.CTkLabel(
                main_frame,
                image=self.logo_small,
                text=""
            )
            logo_label.pack(pady=(0, 20))

        title = ctk.CTkLabel(
            main_frame,
            text="Generador de Contraseñas",
            font=("Roboto", 24, "bold"),
            text_color="#00FFE0"
        )
        title.pack(pady=(0, 30))

        # Opciones
        options_frame = ctk.CTkFrame(main_frame, fg_color="#2d2d2d")
        options_frame.pack(fill="x", pady=(0, 20), padx=10)

        # Longitud
        length_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        length_frame.pack(fill="x", padx=20, pady=10)
        
        length_label = ctk.CTkLabel(
            length_frame,
            text="Longitud:",
            font=("Roboto", 13, "bold"),
            text_color="#00FFE0"
        )
        length_label.pack(side="left")

        length_value = tk.StringVar(value="16")
        length_entry = ctk.CTkEntry(
            length_frame,
            width=70,
            textvariable=length_value,
            font=("Roboto", 13),
            fg_color="#404040"
        )
        length_entry.pack(side="right")

        # Checkboxes
        use_upper = tk.BooleanVar(value=True)
        upper_check = ctk.CTkCheckBox(
            options_frame,
            text="Mayúsculas (A-Z)",
            variable=use_upper,
            font=("Roboto", 13),
            text_color="#FFFFFF",
            fg_color="#00FFE0",
            hover_color="#00CCB4"
        )
        upper_check.pack(pady=10, padx=20, anchor="w")

        use_lower = tk.BooleanVar(value=True)
        lower_check = ctk.CTkCheckBox(
            options_frame,
            text="Minúsculas (a-z)",
            variable=use_lower,
            font=("Roboto", 13),
            text_color="#FFFFFF",
            fg_color="#00FFE0",
            hover_color="#00CCB4"
        )
        lower_check.pack(pady=10, padx=20, anchor="w")

        use_digits = tk.BooleanVar(value=True)
        digits_check = ctk.CTkCheckBox(
            options_frame,
            text="Números (0-9)",
            variable=use_digits,
            font=("Roboto", 13),
            text_color="#FFFFFF",
            fg_color="#00FFE0",
            hover_color="#00CCB4"
        )
        digits_check.pack(pady=10, padx=20, anchor="w")

        use_special = tk.BooleanVar(value=True)
        special_check = ctk.CTkCheckBox(
            options_frame,
            text="Caracteres Especiales (!@#$%^&*)",
            variable=use_special,
            font=("Roboto", 13),
            text_color="#FFFFFF",
            fg_color="#00FFE0",
            hover_color="#00CCB4"
        )
        special_check.pack(pady=10, padx=20, anchor="w")

        # Campo para mostrar la contraseña generada
        result_frame = ctk.CTkFrame(main_frame, fg_color="#2d2d2d")
        result_frame.pack(fill="x", pady=20, padx=10)

        password_var = tk.StringVar()
        password_entry = ctk.CTkEntry(
            result_frame,
            textvariable=password_var,
            width=350,
            height=40,
            font=("Roboto", 14),
            fg_color="#404040"
        )
        password_entry.pack(pady=20, padx=20)

        # Botones
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=20)

        generate_btn = ctk.CTkButton(
            buttons_frame,
            text="🔄 Generar Nueva Contraseña",
            command=lambda: password_var.set(
                self.generate_password(
                    int(length_value.get()),
                    use_upper.get(),
                    use_lower.get(),
                    use_digits.get(),
                    use_special.get()
                )
            ),
            width=350,
            height=40,
            font=("Roboto", 14, "bold"),
            fg_color="#00FFE0",
            text_color="black",
            hover_color="#00CCB4"
        )
        generate_btn.pack(pady=5)

        copy_btn = ctk.CTkButton(
            buttons_frame,
            text="📋 Copiar al Portapapeles",
            command=lambda: self.copy_to_clipboard(password_var.get()),
            width=350,
            height=40,
            font=("Roboto", 14),
            fg_color="#404040",
            hover_color="#505050"
        )
        copy_btn.pack(pady=5)

        close_btn = ctk.CTkButton(
            buttons_frame,
            text="✖️ Cerrar",
            command=dialog.destroy,
            width=350,
            height=40,
            font=("Roboto", 14),
            fg_color="#333333",
            hover_color="#444444"
        )
        close_btn.pack(pady=5)

        # Generar una contraseña inicial
        password_var.set(self.generate_password())

    def generate_password(
        self,
        length: int = 16,
        use_upper: bool = True,
        use_lower: bool = True,
        use_digits: bool = True,
        use_special: bool = True
    ) -> str:
        """Genera una contraseña aleatoria según los criterios especificados."""
        chars = ""
        if use_upper:
            chars += string.ascii_uppercase
        if use_lower:
            chars += string.ascii_lowercase
        if use_digits:
            chars += string.digits
        if use_special:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        if not chars:
            chars = string.ascii_letters + string.digits

        return ''.join(random.choice(chars) for _ in range(length))

    def copy_to_clipboard(self, text: str):
        """Copia el texto al portapapeles."""
        pyperclip.copy(text)
        messagebox.showinfo("Éxito", "Copiado al portapapeles")

    def handle_login(self):
        """Maneja el proceso de inicio de sesión."""
        password = self.password_entry.get()
        try:
            if self.auth_manager.login(password):
                self.crypto_manager.initialize_encryption(password)
                self.db_manager = DatabaseManager(self.crypto_manager)
                self.setup_main_frame()
            else:
                messagebox.showerror("Error", "Contraseña incorrecta")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def handle_register(self):
        """Maneja el proceso de registro."""
        password = self.password_entry.get()
        try:
            # Verificar la fortaleza de la contraseña
            password_strength = self.crypto_manager.check_password_strength(password)
            if password_strength["score"] < 3:
                messagebox.showerror(
                    "Error",
                    "La contraseña es demasiado débil.\n" + "\n".join(password_strength["feedback"])
                )
                return

            if self.auth_manager.register_user(password):
                # Inicializar el administrador de base de datos
                self.crypto_manager.initialize_encryption(password)
                self.db_manager = DatabaseManager(self.crypto_manager)
                
                messagebox.showinfo(
                    "Éxito",
                    "Usuario registrado correctamente.\nPor favor, guarda tu contraseña maestra en un lugar seguro."
                )
                self.handle_login()
            else:
                messagebox.showerror("Error", "Ya existe un usuario registrado")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def handle_logout(self):
        """Maneja el proceso de cierre de sesión."""
        self.vault = None
        self.setup_login_frame()

    def refresh_credentials(self):
        """Actualiza la lista de credenciales mostradas."""
        # Limpia el frame de credenciales
        for widget in self.credentials_frame.winfo_children():
            widget.destroy()

        # Obtiene y muestra las credenciales
        credentials = self.db_manager.get_credentials()
        for cred in credentials:
            self.create_credential_card(cred)

    def add_credential(self, website: str, username: str, password: str, dialog: ctk.CTkToplevel) -> bool:
        """Agrega nuevas credenciales a la base de datos."""
        if not website or not username or not password:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return False

        try:
            if self.db_manager.add_credential(website, username, password):
                self.refresh_credentials()
                return True
            else:
                messagebox.showerror("Error", "No se pudo guardar la credencial")
                return False
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
            return False

    def delete_credential(self, credential_id: int):
        """Elimina credenciales de la base de datos."""
        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta credencial?"):
            if self.db_manager.delete_credential(credential_id):
                self.refresh_credentials()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la credencial")

    def search_credentials(self):
        """Busca credenciales según el texto ingresado."""
        query = self.search_entry.get().strip()
        for widget in self.credentials_frame.winfo_children():
            widget.destroy()

        if query:
            credentials = self.db_manager.search_credentials(query)
        else:
            credentials = self.db_manager.get_credentials()
            
        for cred in credentials:
            self.create_credential_card(cred)

    def run(self):
        """Inicia la aplicación."""
        self.root.mainloop()

if __name__ == "__main__":
    app = SecureVaultGUI()
    app.run() 