from crewai import Task
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import read_data_tool

verification = Task(
    description="Examine the document at the following path: {file_path}. Verify that it is a valid financial report. Extract the company name, document type (e.g., Q2 Update), and reporting period.",
    expected_output="A concise verification statement confirming document validity, company name, and time period.",
    agent=verifier,
    async_execution=False
)

analyze_financial_document = Task(
    description="Using the document at {file_path}, perform a detailed fundamental analysis. Extract exact metrics for revenue, profit margins, cash flow, and deliveries/production. Address the specific user query: {query}",
    expected_output="A comprehensive, factual financial summary detailing exact performance metrics and YoY/QoQ trends.",
    agent=financial_analyst,
    async_execution=False
)

risk_assessment = Task(
    description="Based on the financial analysis provided by the previous task, assess the risks for this company. Identify headwinds like margin compression, tariff impacts, or cash burn.",
    expected_output="A structured list of 3-5 objective financial and operational risks facing the company.",
    agent=risk_assessor,
    async_execution=False
)

investment_analysis = Task(
    description="Synthesize the financial analysis and risk assessment to provide a final investment recommendation regarding the user query: {query}. Should an investor Buy, Hold, or Sell? Justify it with data.",
    expected_output="A professional, data-backed investment recommendation with clear rationale.",
    agent=investment_advisor,
    async_execution=False
)