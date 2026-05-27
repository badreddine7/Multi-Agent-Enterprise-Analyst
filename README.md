# Multi-Agent Enterprise Analyst

A production-style **Multi-Agent AI system** that analyzes enterprise business documents using **LangGraph**, **LangChain**, **FastAPI**, **Gemini**, and **Pydantic Structured Outputs**.

Users upload:

1. A company financial report PDF.
2. A competitor marketing report PDF.

The system runs multiple specialized agents to extract insights, synthesize findings, and generate a final board-ready PDF report.

---

## Overview

Most beginner AI projects use simple RAG over one document.

This project demonstrates a more advanced architecture:

```text
PDF Uploads
    ↓
PDF Text Extraction
    ↓
LangGraph Supervisor
    ↓
Parallel Specialist Agents
    ↓
Structured Pydantic Outputs
    ↓
Strategy Synthesis Agent
    ↓
Generated PDF Report
```

The final output is a downloadable enterprise analysis report containing:

- Financial metrics
- Marketing insights
- Competitor strengths and weaknesses
- Executive summary
- Strategic recommendations
- Strategic risks

---

## Tech Stack

- Python 3.11
- FastAPI
- LangGraph
- LangChain
- Gemini Free Tier
- Pydantic v2
- AsyncIO
- pypdf
- ReportLab
- Poetry
- Docker

---

## Key Features

### Multi-Agent System

The workflow contains several specialized agents:

| Agent | Purpose |
|---|---|
| Financial Analyst Agent | Extracts revenue, margins, growth, income, and financial risks |
| Marketing Intelligence Agent | Extracts competitor channels, positioning, strengths, and weaknesses |
| Strategy Synthesis Agent | Creates final strategic report |
| Supervisor Agent | Routes the workflow and prevents infinite loops |

---

### LangGraph Workflow

The system uses **LangGraph** to manage stateful multi-agent orchestration.

Workflow:

```text
Supervisor
    ↓
Analyze financial and marketing documents in parallel
    ↓
Supervisor
    ↓
Synthesize final report
    ↓
Supervisor
    ↓
END
```

The supervisor decides what happens next based on graph state.

---

### Structured Outputs

Agents return validated Pydantic models instead of raw unstructured LLM text.

Example schema:

```python
class FinancialMetrics(BaseModel):
    revenue: Optional[float]
    gross_margin_pct: Optional[float]
    yoy_growth_pct: Optional[float]
    operating_income: Optional[float]
    net_income: Optional[float]
    key_risks: List[str]
```

This makes the application more reliable and easier to debug.

---

### Async Parallel Execution

The financial and marketing agents run concurrently:

```python
financial_result, marketing_result = await asyncio.gather(
    run_financial_agent(financial_text),
    run_marketing_agent(marketing_text),
)
```

This improves performance because both LLM calls happen at the same time.

---

### PDF Report Generation

The final structured report is converted into a professional PDF using `ReportLab`.

The API returns:

```text
enterprise_analysis_report.pdf
```

---

## Project Structure

```text
multi-agent-analyst/
├── README.md
├── pyproject.toml
├── Dockerfile
├── generated_reports/
├── src/
│   └── multi_agent_analyst/
│       ├── __init__.py
│       ├── api/
│       │   ├── __init__.py
│       │   └── main.py
│       ├── agents/
│       │   ├── __init__.py
│       │   ├── financial_agent.py
│       │   ├── marketing_agent.py
│       │   └── synthesis_agent.py
│       ├── graph/
│       │   ├── __init__.py
│       │   └── workflow.py
│       ├── schemas/
│       │   ├── __init__.py
│       │   └── models.py
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── document_loader.py
│       │   └── pdf_report.py
│       └── llms.py
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/multi-agent-analyst.git
cd multi-agent-analyst
```

### 2. Install Poetry

If Poetry is not installed:

```bash
pip install poetry
```

### 3. Install dependencies

```bash
poetry install
```

### 4. Install Gemini LangChain provider

If not already installed:

```bash
poetry add langchain-google-genai
```

---

## Environment Variables

This project uses Gemini through Google AI Studio.

Get a free API key from:

