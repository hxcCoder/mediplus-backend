Resumen de acciones y limpieza (transparencia)

- Se corrigieron y completaron elementos críticos para que la aplicación sea funcional:
  - Autenticación segura con hash (bcrypt) y verificación robusta.
  - Normalización de sesión (`session['user']` + `user_id`, `username`, `tipo`).
  - Filtrado y formateo de montos a CLP con un filtro Jinja (`format_clp`).
  - Añadidos tests unitarios (controllers básicos) y un test de integración que se saltea si no hay credenciales Oracle.

- Limpieza / cambios de transparencia:
  - Se deshabilitó cualquier script que genere PDFs automáticamente (por petición del autor).
  - `reportlab` eliminado de `requirements.txt` para evitar dependencias innecesarias.
  - Se añadió `assets/informe_entrega.txt` con el enunciado de la evaluación (para referencia del profesor).

- Pendientes relevantes (por hacer o revisar):
  - Completar pruebas e integración contra Oracle XE (crear DB de pruebas y scripts de migración).
  - Revisar y pulir todas las plantillas UI y completar cualquier CRUD aún incompleto.
  - Añadir CI (GitHub Actions) para ejecutar pruebas automáticas.

Si quiere, puedo continuar y completar los CRUD restantes y la integración con la base de datos (necesitaré las credenciales de Oracle o indicaciones para usar una DB local). Si prefiere que pause, me indica "pausa".
