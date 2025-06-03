# SecureVault - Gestor de Contraseñas Local Seguro

<div align="center">

![SecureVault Logo](Logo.ps.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)

*Un gestor de contraseñas seguro, local y moderno desarrollado en Python*

</div>

## 🔒 Características de Seguridad

- **Almacenamiento Local**
  - Base de datos SQLite local para máxima privacidad
  - Sin conexión a internet ni almacenamiento en la nube
  - Control total sobre tus datos

- **Encriptación Robusta**
  - Encriptación AES-256 para todas las contraseñas
  - Contraseñas nunca almacenadas en texto plano
  - Salt único para cada hash de contraseña maestra

- **Protección de Acceso**
  - Autenticación con contraseña maestra
  - Bloqueo automático después de intentos fallidos
  - Tiempo de espera progresivo entre intentos

## 💫 Características Principales

- **Interfaz Moderna**
  - Diseño intuitivo y amigable
  - Tema oscuro por defecto
  - Iconos y elementos visuales modernos
  - Interfaz responsive y adaptable

- **Gestión de Credenciales**
  - Agregar/Editar/Eliminar credenciales
  - Búsqueda rápida de credenciales
  - Copiar al portapapeles con un clic
  - Mostrar/ocultar contraseñas

- **Generador de Contraseñas**
  - Generación de contraseñas seguras
  - Opciones personalizables:
    - Longitud ajustable
    - Mayúsculas/minúsculas
    - Números
    - Caracteres especiales

## 🛠️ Requisitos del Sistema

- Python 3.8 o superior
- Sistema operativo:
  - Windows 10/11
  - macOS 10.14+
  - Linux (distribuciones modernas)
- 100 MB de espacio en disco
- 2 GB de RAM (recomendado)

## 📥 Instalación

1. **Clonar el Repositorio**
   ```bash
   git clone https://github.com/yourusername/securevault.git
   cd securevault
   ```

2. **Instalar Dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la Aplicación**
   ```bash
   python src/main.py
   ```

## 🔄 Flujo de Trabajo

### 1. Primer Uso
1. Ejecutar la aplicación
2. Crear una contraseña maestra segura
3. La base de datos se inicializa automáticamente

### 2. Uso Diario
1. Iniciar la aplicación
2. Ingresar contraseña maestra
3. Gestionar credenciales:
   - Agregar nuevas
   - Buscar existentes
   - Editar/eliminar según necesidad

### 3. Agregar Credenciales
1. Clic en "➕ Agregar Credencial"
2. Completar formulario:
   - Sitio web
   - Usuario
   - Contraseña (manual o generada)
3. Guardar cambios

### 4. Buscar y Editar
1. Usar la barra de búsqueda
2. Seleccionar credencial
3. Editar información
4. Guardar cambios

## 🔐 Arquitectura de Seguridad

### Base de Datos Local
- SQLite3 para almacenamiento local
- Archivo de base de datos encriptado
- Sin conexiones externas

### Encriptación
1. **Contraseña Maestra**
   - Hash SHA-256
   - Salt único por instalación
   - Verificación segura

2. **Credenciales**
   - Encriptación AES-256
   - Claves únicas por sesión
   - Datos en memoria limpiados al cerrar

### Protección de Datos
- Limpieza automática del portapapeles
- Bloqueo por inactividad
- Sanitización de entradas

## 🛡️ Medidas de Seguridad Adicionales

1. **Protección contra Ataques**
   - Prevención de inyección SQL
   - Sanitización de entradas
   - Límite de intentos de acceso

2. **Seguridad de Datos**
   - Backups automáticos encriptados
   - Limpieza segura de memoria
   - Protección contra volcados de memoria

3. **Privacidad**
   - Sin telemetría
   - Sin conexiones externas
   - Sin recolección de datos

## 📋 Recomendaciones de Uso

1. **Contraseña Maestra**
   - Usar una contraseña fuerte
   - Cambiarla regularmente
   - No compartirla nunca

2. **Backups**
   - Realizar copias regulares
   - Almacenar en lugar seguro
   - Verificar integridad

3. **Seguridad General**
   - Mantener el sistema actualizado
   - Usar antivirus actualizado
   - Cerrar sesión al terminar

## 🤝 Contribuir

1. Fork del repositorio
2. Crear rama para feature: `git checkout -b feature/nueva-funcion`
3. Commit cambios: `git commit -am 'Agrega nueva función'`
4. Push a la rama: `git push origin feature/nueva-funcion`
5. Crear Pull Request

### Guía de Estilo
- Seguir PEP 8
- Documentar todo el código
- Pruebas unitarias para nuevas funciones

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- Iconos: [Feather Icons](https://feathericons.com)
- UI Framework: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Encriptación: [cryptography](https://cryptography.io)

---

<div align="center">
Desarrollado @mat1520

[Reportar Bug](https://github.com/yourusername/securevault/issues) · [Solicitar Función](https://github.com/yourusername/securevault/issues)
</div> 