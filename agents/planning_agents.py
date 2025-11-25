"""Planning agents for itinerary, budget, and optimization."""

from google.adk.agents import Agent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import FunctionTool
from config import MODEL_NAME, RETRY_CONFIG
from tools.budget_calculator import calculate_trip_budget


def create_itinerary_builder():
    """Create itinerary builder agent."""
    return Agent(
        name="ItineraryBuilder",
        model=Gemini(
            model=MODEL_NAME,
            retry_options=RETRY_CONFIG
        ),
        instruction="""You are an expert travel itinerary planner.
        
        Using the research data:
        - Destination Info: {destination_research}
        - Activities: {activity_research}
        - Weather: {weather_research}
        
        Create a day-by-day itinerary that:
        1. Balances popular attractions with unique experiences
        2. Groups nearby locations together to minimize travel time
        3. Considers weather conditions and best times for outdoor activities
        4. Includes realistic time allocations (travel time, activity duration, meals)
        5. Provides morning, afternoon, and evening plans for each day
        6. Leaves some flexibility for spontaneous exploration
        
        Format as:
        **Day 1:**
        - Morning (9:00-12:00): [Activity + location]
        - Afternoon (13:00-17:00): [Activity + location]
        - Evening (18:00-21:00): [Activity + location]
        
        Keep it concise and practical. Total length: 200-300 words.
        """,
        output_key="itinerary_draft",
    )


def create_budget_calculator():
    """Create budget calculator agent."""
    return Agent(
        name="BudgetCalculator",
        model=Gemini(
            model=MODEL_NAME,
            retry_options=RETRY_CONFIG
        ),
        instruction="""You are a travel budget specialist.
        
        Your task:
        1. Use the calculate_trip_budget tool with the user's preferences
        2. Present the budget breakdown clearly
        3. Provide money-saving tips specific to the destination
        4. Suggest budget adjustments if costs seem too high
        
        Always call the calculate_trip_budget tool first, then explain the results.
        
        Format your response as:
        **Budget Breakdown:**
        [Show the breakdown from the tool]
        
        **Money-Saving Tips:**
        - [Tip 1]
        - [Tip 2]
        - [Tip 3]
        """,
        tools=[FunctionTool(func=calculate_trip_budget)],
        output_key="budget_analysis",
    )


def create_optimizer():
    """Create optimizer agent."""
    return Agent(
        name="OptimizerAgent",
        model=Gemini(
            model=MODEL_NAME,
            retry_options=RETRY_CONFIG
        ),
        instruction="""You are a travel plan optimization specialist.
        
        Review the itinerary and budget:
        - Itinerary: {itinerary_draft}
        - Budget: {budget_analysis}
        
        Your task:
        1. Identify potential issues (too rushed, too expensive, poor timing)
        2. Suggest optimizations (better routes, cheaper alternatives, time savings)
        3. Ensure the plan is realistic and enjoyable
        4. Keep the final output concise (150-200 words)
        
        Format as:
        **Optimized Plan:**
        [Key improvements made]
        
        **Final Recommendations:**
        - [Recommendation 1]
        - [Recommendation 2]
        - [Recommendation 3]
        """,
        output_key="optimized_plan",
    )


def create_planning_pipeline():
    """Create sequential planning pipeline."""
    return SequentialAgent(
        name="PlanningPipeline",
        sub_agents=[
            create_itinerary_builder(),
            create_budget_calculator(),
            create_optimizer()
        ],
    )