```text
https://aistudio.google.com/app/apikey
```

Set your API key.

### macOS/Linux

```bash
export GOOGLE_API_KEY="your_google_api_key_here"
```

### Windows PowerShell

```powershell
$env:GOOGLE_API_KEY="your_google_api_key_here"
```

You can also create a `.env.example` file:

```bash
GOOGLE_API_KEY=your_google_api_key_here
```

---

## Running the App

Start the FastAPI server:

```bash
poetry run uvicorn multi_agent_analyst.api.main:app --reload
```

Open the API docs:

```text
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Health Check

```http
GET /
```

Example response:

```json
{
  "message": "Multi-Agent Enterprise Analyst API",
  "docs": "/docs"
}
```

---

### Analyze Documents

```http
POST /analyze
```

Upload two PDF files:

| Field | Description |
|---|---|
| `financial_doc` | Company financial report PDF |
| `marketing_doc` | Competitor marketing report PDF |

Response:

```text
Downloadable PDF report
```

---

### Optional JSON Debug Endpoint

If implemented:

```http
POST /analyze-json
```

This returns the full LangGraph state as JSON.

Example response:

```json
{
  "financial_result": {
    "revenue": 248600000,
    "gross_margin_pct": 70.0,
    "yoy_growth_pct": 20.0,
    "operating_income": 31500000,
    "net_income": 24800000,
    "key_risks": [
      "Customer concentration risk",
      "Margin pressure from infrastructure costs",
      "Competitive pricing pressure"
    ]
  },
  "marketing_result": {
    "top_channels": [
      "LinkedIn advertising",
      "Technical webinars",
      "SEO-driven blog content"
    ],
    "positioning_summary": "The competitor positions itself as an AI-first CloudOps platform.",
    "competitor_strengths": [
      "Strong AI-first positioning",
      "Effective technical SEO",
      "Strong DevOps credibility"
    ],
    "competitor_weaknesses": [
      "Messaging may be too technical for executives",
      "Pricing may be expensive for smaller customers"
    ]
  },
  "final_report": {
    "executive_summary": "The company is financially healthy but faces competitive pressure.",
    "recommendations": [
      "Emphasize enterprise trust and compliance",
      "Create CFO and CIO-focused content",
      "Develop industry-specific case studies"
    ],
    "strategic_risks": [
      "Competitor may gain share through AI-first positioning",
      "Large cloud vendors may bundle similar features"
    ]
  },
  "pdf_path": "generated_reports/enterprise_analysis_xxxxx.pdf"
}
```

---

## Expected PDF Output

The generated PDF contains:

```text
Multi-Agent Enterprise Analyst Report

1. Executive Summary

2. Financial Analysis
   - Revenue
   - Gross margin
   - YoY growth
   - Operating income
   - Net income
   - Financial risks

3. Marketing Analysis
   - Positioning summary
   - Top channels
   - Target audience
   - Competitor strengths
   - Competitor weaknesses
   - Notable campaigns

4. Strategic Recommendations

5. Strategic Risks
```

---

## How the LangGraph Workflow Works

The graph uses a shared state object:

```python
class AgentState(TypedDict, total=False):
    financial_text: str
    marketing_text: str
    financial_result: Optional[dict]
    marketing_result: Optional[dict]
    final_report: Optional[dict]
    pdf_path: Optional[str]
    turn: int
    next: Literal["analyze", "synthesize", "end"]
    errors: list[str]
```

The supervisor checks the state and routes execution:

```text
If financial_result or marketing_result is missing:
    go to analyze

If both analyses exist but final_report is missing:
    go to synthesize

If final_report exists:
    end workflow
