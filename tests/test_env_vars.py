import os
import pytest

def test_env_vars_present():
    required_vars = ["URL", "APPKEY", "APPTOKEN", "BOTTOKEN", "CHATID"]
    missing = [var for var in required_vars if not os.getenv(var)]
    assert not missing, f"Variáveis ausentes no .env: {', '.join(missing)}"