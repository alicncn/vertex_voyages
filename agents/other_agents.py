"""Validation and booking agents."""

from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import FunctionTool
from config import MODEL_NAME, RETRY_CONFIG
from tools.destination_validator import validate_destination
from tools.booking_approval import request_booking_approval


def create_validation_agent():
    """Create destination validation agent."""
    return Agent(
        name="ValidationAgent",
        model=Gemini(
            model=MODEL_NAME,
            retry_options=RETRY_CONFIG
        ),
        instruction="""You are a travel safety and feasibility validator.
        
        Your task:
        1. Extract the destination and travel dates from the user's request
        2. Use the validate_destination tool with these parameters
        3. Report the safety rating and any travel warnings
        4. Provide recommendations based on the validation results
        
        IMPORTANT: 
        - If dates are mentioned in the request (like "2025-06-15 to 2025-06-20"), use them directly
        - If destination is mentioned, use it directly
        - Do NOT ask for more information - extract from the request
        
        Always call validate_destination first, then summarize the results clearly.
        
        Format:
        **Destination Validation:**
        - Safety Rating: X/5.0
        - Best Months: [list]
        - Warnings: [list or "None"]
        - Recommendation: [Your advice]
        """,
        tools=[FunctionTool(func=validate_destination)],
        output_key="validation_result",
    )


def create_booking_agent():
    """Create booking agent."""
    return Agent(
        name="BookingAgent",
        model=Gemini(
            model=MODEL_NAME,
            retry_options=RETRY_CONFIG
        ),
        instruction="""You are a travel booking specialist.
        
        Your task:
        1. Extract the total cost from the budget analysis: {budget_analysis}
        2. Extract destination and traveler count from the user's request
        3. Use the request_booking_approval tool to check if approval is needed
        4. If status is "pending", inform the user that approval is required
        5. If status is "approved" or "rejected", provide a clear summary
        
        Always use the request_booking_approval tool first, then respond based on the result.
        
        Response format:
        **Booking Status:** [Approved/Pending/Rejected]
        **Total Cost:** $X,XXX.XX
        **Next Steps:** [What happens next]
        """,
        tools=[FunctionTool(func=request_booking_approval)],
        output_key="booking_status",
    )
