"""Main travel planning workflow."""

import os
import uuid
from datetime import datetime

from google.genai import types
from google.adk.apps.app import App, ResumabilityConfig
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.plugins import LoggingPlugin

from config import DEFAULT_USER_ID, APP_NAME
from agents.coordinator import create_coordinator
from utils.helpers import check_for_approval, create_approval_response, print_agent_response


# Initialize services
session_service = InMemorySessionService()


def create_app():
    """Create and configure the Vertex Voyages app."""
    coordinator = create_coordinator()
    
    app = App(
        name=APP_NAME,
        root_agent=coordinator,
        resumability_config=ResumabilityConfig(
            is_resumable=True
        ),
        plugins=[LoggingPlugin()]
    )
    
    return app


def create_runner():
    """Create and configure the runner."""
    app = create_app()
    runner = Runner(
        app=app,
        session_service=session_service,
    )
    return runner


async def plan_trip(
    user_query: str,
    destination: str,
    travel_dates: str,
    num_days: int,
    num_travelers: int,
    accommodation_level: str = "mid-range",
    auto_approve: bool = True
) -> dict:
    """Main workflow function for Vertex Voyages travel planning.
    
    Args:
        user_query: Natural language travel request
        destination: Destination name (e.g., "Paris, France")
        travel_dates: Date range "YYYY-MM-DD to YYYY-MM-DD"
        num_days: Number of days for the trip
        num_travelers: Number of travelers
        accommodation_level: "budget", "mid-range", or "luxury"
        auto_approve: Auto-approve bookings for testing (True) or require manual approval (False)
    
    Returns:
        Dictionary with complete travel plan and status
    """
    
    print(f"\n{'='*70}")
    print(f"🌍 VERTEX VOYAGES - Travel Planning System")
    print(f"{'='*70}")
    print(f"📍 Destination: {destination}")
    print(f"📅 Dates: {travel_dates}")
    print(f"👥 Travelers: {num_travelers}")
    print(f"🏨 Level: {accommodation_level}")
    print(f"{'='*70}\n")
    
    # Generate unique session ID
    session_id = f"trip_{uuid.uuid4().hex[:8]}"
    
    # Create runner
    runner = create_runner()
    
    # Create session
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=DEFAULT_USER_ID,
        session_id=session_id
    )
    
    # Prepare user message
    enhanced_query = f"""{user_query}
    
Trip Details:
- Destination: {destination}
- Dates: {travel_dates}
- Duration: {num_days} days
- Travelers: {num_travelers}
- Accommodation: {accommodation_level}
"""
    
    query_content = types.Content(
        role="user",
        parts=[types.Part(text=enhanced_query)]
    )
    
    events = []
    
    # STEP 1: Send initial request to coordinator
    print("🚀 Starting travel planning workflow...\n")
    
    async for event in runner.run_async(
        user_id=DEFAULT_USER_ID,
        session_id=session_id,
        new_message=query_content
    ):
        events.append(event)
    
    # STEP 2: Check for approval request (long-running operation)
    approval_info = check_for_approval(events)
    
    if approval_info:
        print(f"\n{'='*70}")
        print("⏸️  BOOKING APPROVAL REQUIRED")
        print(f"{'='*70}")
        print(f"💰 Trip cost exceeds $1,000 threshold")
        print(f"🤔 Simulated Human Decision: {'APPROVE ✅' if auto_approve else 'REJECT ❌'}\n")
        
        # STEP 3: Resume with approval decision
        async for event in runner.run_async(
            user_id=DEFAULT_USER_ID,
            session_id=session_id,
            new_message=create_approval_response(approval_info, auto_approve),
            invocation_id=approval_info["invocation_id"]
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(f"🤖 Agent: {part.text}")
    else:
        # No approval needed - print response
        print_agent_response(events)
    
    print(f"\n{'='*70}")
    print("✅ TRAVEL PLANNING COMPLETE")
    print(f"{'='*70}\n")
    
    return {
        "session_id": session_id,
        "status": "complete",
        "destination": destination,
        "dates": travel_dates
    }


if __name__ == "__main__":
    import asyncio
    
    # Example usage
    result = asyncio.run(plan_trip(
        user_query="I want to plan a relaxing beach vacation to Bali with my partner.",
        destination="Bali, Indonesia",
        travel_dates="2026-02-10 to 2026-02-15",
        num_days=5,
        num_travelers=2,
        accommodation_level="budget",
        auto_approve=True
    ))
    
    print(f"\n✅ Complete - Session ID: {result['session_id']}")
