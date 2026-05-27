from langchain_core.prompts import ChatPromptTemplate
from multi_agent_analyst.schemas.models import FinancialMetrics
from multi_agent_analyst.llms import get_gemini_llm





llm = get_gemini_llm(max_output_tokens=1200)
structured_llm = llm.with_structured_output(FinancialMetrics)


async def run_financial_agent(doc_text: str) -> FinancialMetrics:
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are a financial analyst agent.

            Extract financial metrics from the provided company financial report.
            Return only data matching the required structured schema.

            Rules:
            - Use numeric values where possible.
            - If a field is unavailable, leave it as null or empty.
            - Include key financial risks mentioned in the document.
            """
        ),
        ("user", "{doc}")
    ])

    chain = prompt | structured_llm
    return await chain.ainvoke({"doc": doc_text})
