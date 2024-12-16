from cx_Freeze import setup, Executable
import sys
import os

include_files = [
    "src\sistema_recomendacao.db",              # Banco de dados
    "src\img\logo.ico",            # Ícone
    "src\inferencia.py"          # Arquivo Python secundário
]

def resource_path(relative_path):
    """Obter o caminho correto dos arquivos no executável"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


executables = [
    Executable(
        "AgroExpert.py",         # Arquivo Python principal
        base="Win32GUI",     # Impede a abertura do terminal no Windows (GUI app)
        icon="src\img\logo.ico"    # Define o ícone para o executável
    )
]

setup(
    name="AgroExpert",
    version="1.0",
    description="AgroExpert",
    options={
        "build_exe": {
            "include_files": include_files  # Inclui os arquivos no pacote
        }
    },
    executables=executables
)
