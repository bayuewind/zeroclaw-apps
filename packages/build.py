#!/usr/bin/env python3
"""Build deterministic package archives from tracked skill sources, never credentials."""
from pathlib import Path
import hashlib
import zipfile
root = Path(__file__).resolve().parent
output = root / 'nutstore-1.0.0.zip'
with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
    for path in sorted((root / 'nutstore').rglob('*')):
        if not path.is_file() or path.suffix not in ('.md', '.py') or '__pycache__' in path.parts:
            continue
        info = zipfile.ZipInfo(path.relative_to(root / 'nutstore').as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
        info.external_attr = 0o100644 << 16
        info.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(info, path.read_bytes())
print(output.name, hashlib.sha256(output.read_bytes()).hexdigest())
