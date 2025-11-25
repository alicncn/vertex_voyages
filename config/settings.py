"""Configuration settings for Vertex Voyages."""

import os
from dotenv import load_dotenv
from google.genai import types

# Load environment variables
load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Model Configuration
MODEL_NAME = "gemini-2.5-flash-lite"

# Retry Configuration
RETRY_CONFIG = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504]
)

# Booking Configuration
APPROVAL_THRESHOLD = 1000.0  # USD

# Session Configuration
DEFAULT_USER_ID = "traveler_001"
APP_NAME = "VertexVoyages"
