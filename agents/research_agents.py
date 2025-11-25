"""Research agents for destination, activities, and weather."""

from google.adk.agents import Agent, ParallelAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from config import MODEL_NAME, RETRY_CONFIG


def create_destination_researcher():
    """Create destination research agent."""
    return Agent(
        name="DestinationResearcher",
        model=Gemini(
            model=MODEL_NAME,
            retry_options=RETRY_CONFIG
        ),
        instruction="""You are a destination research specialist.
        
        Your task:
        1. Research the given destination using Google Search
        2. Find information about: top attractions, local culture, must-see landmarks, hidden gems
        3. Focus on recent and popular recommendations
        4. Keep your findings concise (150-200 words)
        5. Include 3-5 specific attraction names with brief descriptions
        
        Format your response as:
        **Top Attractions:**
        - [Attraction 1]: Brief description
        - [Attraction 2]: Brief description
        ...
        """,
        tools=[google_search],
        output_key="destination_research",
    )


def create_activity_finder():
    """Create activity finder agent."""
    return Agent(
        name="ActivityFinder",
        model=Gemini(
            model=MODEL_NAME,
            retry_options=RETRY_CONFIG
        ),
        instruction="""You are an activity and experience specialist.
        
        Your task:
        1. Use Google Search to find activities, tours, and experiences at the destination
        2. Focus on: outdoor activities, cultural experiences, food tours, adventure sports
        3. Include family-friendly and adult options
        4. Provide realistic time estimates for each activity
        5. Keep findings concise (150-200 words)
        
        Format your response as:
        **Recommended Activities:**
        - [Activity 1]: Description (Duration: X hours)
        - [Activity 2]: Description (Duration: X hours)
        ...
        """,
        tools=[google_search],
        output_key="activity_research",
    )


def create_weather_checker():
    """Create weather checker agent."""
    from google.genai import types
    
    return Agent(
        name="WeatherChecker",
        model=Gemini(
            model=MODEL_NAME,
            retry_options=RETRY_CONFIG,
            generation_config=types.GenerateContentConfig(
                temperature=0.7,
            )
        ),
        instruction="""You are a weather research specialist for travel planning.

YOUR MISSION:
Extract the destination and travel dates/months from the user's request, then use Google Search to find accurate weather information.

SEARCH STRATEGY:
1. Search: "[destination] weather [specific month/season] average"
2. Search: "[destination] climate [month]" 
3. Look for: temperature ranges, rainfall, seasonal patterns, typical conditions

WHAT TO FIND:
- Average temperatures (highs and lows)
- Precipitation likelihood (rainy/dry season)
- Weather patterns for that specific time period
- Any extreme weather warnings

OUTPUT FORMAT:
**Weather for [Destination] in [Month/Season]:**
- 🌡️ Temperature: [typical range in °C/°F]
- ☁️ Conditions: [sunny/rainy/mixed + seasonal patterns]
- 🧳 What to Pack: 
  - [Specific clothing items]
  - [Weather accessories needed]
  - [Activity-specific gear if applicable]

Keep your response concise (120-150 words), accurate, and immediately actionable for travelers.
""",
        tools=[google_search],
        output_key="weather_research",
    )


def create_research_team():
    """Create parallel research team."""
    return ParallelAgent(
        name="ResearchTeam",
        sub_agents=[
            create_destination_researcher(),
            create_activity_finder(),
            create_weather_checker()
        ],
    )
