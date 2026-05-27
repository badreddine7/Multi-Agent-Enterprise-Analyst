from multi_agent_analyst.llms import get_gemini_llm
from langchain_core.prompts import ChatPromptTemplate
from multi_agent_analyst.schemas.models import FinalReport


llm = get_gemini_llm(max_output_tokens=1200)
structured_llm = llm.with_structured_output(FinalReport)


async def run_synthesis_agent(financial_data: dict, marketing_data: dict) -> FinalReport:
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are a senior enterprise strategy consultant.

            Synthesize the financial analysis and marketing analysis into
            a board-ready strategic report.

            Include:
            - executive summary
            - strategic recommendations
            - strategic risks
            - the original financial and marketing structured data

            Return only the required structured schema.
            """
        ),
        (
            "user",
            """
            Financial analysis:
            {financial_data}

            Marketing analysis:
            {marketing_data}
            """
        )
    ])

    chain = prompt | structured_llm

    return await chain.ainvoke({
        "financial_data": financial_data,
        "marketing_data": marketing_data,
    })
