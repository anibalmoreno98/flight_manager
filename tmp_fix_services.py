from pathlib import Path
import re

service_files = [
    'app/services/usuario_service.py',
    'app/services/piloto_service.py',
    'app/services/mision_service.py',
    'app/services/vuelo_service.py',
    'app/services/telemetria_service.py',
]

for path_str in service_files:
    path = Path(path_str)
    text = path.read_text(encoding='utf-8')

    # detect model name from app.models import
    m = re.search(r'from app\.models\.(\w+) import (\w+)', text)
    if not m:
        print('skip', path_str, 'no model import')
        continue

    mod_name, model_name = m.group(1), m.group(2)
    repo_name = model_name + 'Repository'

    # replace repository import with class import
    text = re.sub(r'from app\.repositories(?:\.[^ ]+)? import [^\n]+',
                  f'from app.repositories.{mod_name} import {repo_name}', text)

    # ensure class __init__ has self.repo
    text = re.sub(r'def __init__\(self, session: Session\):\n\s*self\.session = session',
                  f'def __init__(self, session: Session):\n        self.session = session\n        self.repo = {repo_name}(session)',
                  text)

    # replace old repo calls
    text = re.sub(rf'\b{mod_name}_repo\.(add|get|list_all|update|delete)\(', r'self.repo.\1(', text)
    text = re.sub(r'\b\w+_repo\.(add|get|list_all|update|delete)\(', r'self.repo.\1(', text)

    text = re.sub(r'self\.repo\.list_all\(self\.session\)', 'self.repo.list_all()', text)

    # append router wrappers only if not already declared
    if 'def create_' + mod_name + '_service(' in text and 'def delete_' + mod_name + '_service(' in text:
        if not re.search(r'def create_' + mod_name + '_service\(.*session: Session', text):
            wrapper = f"\n\n# API de funciones para routers\n\n"
            wrapper += f"def create_{mod_name}_service({mod_name}: {model_name}, session: Session) -> {model_name}:\n"
            wrapper += f"    return {model_name}Service(session).create_{mod_name}_service({mod_name})\n\n"
            wrapper += f"def get_{mod_name}_service({mod_name}_id: int, session: Session) -> {model_name}:\n"
            wrapper += f"    return {model_name}Service(session).get_{mod_name}_service({mod_name}_id)\n\n"
            wrapper += f"def list_{mod_name}s_service(session: Session) -> list[{model_name}]:\n"
            wrapper += f"    return {model_name}Service(session).list_{mod_name}s_service()\n\n"
            wrapper += f"def update_{mod_name}_service({mod_name}_id: int, {mod_name}_data: {model_name}, session: Session) -> {model_name}:\n"
            wrapper += f"    return {model_name}Service(session).update_{mod_name}_service({mod_name}_id, {mod_name}_data)\n\n"
            wrapper += f"def delete_{mod_name}_service({mod_name}_id: int, session: Session) -> dict[str, bool]:\n"
            wrapper += f"    return {model_name}Service(session).delete_{mod_name}_service({mod_name}_id)\n"
            text = text.strip() + '\n' + wrapper

    path.write_text(text, encoding='utf-8')
    print('updated', path_str)
