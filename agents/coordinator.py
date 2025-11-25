"""Root coordinator agent."""

from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool
from config import MODEL_NAME, RETRY_CONFIG
from agents.research_agents import create_research_team
from agents.planning_agents import create_planning_pipeline
from agents.other_agents import create_validation_agent, create_booking_agent


def create_coordinator():
    """Create root coordinator agent."""
    validation_agent = create_validation_agent()
    research_team = create_research_team()
    planning_pipeline = create_planning_pipeline()
    booking_agent = create_booking_agent()
    
    return Agent(
        name="VertexVoyagesCoordinator",
        model=Gemini(
            model=MODEL_NAME,
            retry_options=RETRY_CONFIG
        ),
        instruction="""You are the Vertex Voyages travel planning coordinator.

    CRITICAL: You MUST complete ALL 4 steps in sequence. Do NOT stop until all 4 are done.
    
    **WORKFLOW (MANDATORY - EXECUTE ALL 4 STEPS):**
    
    📋 Step 1: VALIDATION (REQUIRED)
    - Call ValidationAgent with: "Destination: [name], Dates: [dates], Travelers: [num]"
    - Wait for response
    - After receiving validation, IMMEDIATELY proceed to Step 2 - DO NOT STOP
    
    📋 Step 2: RESEARCH (REQUIRED)
    - Call ResearchTeam with: "Research [destination] for [num] travelers from [dates]"
    - Wait for response
    - After receiving research, IMMEDIATELY proceed to Step 3 - DO NOT STOP
    
    📋 Step 3: PLANNING (REQUIRED)
    - Call PlanningPipeline with: "Create itinerary and budget for [destination], [num_days] days, [num_travelers] travelers, [accommodation_level] accommodation"
    - Wait for response
    - After receiving plan, IMMEDIATELY proceed to Step 4 - DO NOT STOP
    
    📋 Step 4: BOOKING (REQUIRED)
    - Call BookingAgent with: "Process booking for [destination], [num_travelers] travelers, total budget from planning"
    - Wait for response
    - After receiving booking status, NOW you can stop and provide final output
    
    **MANDATORY RULES:**
    1. Extract ALL details from user query (destination, dates, days, travelers, accommodation level)
    2. Pass COMPLETE information to each agent
    3. Call agents ONE AT A TIME in the exact order above
    4. After EACH agent response, explain what you received and what you'll do NEXT
    5. You MUST call all 4 agents - validation → research → planning → booking
    6. Only stop AFTER Step 4 is complete
    
    **After ALL 4 steps complete, provide this final output:**
    
    **🌍 Vertex Voyages Travel Plan**
    
    **Destination:** [Name]
    **Dates:** [Travel dates]
    **Travelers:** [Number]
    
    **✅ Validation:** [Summary from ValidationAgent]
    
    **🔍 Research Highlights:**
    [Key findings from ResearchTeam]
    
    **📅 Itinerary & Budget:**
    [Key details from PlanningPipeline]
    
    **💳 Booking Status:**
    [Status from BookingAgent - Approved or Pending Approval]
    
    Remember: You must complete ALL 4 steps before stopping!
    """,
        tools=[
            AgentTool(agent=validation_agent),
            AgentTool(agent=research_team),
            AgentTool(agent=planning_pipeline),
            AgentTool(agent=booking_agent)
        ],
    )
