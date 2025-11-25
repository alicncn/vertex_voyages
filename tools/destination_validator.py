"""Destination validation tool for travel planning."""

from google.adk.tools import ToolContext


def validate_destination(
    destination: str,
    travel_dates: str,
    tool_context: ToolContext
) -> dict:
    """Validates if a destination is safe and suitable for travel during specified dates.
    
    Args:
        destination: City or country name (e.g., "Bali, Indonesia")
        travel_dates: Date range in format "YYYY-MM-DD to YYYY-MM-DD"
        tool_context: Context for storing state
    
    Returns:
        Dictionary with validation status, safety rating, and recommendations
    """
    
    # Mock validation database (in production, use real travel advisory APIs)
    destination_info = {
        "paris": {
            "safe": True,
            "safety_rating": 4.2,
            "best_months": ["Apr", "May", "Sep", "Oct"],
            "warnings": []
        },
        "tokyo": {
            "safe": True,
            "safety_rating": 4.8,
            "best_months": ["Mar", "Apr", "Oct", "Nov"],
            "warnings": ["Typhoon season: Aug-Sep"]
        },
        "bali": {
            "safe": True,
            "safety_rating": 4.5,
            "best_months": ["Apr", "May", "Jun", "Sep"],
            "warnings": ["Rainy season: Nov-Mar"]
        },
        "new york": {
            "safe": True,
            "safety_rating": 4.0,
            "best_months": ["Apr", "May", "Sep", "Oct"],
            "warnings": ["Very cold winters"]
        },
        "istanbul": {
            "safe": True,
            "safety_rating": 4.3,
            "best_months": ["Apr", "May", "Sep", "Oct"],
            "warnings": []
        }
    }
    
    # Normalize destination
    dest_key = destination.lower().split(",")[0].strip()
    
    # Find matching destination
    info = None
    matched_dest = "Unknown"
    for key in destination_info:
        if key in dest_key or dest_key in key:
            info = destination_info[key]
            matched_dest = key.title()
            break
    
    if info is None:
        # Default for unknown destinations
        info = {
            "safe": True,
            "safety_rating": 3.5,
            "best_months": [],
            "warnings": ["Limited information available - verify travel advisories"]
        }
    
    # Store in session state
    tool_context.state["validated_destination"] = destination
    tool_context.state["destination_safe"] = info["safe"]
    tool_context.state["safety_rating"] = info["safety_rating"]
    
    return {
        "status": "success",
        "destination": destination,
        "matched_location": matched_dest,
        "is_safe": info["safe"],
        "safety_rating": f"{info['safety_rating']}/5.0",
        "best_months_to_visit": info["best_months"],
        "travel_warnings": info["warnings"],
        "recommendation": "Approved for travel" if info["safe"] else "Check travel advisories",
        "travel_dates": travel_dates
    }
