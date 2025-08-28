import os
import pathlib
import subprocess
import sys

def _venv_python(venv_dir: pathlib.Path) -> pathlib.Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python"
    return venv_dir / "bin" / "python"

def main() -> None:
    root = pathlib.Path(os.environ.get("BUILD_WORKING_DIRECTORY", ".")).resolve()
    venv_dir = root / ".venv"
    if not venv_dir.exists():
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
    reqs = pathlib.Path(__file__).with_name("requirements.txt")
    subprocess.run([str(_venv_python(venv_dir)), "-m", "pip", "install", "-r", str(reqs)], check=True)


if __name__ == "__main__":
    main()
