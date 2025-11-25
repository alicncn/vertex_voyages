"""Booking approval tool for long-running operations."""

from google.adk.tools import ToolContext
from config import APPROVAL_THRESHOLD


def request_booking_approval(
    total_cost: float,
    destination: str,
    num_travelers: int,
    tool_context: ToolContext
) -> dict:
    """Requests human approval for expensive bookings (>$1000).
    
    This is a long-running operation that pauses the agent workflow
    and waits for human confirmation before proceeding.
    
    Args:
        total_cost: Total trip cost in USD
        destination: Destination name
        num_travelers: Number of travelers
        tool_context: Context for pause/resume functionality
    
    Returns:
        Dictionary with approval status
    """
    
    # SCENARIO 1: Cost under threshold - auto-approve
    if total_cost <= APPROVAL_THRESHOLD:
        tool_context.state["booking_approved"] = True
        tool_context.state["approval_reason"] = "auto_approved"
        return {
            "status": "approved",
            "reason": "auto_approved",
            "message": f"Booking auto-approved (${total_cost:.2f} ≤ ${APPROVAL_THRESHOLD})",
            "total_cost": total_cost
        }
    
    # SCENARIO 2: First call - request approval and PAUSE
    if not tool_context.tool_confirmation:
        approval_details = {
            "destination": destination,
            "num_travelers": num_travelers,
            "total_cost": total_cost,
            "threshold": APPROVAL_THRESHOLD
        }
        
        tool_context.request_confirmation(
            hint=f"⚠️ High-cost booking detected!\n"
                 f"Destination: {destination}\n"
                 f"Travelers: {num_travelers}\n"
                 f"Total Cost: ${total_cost:.2f}\n"
                 f"Threshold: ${APPROVAL_THRESHOLD}\n\n"
                 f"Do you approve this booking?",
            payload=approval_details
        )
        
        return {
            "status": "pending",
            "message": f"Booking requires approval (${total_cost:.2f} > ${APPROVAL_THRESHOLD})",
            "awaiting_confirmation": True
        }
    
    # SCENARIO 3: Resumed after human response
    if tool_context.tool_confirmation.confirmed:
        tool_context.state["booking_approved"] = True
        tool_context.state["approval_reason"] = "human_approved"
        return {
            "status": "approved",
            "reason": "human_approved",
            "message": f"Booking approved by user for ${total_cost:.2f}",
            "total_cost": total_cost
        }
    else:
        tool_context.state["booking_approved"] = False
        tool_context.state["approval_reason"] = "rejected"
        return {
            "status": "rejected",
            "message": f"Booking rejected by user for ${total_cost:.2f}",
            "total_cost": total_cost
        }
