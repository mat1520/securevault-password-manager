# SecureVault - Gestor de Contraseñas

<div align="center">

![SecureVault Logo](Logo.ps.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)

*Un gestor de contraseñas seguro y moderno desarrollado en Python*

</div>

## 🌟 Características Principales

- 🔐 **Seguridad Avanzada**
  - Encriptación AES-256 para todas las contraseñas
  - Autenticación con contraseña maestra
  - Bloqueo automático después de intentos fallidos
  - Sin almacenamiento de contraseñas en texto plano

- 🎨 **Interfaz Moderna**
  - Diseño intuitivo y amigable
  - Temas oscuro/claro
  - Animaciones fluidas
  - Iconos y elementos visuales modernos

- ⚡ **Funcionalidades**
  - Generador de contraseñas seguras
  - Búsqueda rápida de credenciales
  - Copiar al portapapeles con un clic
  - Mostrar/ocultar contraseñas
  - Edición y eliminación de credenciales

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Sistema operativo: Windows, macOS, o Linux

## 🚀 Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/mat1520/securevault-password-manager.git
   cd securevault-password-manager
   ```

2. **Crear y activar entorno virtual**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Uso

1. **Iniciar la aplicación**
   ```bash
   python src/main.py
   ```

2. **Primer uso**
   - Crear una contraseña maestra segura
   - La contraseña debe incluir:
     - Mínimo 8 caracteres
     - Mayúsculas y minúsculas
     - Números
     - Caracteres especiales

3. **Gestión de Credenciales**
   - **Agregar**: Click en "➕ Agregar Credencial"
   - **Ver**: Click en "👁️ Ver Credenciales"
   - **Buscar**: Usar la barra de búsqueda
   - **Editar/Eliminar**: Botones en cada credencial

4. **Generador de Contraseñas**
   - Click en "🔑 Generar Contraseña"
   - Personalizar longitud y caracteres
   - Copiar al portapapeles automáticamente

## 🔧 Solución de Problemas

### Problemas Comunes

1. **Error al guardar credenciales**
   - Verificar permisos de escritura en la carpeta `data`
   - Asegurar que la base de datos no está bloqueada
   - Reiniciar la aplicación si persiste

2. **Contraseña maestra no funciona**
   - Verificar el bloqueo de mayúsculas
   - Esperar si la cuenta está bloqueada
   - Usar la opción de recuperación si es necesario

3. **Base de datos corrupta**
   - Hacer backup de `data/vault.db`
   - Eliminar y dejar que se recree
   - Restaurar desde backup si es necesario

### Mensajes de Error

| Mensaje | Causa | Solución |
|---------|-------|----------|
| "No se pudo guardar la credencial" | Error de escritura en DB | Verificar permisos |
| "Contraseña incorrecta" | Error de autenticación | Verificar credenciales |
| "Base de datos bloqueada" | Acceso simultáneo | Cerrar otras instancias |

## 🛡️ Seguridad

- Las contraseñas se almacenan usando encriptación AES-256
- La contraseña maestra nunca se guarda, solo su hash
- Datos sensibles protegidos en memoria
- Bloqueo automático por seguridad
- Sin telemetría ni recolección de datos

## 🤝 Contribuir

1. Fork del repositorio
2. Crear rama para feature: `git checkout -b feature/nueva-funcion`
3. Commit cambios: `git commit -am 'Agrega nueva función'`
4. Push a la rama: `git push origin feature/nueva-funcion`
5. Crear Pull Request

### Guía de Estilo

- Seguir PEP 8 para Python
- Documentar funciones y clases
- Mantener coherencia en el diseño UI
- Escribir pruebas unitarias

## 📝 TODO

- [ ] Sincronización en la nube
- [ ] Importar/exportar credenciales
- [ ] Autenticación biométrica
- [ ] Historial de contraseñas
- [ ] Auditoría de seguridad
- [ ] Backup automático

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles

## 👥 Autores

- [@mat1520](https://github.com/mat1520) - Desarrollo inicial

## 🙏 Agradecimientos

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) por el framework UI
- [cryptography](https://github.com/pyca/cryptography) por las funciones de encriptación
- Comunidad de Python por el apoyo

## 📞 Soporte

Para reportar problemas o sugerir mejoras:
1. Abrir un issue en GitHub
2. Describir el problema/sugerencia
3. Incluir pasos para reproducir (si aplica)
4. Agregar capturas de pantalla si es necesario 