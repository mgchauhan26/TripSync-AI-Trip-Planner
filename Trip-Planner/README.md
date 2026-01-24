# Trip Planner

A smart itinerary generator that creates day-wise trip plans using LLM and real-time places data.

## Prerequisites

- Node.js installed
- valid `.env` file with `OPENAI_API_KEY` (OpenRouter) and `PLACES_API_KEY` (Geoapify).

## Installation

```bash
npm install
```

## Running the Project

1. Start the server:
   ```bash
   npm start
   ```

2. Open your browser and visit:
   `http://localhost:3000`

3. Enter your destination, budget, number of people, and days to generate an itinerary.

## Architecture

- **Backend**: Node.js + Express
- **Frontend**: HTML/CSS/JS
- **Services**:
  - `llm.service.js`: Connects to OpenRouter (GPT-4o-mini)
  - `places.service.js`: Fetches real places from Geoapify
