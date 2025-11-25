# 🌍 Vertex Voyages - AI Travel Planning System

A multi-agent travel planner built with Google ADK that demonstrates:
- ✅ Multi-agent orchestration (Sequential, Parallel, Loop)
- ✅ Custom tools + Built-in tools
- ✅ Long-running operations with human approval
- ✅ Sessions & Memory for personalized planning
- ✅ Observability & Evaluation

## 🚀 Quick Start

### Prerequisites
1. Get your [Gemini API key](https://aistudio.google.com/app/api-keys)
2. Python 3.9+

### Installation

```bash
# Clone/navigate to the project
cd vertex_voyages

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### Usage

```python
from main import plan_trip
import asyncio

# Plan a trip
result = asyncio.run(plan_trip(
    user_query="I want to plan a beach vacation to Bali",
    destination="Bali, Indonesia",
    travel_dates="2026-02-10 to 2026-02-15",
    num_days=5,
    num_travelers=2,
    accommodation_level="budget"
))
```

Or run the example:

```bash
python example.py
```

## 📁 Project Structure

```
vertex_voyages/
├── agents/              # Agent definitions
│   ├── research_agents.py
│   ├── planning_agents.py
│   └── coordinator.py
├── tools/               # Custom tools
│   ├── budget_calculator.py
│   ├── destination_validator.py
│   └── booking_approval.py
├── utils/               # Helper functions
│   └── helpers.py
├── config/              # Configuration
│   └── settings.py
├── main.py              # Main workflow
├── example.py           # Usage examples
└── requirements.txt
```

## 🏗️ System Architecture

```
User Query
    ↓
Coordinator Agent (Root)
    ├──→ Validation Agent
    ├──→ Research Team (Parallel)
    │    ├── Destination Researcher
    │    ├── Activity Finder
    │    └── Weather Checker
    ├──→ Planning Pipeline (Sequential)
    │    ├── Itinerary Builder
    │    ├── Budget Calculator
    │    └── Optimizer
    └──→ Booking Agent (Long-Running)
         └── Human Approval for >$1000
```

## 🔧 Features

### Custom Tools
- **Budget Calculator**: Estimates trip costs with breakdown
- **Destination Validator**: Checks safety and seasonal suitability
- **Booking Approval**: Handles high-cost trip approvals (>$1000)

### Agent Types
- **Parallel Agents**: Research team runs concurrently
- **Sequential Agents**: Planning pipeline executes in order
- **Long-Running Operations**: Booking agent can pause for approval

## 📝 License

MIT License
