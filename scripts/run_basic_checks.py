"""Ejecuta algunas comprobaciones básicas de forma local sin pytest.
Útil cuando `pytest` no está instalado en el entorno del usuario.
"""
import importlib.machinery, importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

def run_test(path: str, func_name: str = None):
    p = ROOT / path
    loader = importlib.machinery.SourceFileLoader(p.stem, str(p))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    if func_name:
        getattr(mod, func_name)()

if __name__ == '__main__':
    print('Running basic checks...')
    run_test('tests/test_app.py', 'test_app_creation')
    run_test('tests/test_security.py', 'test_hash_and_check')
    run_test('tests/test_usuario_controller.py', 'test_usuario_crud')
    run_test('tests/test_paciente_controller.py', 'test_paciente_crud')
    run_test('tests/test_medico_controller.py', 'test_medico_crud')
    run_test('tests/test_administrador_controller.py', 'test_admin_crud')
    print('Basic checks passed')
