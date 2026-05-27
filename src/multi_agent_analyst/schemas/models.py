from pydantic import BaseModel, Field
from typing import List, Optional


class FinancialMetrics(BaseModel):
    revenue: Optional[float] = Field(default=None, description="Total company revenue in euros")
    gross_margin_pct: Optional[float] = Field(default=None, description="Gross margin percentage")
    yoy_growth_pct: Optional[float] = Field(default=None, description="Year-over-year growth percentage")
    operating_income: Optional[float] = Field(default=None, description="Operating income if available in euros")
    net_income: Optional[float] = Field(default=None, description="Net income if available in euros")
    key_risks: List[str] = Field(default_factory=list)


class MarketingInsights(BaseModel):
    top_channels: List[str] = Field(default_factory=list)
    positioning_summary: str = ""
    competitor_strengths: List[str] = Field(default_factory=list)
    competitor_weaknesses: List[str] = Field(default_factory=list)
    target_audience: Optional[str] = None
    notable_campaigns: List[str] = Field(default_factory=list)


class FinalReport(BaseModel):
    financial: FinancialMetrics
    marketing: MarketingInsights
    recommendations: List[str]
    executive_summary: str
    strategic_risks: List[str] = Field(default_factory=list)
    pdf_path: Optional[str] = None
