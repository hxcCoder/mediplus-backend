from pathlib import Path
import sys
p = Path(__file__).resolve().parent.parent / 'tests'
errors = []
for f in p.glob('*.py'):
    try:
        compile(f.read_text(encoding='utf-8'), str(f), 'exec')
    except Exception as e:
        errors.append((f, str(e)))
if errors:
    print('SYNTAX_ERRORS')
    for f,e in errors:
        print(f, e)
    sys.exit(1)
print('ALL_OK')
