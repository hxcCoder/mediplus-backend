# MediPlus

Proyecto prototipo para la clínica MediPlus (Trabajo POO Seguro).

Requisitos mínimos:
- Python 3.10+
- Oracle XE 21c (ODBC/Net listener configurado)

Instalación (entorno virtual):

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # Windows: copy .env.example .env
# Editar .env con credenciales de BD
```

Cargar usuarios iniciales desde JSON:

```bash
python -m scripts.init_users
```

Endpoints principales (ejemplos):
- `GET /login` (formulario)
- `POST /login` (login form)
- `GET /register` (formulario registro)
- `POST /register` (registro)
- `GET /insumos/` (listar insumos)
- `POST /insumos/` (crear insumo)
- `PUT /insumos/<id>` (actualizar insumo)
- `DELETE /insumos/<id>` (eliminar insumo)
- `GET /recetas` (listar recetas)
- `GET /receta/nueva` (formulario)
- `POST /receta/nueva` (crear receta)
- `POST /receta/eliminar/<id>` (eliminar receta)

(Completar más endpoints conforme se implementen los controllers.)

Ejecutar la aplicación (desarrollo):

```bash
set FLASK_DEBUG=true
python app.py
```

Tests:

Instalar dependencias y ejecutar tests con `pytest`, o ejecutar comprobaciones rápidas sin `pytest`:

```bash
pip install -r requirements.txt
python -m pytest -q    # si tienes pytest instalado
# o, para comprobar localmente sin pytest:
python scripts/run_basic_checks.py
```

Entrega y transparencia:

- El enunciado de la evaluación se añadió como `assets/informe_entrega.txt` para referencia.
- La generación automática de PDFs desde el repositorio fue deshabilitada por petición del autor (evita dependencias innecesarias).
- Para crear un PDF localmente copie `assets/informe_entrega.txt` y use su herramienta preferida.

