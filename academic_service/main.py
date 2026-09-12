import os
from typing import Literal

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from .agent import run_academic

app = FastAPI(
    title="OpenManus Academic API",
    version="0.2.0",
    description="API acadêmica independente para GPT Actions. Não pertence ao SaaS jurídico.",
    servers=[{"url": os.getenv("PUBLIC_BASE_URL", "http://localhost:8000")}],
)

Mode = Literal["tcc", "case", "paper", "abnt", "references", "compare", "research"]


class AcademicRequest(BaseModel):
    mode: Mode = Field(description="Tipo de tarefa acadêmica")
    task: str = Field(min_length=3, description="Instrução específica")
    context: str | None = Field(default=None, description="Texto, referências ou documentos convertidos em texto")


class AcademicResponse(BaseModel):
    mode: Mode
    result: str


def require_api_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> None:
    expected = os.getenv("ACADEMIC_API_KEY")
    if not expected:
        raise HTTPException(status_code=503, detail="ACADEMIC_API_KEY não configurada")
    if x_api_key != expected:
        raise HTTPException(status_code=401, detail="Chave de API inválida")


@app.get("/health", operation_id="academicHealth")
async def health():
    return {
        "status": "ok",
        "service": "openmanus-academic",
        "openmanus_key_configured": bool(os.getenv("OPENMANUS_API_KEY")),
        "academic_api_key_configured": bool(os.getenv("ACADEMIC_API_KEY")),
    }


@app.get("/modes", operation_id="listAcademicModes", dependencies=[Depends(require_api_key)])
async def modes():
    return {"modes": ["tcc", "case", "paper", "abnt", "references", "compare", "research"]}


@app.post(
    "/v1/academic/run",
    response_model=AcademicResponse,
    operation_id="runAcademicTask",
    dependencies=[Depends(require_api_key)],
)
async def run(req: AcademicRequest):
    try:
        result = await run_academic(req.mode, req.task, req.context)
        return AcademicResponse(mode=req.mode, result=result)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/privacy", response_class=HTMLResponse, include_in_schema=False)
async def privacy():
    return """<html><body><h1>OpenManus Academic - Política de Privacidade</h1><p>O serviço processa apenas o conteúdo enviado pela Action para executar a tarefa solicitada. A implantação deve usar logs mínimos e não armazenar trabalhos acadêmicos além do necessário para o processamento.</p><p>Este serviço é independente do SaaS jurídico e não acessa dados de escritório.</p></body></html>"""
