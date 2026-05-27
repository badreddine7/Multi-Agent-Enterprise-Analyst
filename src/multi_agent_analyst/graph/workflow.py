from typing import TypedDict, Optional, Literal
from langgraph.graph import StateGraph, END
import asyncio

from multi_agent_analyst.agents.financial_agent import run_financial_agent
from multi_agent_analyst.agents.marketing_agent import run_marketing_agent
from multi_agent_analyst.agents.synthesis_agent import run_synthesis_agent
from multi_agent_analyst.utils.document_loader import extract_text_from_pdf_bytes
from multi_agent_analyst.utils.pdf_report import generate_pdf_report


MAX_TURNS = 5


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


async def supervisor_node(state: AgentState):
    turn = state.get("turn", 0)

    if turn >= MAX_TURNS:
        return {
            "next": "end",
            "errors": state.get("errors", []) + ["Workflow stopped by loop guard."]
        }

    financial_done = state.get("financial_result") is not None
    marketing_done = state.get("marketing_result") is not None
    final_done = state.get("final_report") is not None

    if not financial_done or not marketing_done:
        return {
            "next": "analyze",
            "turn": turn + 1,
        }

    if not final_done:
        return {
            "next": "synthesize",
            "turn": turn + 1,
        }

    return {"next": "end"}


async def parallel_analysis_node(state: AgentState):
    financial_text = state["financial_text"]
    marketing_text = state["marketing_text"]

    financial_task = run_financial_agent(financial_text)
    marketing_task = run_marketing_agent(marketing_text)

    financial_result, marketing_result = await asyncio.gather(
        financial_task,
        marketing_task,
    )

    return {
        "financial_result": financial_result.model_dump(),
        "marketing_result": marketing_result.model_dump(),
    }


async def synthesis_node(state: AgentState):
    final_report = await run_synthesis_agent(
        financial_data=state["financial_result"],
        marketing_data=state["marketing_result"],
    )

    pdf_path = generate_pdf_report(final_report)

    report_dict = final_report.model_dump()
    report_dict["pdf_path"] = pdf_path

    return {
        "final_report": report_dict,
        "pdf_path": pdf_path,
    }


workflow = StateGraph(AgentState)

workflow.add_node("supervisor", supervisor_node)
workflow.add_node("analyze", parallel_analysis_node)
workflow.add_node("synthesize", synthesis_node)

workflow.set_entry_point("supervisor")

workflow.add_conditional_edges(
    "supervisor",
    lambda state: state["next"],
    {
        "analyze": "analyze",
        "synthesize": "synthesize",
        "end": END,
    },
)

workflow.add_edge("analyze", "supervisor")
workflow.add_edge("synthesize", "supervisor")

graph = workflow.compile()


async def run_workflow(financial_pdf_bytes: bytes, marketing_pdf_bytes: bytes) -> dict:
    financial_text = extract_text_from_pdf_bytes(financial_pdf_bytes)
    marketing_text = extract_text_from_pdf_bytes(marketing_pdf_bytes)

    initial_state: AgentState = {
        "financial_text": financial_text,
        "marketing_text": marketing_text,
        "financial_result": None,
        "marketing_result": None,
        "final_report": None,
        "pdf_path": None,
        "turn": 0,
        "next": "analyze",
        "errors": [],
    }

    result = await graph.ainvoke(
        initial_state,
        config={"recursion_limit": 10},
    )

    return result
