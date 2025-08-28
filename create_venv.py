import subprocess
import sys
from pathlib import Path


def main() -> None:
    venv_dir = Path('.venv')
    if not venv_dir.exists():
        subprocess.run([sys.executable, '-m', 'venv', str(venv_dir)], check=True)
    pip = venv_dir / ('Scripts' if sys.platform == 'win32' else 'bin') / 'pip'
    subprocess.run([str(pip), 'install', '--upgrade', 'pip'], check=True)
    req = Path('requirements.txt')
    if req.exists():
        subprocess.run([str(pip), 'install', '-r', str(req)], check=True)
    print(f'Virtual environment created at {venv_dir}')


if __name__ == '__main__':
    main()
