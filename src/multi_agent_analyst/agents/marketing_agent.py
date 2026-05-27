from multi_agent_analyst.llms import get_gemini_llm
from langchain_core.prompts import ChatPromptTemplate
from multi_agent_analyst.schemas.models import MarketingInsights


llm = get_gemini_llm(max_output_tokens=1200)
structured_llm = llm.with_structured_output(MarketingInsights)


async def run_marketing_agent(doc_text: str) -> MarketingInsights:
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are a marketing intelligence analyst.

            Analyze the competitor's marketing document.
            Extract marketing channels, positioning, strengths, weaknesses,
            target audience, and notable campaigns.

            Rules:
            - Return only information matching the required structured schema.
            - If information is missing, use null or an empty list.
            """
        ),
        ("user", "{doc}")
    ])

    chain = prompt | structured_llm
    return await chain.ainvoke({"doc": doc_text})
