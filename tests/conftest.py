"""
Configuración y fixtures compartidos para todos los tests.
"""

import pytest
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Agregar directorio raíz al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Cargar variables de entorno desde la raíz del proyecto
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path, override=True)

# Debug: imprimir si el .env existe y se cargó
if env_path.exists():
    print(f"\n✅ Archivo .env encontrado en: {env_path}")
else:
    print(f"\n⚠️  Archivo .env NO encontrado en: {env_path}")

# Verificar que las variables de entorno necesarias estén configuradas
@pytest.fixture(scope="session", autouse=True)
def check_env_vars():
    """Verifica que las variables de entorno necesarias estén configuradas."""
    required_vars = [
        "OPENROUTER_API_KEY",
        "SUPABASE_URL",
        "SUPABASE_ANON_KEY"  # Usar ANON_KEY en lugar de SERVICE_KEY (más seguro)
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        pytest.skip(
            f"Variables de entorno faltantes: {', '.join(missing_vars)}. "
            "Configure estas variables en .env para ejecutar los tests."
        )


@pytest.fixture(scope="session")
def openrouter_api_key():
    """Retorna la API key de OpenRouter."""
    return os.getenv("OPENROUTER_API_KEY")


@pytest.fixture(scope="session")
def supabase_config():
    """Retorna la configuración de Supabase."""
    return {
        "url": os.getenv("SUPABASE_URL"),
        # Usar ANON_KEY (más seguro con RLS habilitado)
        "key": os.getenv("SUPABASE_ANON_KEY") or os.getenv("SUPABASE_SERVICE_KEY")
    }


@pytest.fixture
def sample_wollok_query():
    """Query de ejemplo para Wollok."""
    return "¿Qué es un objeto en Wollok?"


@pytest.fixture
def sample_haskell_query():
    """Query de ejemplo para Haskell."""
    return "¿Qué son las funciones de orden superior?"


@pytest.fixture
def sample_prolog_query():
    """Query de ejemplo para Prolog."""
    return "¿Qué es la unificación en Prolog?"


@pytest.fixture
def agent_configs():
    """Retorna las configuraciones de todos los agentes."""
    from config.agents import AGENTS
    return AGENTS

