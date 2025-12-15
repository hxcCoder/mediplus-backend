# MediPlus - Sistema de Gestión Medica Seguro

**Asignatura:** Programación Orientada a Objetos Seguro  
**Sección:** 3  
**Carrera:** Ingeniería en Informática  
**Estudiante:** Benjamin millalonco 
**Fecha de entrega:** 15/12/2025  
**Versión:** 1.0

## Descripcion
MediPlus es un prototipo de sistema de informacion para clinicas de tamaño medio. Su objetivo es reemplazar registros en Excel y formularios en papel, permitiendo gestionar de manera segura usuarios, consultas, recetas, insumos y agenda médica. El sistema utiliza **Python**, **Flask**, **Oracle XE 21c**, y sigue buenas practicas de seguridad y el patrom MVC.

El proyecto fue desarrollado como parte de la asignatura **Programacion Orientada a Objetos Seguro**, aplicando metodologias ágiles y control de roles de usuarios (administrador, médico y paciente).

## Objetivos Específicos
- Registrar usuarios de manera segura a partir de archivos JSON.
- Implementar autenticación con hash de contraseñas.
- Crear un CRUD completo para cada entidad del sistema.
- Presentar menús dinámicos según el tipo de usuario.
- Mostrar valores en pesos chilenos (CLP) de forma consistente.
- Prevenir inyección SQL mediante consultas parametrizadas.
- Almacenar y gestionar la información en Oracle XE 21c.

---

## Introducciin
Actualmente, la clinica MediPlus registra información en planillas y papel, lo que genera pérdida de datos y dificultades en el seguimiento de pacientes. MediPlus busca digitalizar el proceso con un sistema seguro, eficiente y fácil de usar, asegurando integridad de datos y control de acceso.

---
## Requerimientos Detectados

### Funcionales
- Registro de usuarios desde JSON.
- Inicio de sesión seguro.
- CRUD de Usuarios, Pacientes, Médicos, Administradores, Consultas, Recetas, Insumos y Agenda.
- Menús dinámicos por rol.
- Consultas y reportes médicos.

### No Funcionales
- Seguridad de credenciales (hash de contraseñas).
- Prevención de inyección SQL.
- Control de sesión y roles.
- Integridad y consistencia de datos en Oracle XE 21c.
- Facilidad de uso y navegación.

---

## Tecnologias
- Python 3.11+  
- Flask  
- Oracle XE 21c  
- HTML / CSS / JS (Bootstrap opcional)  
- PlantUML (diagrama de clases)  
- Git y GitHub para control de versiones  

---
Descripción de la Solución
-

El sistema sigue arquitectura MVC:

- Models: Representan las entidades (Usuario, Paciente, Medico, Administrador, Receta, Consulta, Insumo, Agenda).

- DAO: Acceso seguro a la base de datos Oracle XE 21c.

- Controllers: Lógica de negocio y validaciones.

- Views: Plantillas HTML/CSS/JS para interacción con el usuario.

- Seguridad: Hash de contraseñas, sesiones y roles para acceso controlado.
## Instalación
1. Clonar el repositorio:

- git clone https://github.com/tu_usuario/medi_plus_proyecto.git
- cd medi_plus_proyecto

2. Crear y activar entorno virtual:
- python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3. Instalar dependencias:
- pip install -r requirements.txt
4. Configurar variables e entornno(.env):
  
FLASK_SECRET_KEY=tu_clave_segura
FLASK_DEBUG=True
SESSION_COOKIE_SAMESITE=Lax
SESSION_COOKIE_SECURE=False
PORT=5000

5. Configurar base de datos Oracle XE 21c y actualizar db/connection.py

## Uso

1. Ejecutar la aplicación:
- python app.py

2.Acceder desde el navegador:
http://localhost:5000/login

3. Iniciar sesion segun rol:
- Administrador: Gestiona usuarios, consultas, recetas e insumos.

- Médico: Acceso a agenda y consultas de sus pacientes.

- Paciente: Consulta su información y recetas.

Diagrama de Clases
- 

Se utilizo PlantUML para representar las entidades y relaciones:

- Usuario (base)

- Paciente, Medico, Administrador (heredan de Usuario)

- Receta, Consulta, Insumo, Agenda (relaciones con usuarios y entre si)

Flujo de la Aplicación
-

1. Registro de usuarios desde JSON.

2. Login seguro con hash de contraseña.

3. Menus dinámicos por tipo de usuario.

4. CRUD de entidades segun permisos.

5. Consulta de informacion médica y generación de reportes.

Seguridad
-

- Hash de contraseñas con algoritmos seguros.

- Prevención de inyección SQL mediante consultas parametrizadas.

- Control de sesiones y roles.

- Datos criticos protegidos y cifrados en la base de datos.

Ejemplos de Uso
-

- Administrador: Gestiona usuarios y registros de consultas.

- Médico: Visualiza agenda y pacientes asignados.

- Paciente: Consulta recetas y citas programadas.

Repositorio
-

https://github.com/HxcCoder/mediplus-backend

Conclusion
-

El prototipo MediPlus digitaliza la gestión medica, asegura la integridad de la informacion y mejora la eficiencia de la clinica. Se aplicaron buenas practicas de desarrollo seguro y control de acceso, cumpliendo con los requerimientos de la asignatura.

Referencias
-

- Documentacion oficial de Flask: https://flask.palletsprojects.com

- Oracle XE 21c: https://www.oracle.com/database/technologies/xe.html

- PlantUML: https://plantuml.com/es/class-diagram

- Normas APA para referencias bibliográficas.
