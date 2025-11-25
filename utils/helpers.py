"""Helper utilities for approval workflow and response handling."""

from google.genai import types


def check_for_approval(events):
    """Check if events contain an approval request.
    
    Args:
        events: List of event objects from agent execution
    
    Returns:
        dict with approval details or None
    """
    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if (
                    part.function_call
                    and part.function_call.name == "adk_request_confirmation"
                ):
                    return {
                        "approval_id": part.function_call.id,
                        "invocation_id": event.invocation_id,
                    }
    return None


def create_approval_response(approval_info, approved: bool):
    """Create approval response message.
    
    Args:
        approval_info: Dictionary with approval_id and invocation_id
        approved: Boolean indicating approval decision
    
    Returns:
        Content object with function response
    """
    confirmation_response = types.FunctionResponse(
        id=approval_info["approval_id"],
        name="adk_request_confirmation",
        response={"confirmed": approved},
    )
    return types.Content(
        role="user", 
        parts=[types.Part(function_response=confirmation_response)]
    )


def print_agent_response(events):
    """Print agent's text responses from events.
    
    Args:
        events: List of event objects from agent execution
    """
    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(f"🤖 Agent: {part.text}")
