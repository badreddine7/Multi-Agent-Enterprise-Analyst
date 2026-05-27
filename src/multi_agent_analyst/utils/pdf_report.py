from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet
from pathlib import Path
from multi_agent_analyst.schemas.models import FinalReport
import uuid


def _bullet_list(items: list[str], styles):
    if not items:
        return Paragraph("None provided.", styles["BodyText"])

    return ListFlowable(
        [ListItem(Paragraph(item, styles["BodyText"])) for item in items],
        bulletType="bullet"
    )


def generate_pdf_report(report: FinalReport, output_dir: str = "generated_reports") -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    file_name = f"enterprise_analysis_{uuid.uuid4().hex}.pdf"
    pdf_path = str(Path(output_dir) / file_name)

    doc = SimpleDocTemplate(pdf_path, pagesize=LETTER)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Multi-Agent Enterprise Analyst Report", styles["Title"]))
    story.append(Spacer(1, 16))

    story.append(Paragraph("Executive Summary", styles["Heading1"]))
    story.append(Paragraph(report.executive_summary, styles["BodyText"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Financial Analysis", styles["Heading1"]))
    financial = report.financial

    financial_lines = [
        f"Revenue: {financial.revenue}",
        f"Gross Margin %: {financial.gross_margin_pct}",
        f"YoY Growth %: {financial.yoy_growth_pct}",
        f"Operating Income: {financial.operating_income}",
        f"Net Income: {financial.net_income}",
    ]

    for line in financial_lines:
        story.append(Paragraph(line, styles["BodyText"]))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Financial Risks", styles["Heading2"]))
    story.append(_bullet_list(financial.key_risks, styles))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Marketing Analysis", styles["Heading1"]))
    marketing = report.marketing

    story.append(Paragraph(f"Positioning: {marketing.positioning_summary}", styles["BodyText"]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Top Channels", styles["Heading2"]))
    story.append(_bullet_list(marketing.top_channels, styles))

    story.append(Paragraph("Competitor Strengths", styles["Heading2"]))
    story.append(_bullet_list(marketing.competitor_strengths, styles))

    story.append(Paragraph("Competitor Weaknesses", styles["Heading2"]))
    story.append(_bullet_list(marketing.competitor_weaknesses, styles))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Strategic Recommendations", styles["Heading1"]))
    story.append(_bullet_list(report.recommendations, styles))

    story.append(Paragraph("Strategic Risks", styles["Heading1"]))
    story.append(_bullet_list(report.strategic_risks, styles))

    doc.build(story)

    return pdf_path
