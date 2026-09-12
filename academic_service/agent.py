import asyncio
import os
import sys
from pathlib import Path

from .prompts import build_prompt

ROOT = Path(__file__).resolve().parent.parent
OPENMANUS_DIR = Path(os.getenv("OPENMANUS_DIR", str(ROOT / ".runtime-openmanus")))


def _ensure_import_path() -> None:
    if OPENMANUS_DIR.exists() and str(OPENMANUS_DIR) not in sys.path:
        sys.path.insert(0, str(OPENMANUS_DIR))


def _ensure_config() -> None:
    config_dir = OPENMANUS_DIR / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    config = config_dir / "config.toml"

    model = os.getenv("OPENMANUS_MODEL", "gpt-4o-mini")
    base_url = os.getenv("OPENMANUS_BASE_URL", "https://api.openai.com/v1")
    api_key = os.getenv("OPENMANUS_API_KEY", "")
    max_tokens = int(os.getenv("OPENMANUS_MAX_TOKENS", "8192"))
    temperature = float(os.getenv("OPENMANUS_TEMPERATURE", "0.0"))
    use_sandbox = os.getenv("OPENMANUS_USE_SANDBOX", "false").lower() == "true"

    config.write_text(
        f'''[llm]\nmodel = "{model}"\nbase_url = "{base_url}"\napi_key = "{api_key}"\nmax_tokens = {max_tokens}\ntemperature = {temperature}\n\n[sandbox]\nuse_sandbox = {str(use_sandbox).lower()}\n\n[runflow]\nuse_data_analysis_agent = true\n''',
        encoding="utf-8",
    )


async def run_academic(mode: str, task: str, context: str | None = None) -> str:
    if not os.getenv("OPENMANUS_API_KEY"):
        raise RuntimeError("OPENMANUS_API_KEY não configurada")
    if not OPENMANUS_DIR.exists():
        raise RuntimeError("OpenManus runtime não encontrado")

    _ensure_import_path()
    _ensure_config()

    from app.agent.manus import Manus  # type: ignore

    prompt = build_prompt(mode, task, context)
    agent = await Manus.create()
    try:
        return await agent.run(prompt)
    finally:
        await agent.cleanup()


def run_academic_sync(mode: str, task: str, context: str | None = None) -> str:
    return asyncio.run(run_academic(mode, task, context))