```

---

## Infinite Loop Prevention

The system prevents runaway agent loops using three safeguards.

### 1. Explicit State Checks

The supervisor checks whether each step is complete:

```python
financial_done = state.get("financial_result") is not None
marketing_done = state.get("marketing_result") is not None
final_done = state.get("final_report") is not None
```

### 2. Turn Counter

The workflow has a maximum number of allowed turns:

```python
MAX_TURNS = 5
```

If the graph exceeds this limit, it exits safely.

### 3. LangGraph Recursion Limit

The graph is invoked with:

```python
config={"recursion_limit": 10}
```

This provides another runtime safety layer.

---

## Token Limit Strategy

Large PDFs may exceed LLM context limits.

The recommended strategy is:

```text
1. Extract text from the PDF.
2. Split the text into chunks.
3. Analyze each chunk independently.
4. Reduce partial outputs into one structured summary.
5. Pass only compact Pydantic objects between agents.
```

This prevents agents from passing large raw documents back and forth.

Example chunking utility:

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(text: str, chunk_size: int = 12000, chunk_overlap: int = 500) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_text(text)
```

---

## Docker

### Build the image

```bash
docker build -t multi-agent-analyst .
```

### Run the container

```bash
docker run -p 8000:8000 \
  -e GOOGLE_API_KEY="your_google_api_key_here" \
  multi-agent-analyst
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

## Example Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root

COPY src ./src

RUN poetry install

EXPOSE 8000

CMD ["uvicorn", "multi_agent_analyst.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Example Use Case

A user uploads:

```text
sample_financial_report.pdf
sample_competitor_marketing_report.pdf
```

The financial report includes:

```text
Revenue: $248.6 million
Gross Margin: 70.0%
YoY Growth: 20.0%
Operating Income: $31.5 million
Net Income: $24.8 million
```

The competitor marketing report includes:

```text
Competitor: NovaStack Technologies
Positioning: AI-first CloudOps platform
Top Channels: LinkedIn ads, webinars, SEO, partner marketing
```

The generated report includes:

```text
Executive Summary:
Acme Cloud Systems delivered strong fiscal year performance with 20% revenue growth
and a healthy 70% gross margin. However, the company faces competitive pressure
from NovaStack's AI-first positioning and technical marketing strategy.

Recommendations:
- Emphasize enterprise trust and compliance.
- Build CFO/CIO-focused campaigns.
- Create industry-specific case studies.
- Improve technical SEO around cloud observability.
```

---

## Interview Talking Points

### How did you prevent agents from getting stuck in infinite loops?

The workflow uses explicit state flags, a turn counter, and LangGraph's recursion limit.

```text
The supervisor checks whether each required result exists before routing.
If the workflow exceeds MAX_TURNS, it exits safely.
LangGraph's recursion_limit provides an additional runtime safeguard.
```

---

### How did you handle token limit overflows?

```text
The system is designed to avoid repeatedly passing raw documents between agents.
Large PDFs can be chunked, analyzed independently, and reduced into compact
Pydantic summaries. Only structured outputs are passed between agents.
```

---

### Why use Pydantic structured outputs?

```text
Pydantic schemas make LLM outputs predictable and validated.
Instead of parsing free-form text, each agent returns data that matches a known schema.
This improves reliability, debugging, and downstream PDF generation.
```

---

### Why use LangGraph instead of only LangChain?

```text
LangChain is useful for LLM calls and prompt composition.
LangGraph is better for stateful multi-agent workflows because it supports
nodes, edges, conditional routing, shared state, and loop guards.
```

---

## Future Improvements

- Add chunking and reducer agents for large PDFs.
- Add LangSmith tracing and observability.
- Store generated reports in cloud storage.
- Add authentication.
- Add background task processing with Celery or Redis Queue.
- Add frontend dashboard.
- Add support for DOCX, CSV, and HTML competitor data.
- Add automated tests for each node and agent.
- Add evaluation datasets for extraction accuracy.

---

## Resume Bullets

```text
Built a Multi-Agent Enterprise Analyst using LangGraph, LangChain, FastAPI, and Gemini to analyze financial and competitor marketing PDFs.

Implemented asynchronous specialist agents for financial extraction, marketing intelligence, and strategic synthesis using Pydantic structured outputs.

Designed a supervisor-controlled LangGraph workflow with explicit state transitions, loop guards, and recursion limits to prevent runaway agent execution.

Added PDF ingestion, structured JSON validation, and automated board-ready PDF report generation using pypdf and ReportLab.

Containerized the application with Docker and managed dependencies with Poetry.
```

---

## Author

Built by `badreddine7`.

---

## License

MIT License
