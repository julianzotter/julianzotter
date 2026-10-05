"""
NEXUS Orchestrator — FastAPI entry point.
Wires Signal Matrix → MoE Router → Research Engine → COT Workflow.
"""
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import json

from signal_matrix import compute as sig_compute, detect_scope
from moe_router import route as moe_route, sparsity
from kernel_router import route_kernel, coverage_report as kernel_coverage
from research_engine import get_sources, scrape_seed_context
from cot_workflow import run as cot_run

app = FastAPI(title="NEXUS AI-OS", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND = Path(__file__).parent.parent / "frontend"
app.mount("/ui", StaticFiles(directory=str(FRONTEND), html=True), name="ui")


@app.get("/api/health")
def health():
    return {"status": "online", "version": "1.1.0", "kernel_coverage": kernel_coverage()}


@app.get("/api/kernels")
def kernels(status: str | None = None):
    from kernel_router import list_kernels
    return {"kernels": list_kernels(status_filter=status), "coverage": kernel_coverage()}


@app.get("/api/route")
def route_aec(norm_tag: str, nachweis_typ: str):
    return route_kernel(norm_tag, nachweis_typ)


@app.post("/api/analyze")
async def analyze(payload: dict):
    task = payload.get("task", "")
    scope = detect_scope(task)
    sig = sig_compute(scope)
    experts = moe_route(scope)
    sources = get_sources(scope)
    # Layer 3: attempt kernel routing from task text
    norm_hint = next((w.upper() for w in task.split() if w.upper() in ("EC2","EC3","EC5","CENTS19103","SIGEPLAN","SEILSTATIK")), None)
    nachweis_hint = next((w.upper() for w in task.split() if w.upper() in ("BIEGE","SCHUB","KNICKEN","DURCHSTANZEN","ZUGKRAFT","VERBUND-GAMMA2","SICHERHEITSPLAN")), None)
    kernel = route_kernel(norm_hint, nachweis_hint) if norm_hint and nachweis_hint else None
    return {
        "scope": scope,
        "signal": {"score": sig.score, "risk": sig.risk,
                   "R": sig.R, "E": sig.E, "C": sig.C, "A": sig.A, "U": sig.U},
        "experts": experts,
        "sparsity": sparsity(scope),
        "sources": sources,
        "kernel": kernel,
    }


@app.websocket("/ws/run")
async def run_workflow(ws: WebSocket):
    await ws.accept()
    try:
        data = await ws.receive_json()
        task = data.get("task", "")
        scope = detect_scope(task)
        seed = (await scrape_seed_context(scope))["context"]

        def on_step(step):
            import asyncio
            asyncio.create_task(
                ws.send_json({"step": step.step, "status": step.status, "output": step.output})
            )

        result = await cot_run(task, scope, seed, on_step=None)
        for step in result.steps:
            await ws.send_json({"step": step.step, "status": step.status, "output": step.output})

        await ws.send_json({"done": True, "scope": scope})
    except Exception as e:
        await ws.send_json({"error": str(e)})
    finally:
        await ws.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("nexus_orchestrator:app", host="0.0.0.0", port=8000, reload=True)
