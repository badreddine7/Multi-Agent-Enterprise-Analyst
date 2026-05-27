from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def create_pdf(filename: str, title: str, sections: list[tuple[str, str]]):
    doc = SimpleDocTemplate(filename, pagesize=LETTER)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(title, styles["Title"]))
    story.append(Spacer(1, 16))

    for heading, body in sections:
        story.append(Paragraph(heading, styles["Heading1"]))
        story.append(Paragraph(body.replace("\n", "<br/>"), styles["BodyText"]))
        story.append(Spacer(1, 12))

    doc.build(story)


financial_sections = [
    (
        "Company Overview",
        """
        Acme Cloud Systems Inc. is a mid-market enterprise software company that provides
        cloud infrastructure monitoring, workflow automation, and analytics tools for
        B2B customers in finance, healthcare, and logistics.
        """
    ),
    (
        "Fiscal Year 2024 Financial Performance",
        """
        For fiscal year 2024, Acme Cloud Systems reported total revenue of $248.6 million,
        compared with $207.1 million in fiscal year 2023. This represents year-over-year
        revenue growth of approximately 20.0%.

        Subscription revenue accounted for $211.3 million, while professional services
        revenue contributed $37.3 million. Gross profit for the year was $174.0 million,
        resulting in a gross margin of 70.0%.

        Operating income was $31.5 million, compared with $22.4 million in the prior year.
        Net income was $24.8 million, up from $17.9 million in fiscal year 2023.
        """
    ),
    (
        "Expense Breakdown",
        """
        Sales and marketing expenses were $78.2 million, representing 31.5% of total revenue.
        Research and development expenses were $41.6 million, representing 16.7% of revenue.
        General and administrative expenses were $22.7 million.

        The company continued to invest in product development, particularly in AI-assisted
        monitoring features and enterprise security integrations.
        """
    ),
    (
        "Cash Flow and Balance Sheet",
        """
        Acme generated $38.9 million in operating cash flow during fiscal year 2024.
        Free cash flow was $30.2 million after capital expenditures. The company ended
        the year with $96.4 million in cash and equivalents and $42.0 million in long-term debt.

        Management stated that the current liquidity position is sufficient to fund planned
        operations and strategic investments for the next 18 to 24 months.
        """
    ),
    (
        "Key Risks",
        """
        The company faces several financial and operational risks:

        1. Customer concentration risk: the top five customers represent 29% of annual recurring revenue.
        2. Margin pressure: increased cloud infrastructure costs may reduce gross margin.
        3. Competitive pricing risk: larger cloud vendors may bundle similar monitoring tools.
        4. Sales cycle risk: enterprise customers are taking longer to approve large software contracts.
        5. International expansion risk: foreign exchange volatility may affect future revenue.
        """
    ),
    (
        "Management Outlook",
        """
        Management expects fiscal year 2025 revenue to be between $292 million and $305 million.
        The company targets gross margin between 68% and 71% and expects continued investment
        in sales capacity, AI product development, and partner integrations.

        The company expects year-over-year growth to remain above 17%, although management
        warned that enterprise budget scrutiny could create quarterly volatility.
        """
    ),
]


marketing_sections = [
    (
        "Competitor Overview",
        """
        NovaStack Technologies is a competing enterprise cloud operations platform.
        The company targets mid-market and large enterprise customers that need centralized
        observability, incident response automation, and cost optimization tools.
        """
    ),
    (
        "Market Positioning",
        """
        NovaStack positions itself as an AI-first cloud operations platform. Its messaging
        emphasizes faster incident resolution, automated root-cause analysis, and lower
        infrastructure costs.

        The company uses the tagline: "Autonomous CloudOps for Modern Engineering Teams."
        Its brand voice is technical, confident, and focused on engineering productivity.
        """
    ),
    (
        "Top Marketing Channels",
        """
        NovaStack's top marketing channels include:

        1. LinkedIn advertising targeted at engineering leaders, CTOs, and DevOps managers.
        2. Technical webinars focused on cloud cost reduction and incident response.
        3. SEO-driven blog content around Kubernetes monitoring and cloud observability.
        4. Partner marketing with cloud consulting firms and managed service providers.
        5. Conference sponsorships at DevOps, SRE, and cloud infrastructure events.
        """
    ),
    (
        "Notable Campaigns",
        """
        NovaStack launched a campaign called "Resolve Incidents Before Users Notice."
        The campaign included LinkedIn video ads, customer case studies, and an interactive
        ROI calculator.

        Another campaign, "Cut Cloud Waste by 30%," targeted CFOs and infrastructure leaders.
        It highlighted cost optimization dashboards and automated recommendations for
        underused cloud resources.
        """
    ),
    (
        "Target Audience",
        """
        NovaStack primarily targets:
        - CTOs
        - VPs of Engineering
        - DevOps Managers
        - Site Reliability Engineering teams
        - Cloud infrastructure leaders
        - Finance leaders concerned with cloud spend

        The company appears strongest among engineering-led organizations with complex
        Kubernetes and multi-cloud environments.
        """
    ),
    (
        "Competitor Strengths",
        """
        NovaStack has several marketing and product strengths:

        1. Clear AI-first positioning that differentiates it from traditional monitoring vendors.
        2. Strong technical content that ranks well for cloud observability keywords.
        3. Effective use of ROI calculators and cost-saving messaging.
        4. Strong partner ecosystem with cloud consultants.
        5. Good credibility with DevOps and SRE audiences.
        """
    ),
    (
        "Competitor Weaknesses",
        """
        NovaStack also has several weaknesses:

        1. Messaging may be too technical for business executives.
        2. Limited evidence of success in regulated industries like healthcare and finance.
        3. Pricing is perceived as expensive by smaller mid-market customers.
        4. Heavy focus on Kubernetes may limit appeal to companies with simpler infrastructure.
        5. Brand awareness is still lower than larger cloud platform vendors.
        """
    ),
    (
        "Strategic Implications",
        """
        Acme Cloud Systems can compete against NovaStack by emphasizing enterprise trust,
        stronger compliance features, simpler onboarding, and predictable pricing.

        Acme should create more business-oriented content for CFOs and CIOs, while still
        maintaining technical credibility with engineering teams. Acme can also differentiate
        through industry-specific case studies in finance, healthcare, and logistics.
        """
    ),
]


create_pdf(
    filename="sample_financial_report.pdf",
    title="Acme Cloud Systems Inc. - Fiscal Year 2024 Financial Report",
    sections=financial_sections,
)

create_pdf(
    filename="sample_competitor_marketing_report.pdf",
    title="NovaStack Technologies - Competitor Marketing Intelligence Report",
    sections=marketing_sections,
)

print("Generated sample_financial_report.pdf")
print("Generated sample_competitor_marketing_report.pdf")
