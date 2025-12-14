import importlib.machinery, importlib.util, sys, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

p = ROOT / 'tests' / 'test_app.py'
loader = importlib.machinery.SourceFileLoader('test_app', str(p))
spec = importlib.util.spec_from_loader(loader.name, loader)
mod = importlib.util.module_from_spec(spec)
loader.exec_module(mod)
print('Imported test_app')
mod.test_app_creation()
print('test_app_creation OK')
