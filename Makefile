#  ENTORNO VIRTUAL
# Nombre de la carpeta del entorno virtual
VENV = venv

# Detectar Windows vs Linux/Mac para usar las rutas correctas
ifeq ($(OS),Windows_NT)
    PYTHON = $(VENV)/Scripts/python.exe
    PIP = $(VENV)/Scripts/pip.exe
else
    PYTHON = $(VENV)/bin/python
    PIP = $(VENV)/bin/pip
endif

# Crear el entorno virtual
# Este comando ejecuta: python -m venv venv
venv:
    python -m venv $(VENV)

# Cómo ACTIVAR el entorno virtual
activate:
    @echo "Para activar el entorno virtual:"
    @echo "Windows:   venv\\Scripts\\Activate"
    @echo "Linux/Mac: source venv/bin/activate"

# Instalar dependencias dentro del entorno virtual
install: venv
    $(PIP) install -r requirements.txt

# Instalar dependencias de desarrollo (pytest, black, etc.)
install-dev: venv
    $(PIP) install -r requirements.txt
    $(PIP) install pytest pytest-cov httpx black isort

# Salir del entorno virtual
deactivate:
    @echo "Para salir del entorno virtual, simplemente ejecuta: deactivate"

