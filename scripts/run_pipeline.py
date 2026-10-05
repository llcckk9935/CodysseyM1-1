"""Run the complete local pipeline, fail fast, and confirm raw hashes."""
from pathlib import Path
import hashlib
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def raw_hashes():
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (ROOT/'data/raw').glob('*') if p.is_file()}

def main():
    before = raw_hashes()
    if len(before) != 7:
        raise RuntimeError('Expected 7 raw files. See DATA_SOURCES.md to prepare inputs.')
    for name in ['preprocess.py','analyze.py','forecast.py','build_dashboard.py','verify.py']:
        subprocess.run([sys.executable,str(ROOT/'scripts'/name)],cwd=ROOT,check=True)
    if raw_hashes()!=before:
        raise RuntimeError('Raw file hashes changed')
    print('Complete pipeline PASS; original raw SHA256 hashes unchanged.')

if __name__ == '__main__':
    main()
