from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from multi_agent_analyst.graph.workflow import run_workflow
from pathlib import Path


app = FastAPI(
    title="Multi-Agent Enterprise Analyst",
    description="A LangGraph-powered multi-agent system for financial and marketing analysis.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Multi-Agent Enterprise Analyst API",
        "docs": "/docs",
    }


@app.post("/analyze")
async def analyze(
    financial_doc: UploadFile = File(...),
    marketing_doc: UploadFile = File(...),
):
    if not financial_doc.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="financial_doc must be a PDF")

    if not marketing_doc.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="marketing_doc must be a PDF")

    financial_bytes = await financial_doc.read()
    marketing_bytes = await marketing_doc.read()

    result = await run_workflow(financial_bytes, marketing_bytes)

    pdf_path = result.get("pdf_path")

    if not pdf_path or not Path(pdf_path).exists():
        return {
            "status": "failed",
            "result": result,
        }

    return FileResponse(
        path=pdf_path,
        filename="enterprise_analysis_report.pdf",
        media_type="application/pdf",
    )
