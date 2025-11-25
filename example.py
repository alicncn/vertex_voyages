"""Example usage of Vertex Voyages travel planning system."""

import asyncio
from main import plan_trip


async def example_budget_trip():
    """Example 1: Budget-friendly trip to Bali (auto-approved)."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Budget Trip to Bali")
    print("Expected: Auto-approval (cost < $1,000)")
    print("="*70)
    
    result = await plan_trip(
        user_query="I want to plan a relaxing beach vacation to Bali with my partner.",
        destination="Bali, Indonesia",
        travel_dates="2026-02-10 to 2026-02-15",
        num_days=5,
        num_travelers=2,
        accommodation_level="budget",
        auto_approve=True
    )
    
    print(f"\n✅ Example 1 Complete - Session ID: {result['session_id']}")
    return result


async def example_luxury_trip():
    """Example 2: Luxury trip to Paris (requires approval)."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Luxury Trip to Paris")
    print("Expected: Pauses for approval (cost > $1,000)")
    print("="*70)
    
    result = await plan_trip(
        user_query="Plan a romantic luxury getaway to Paris for our anniversary.",
        destination="Paris, France",
        travel_dates="2026-09-01 to 2026-09-08",
        num_days=7,
        num_travelers=2,
        accommodation_level="luxury",
        auto_approve=True  # Change to False to simulate rejection
    )
    
    print(f"\n✅ Example 2 Complete - Session ID: {result['session_id']}")
    return result


async def example_midrange_trip():
    """Example 3: Mid-range trip to Tokyo."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Mid-Range Trip to Tokyo")
    print("Expected: May require approval depending on duration")
    print("="*70)
    
    result = await plan_trip(
        user_query="Plan a cultural exploration trip to Tokyo with traditional experiences.",
        destination="Tokyo, Japan",
        travel_dates="2026-11-10 to 2026-11-15",
        num_days=5,
        num_travelers=2,
        accommodation_level="mid-range",
        auto_approve=True
    )
    
    print(f"\n✅ Example 3 Complete - Session ID: {result['session_id']}")
    return result


async def main():
    """Run all examples."""
    print("\n" + "="*70)
    print("🌍 VERTEX VOYAGES - EXAMPLE DEMONSTRATIONS")
    print("="*70)
    
    # Run examples
    await example_budget_trip()
    
    # Uncomment to run additional examples
    # await example_luxury_trip()
    # await example_midrange_trip()
    
    print("\n" + "="*70)
    print("✅ ALL EXAMPLES COMPLETE")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
