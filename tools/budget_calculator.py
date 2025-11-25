"""Budget calculation tool for travel planning."""

from google.adk.tools import ToolContext


def calculate_trip_budget(
    destination: str,
    num_days: int,
    num_travelers: int,
    accommodation_level: str,
    tool_context: ToolContext
) -> dict:
    """Calculates estimated trip budget based on destination and preferences.
    
    Args:
        destination: City or country name (e.g., "Paris, France")
        num_days: Number of days for the trip
        num_travelers: Number of people traveling
        accommodation_level: "budget", "mid-range", or "luxury"
        tool_context: Context for storing state
    
    Returns:
        Dictionary with budget breakdown and total cost
    """
    
    # Mock pricing database (in production, this would call a real API)
    base_costs = {
        "paris": {"budget": 80, "mid-range": 150, "luxury": 350},
        "tokyo": {"budget": 70, "mid-range": 140, "luxury": 400},
        "bali": {"budget": 40, "mid-range": 90, "luxury": 250},
        "new york": {"budget": 100, "mid-range": 200, "luxury": 500},
        "istanbul": {"budget": 50, "mid-range": 100, "luxury": 220},
    }
    
    # Normalize destination
    dest_key = destination.lower().split(",")[0].strip()
    
    # Find matching destination
    daily_cost = None
    for key in base_costs:
        if key in dest_key or dest_key in key:
            daily_cost = base_costs[key].get(accommodation_level.lower(), 150)
            break
    
    if daily_cost is None:
        # Default for unknown destinations
        daily_cost = {"budget": 60, "mid-range": 120, "luxury": 300}[accommodation_level.lower()]
    
    # Calculate breakdown
    accommodation = daily_cost * 0.4 * num_days * num_travelers
    food = daily_cost * 0.3 * num_days * num_travelers
    activities = daily_cost * 0.2 * num_days * num_travelers
    transport = daily_cost * 0.1 * num_days * num_travelers
    
    total = accommodation + food + activities + transport
    
    # Store in session state
    tool_context.state["last_budget"] = total
    tool_context.state["budget_breakdown"] = {
        "accommodation": accommodation,
        "food": food,
        "activities": activities,
        "transport": transport,
        "total": total
    }
    
    return {
        "status": "success",
        "destination": destination,
        "num_days": num_days,
        "num_travelers": num_travelers,
        "accommodation_level": accommodation_level,
        "breakdown": {
            "accommodation": f"${accommodation:.2f}",
            "food": f"${food:.2f}",
            "activities": f"${activities:.2f}",
            "local_transport": f"${transport:.2f}"
        },
        "total_estimated_cost": f"${total:.2f}"
    }
