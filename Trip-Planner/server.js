import "dotenv/config";
import express from "express";
import path from "path";
import { fileURLToPath } from "url";
import { callLLM } from "./services/llm.service.js";
import { buildPrompt } from "./services/prompt.builder.js";
import { getPlacesByName, getCoordinates } from "./services/places.service.js";
import { getRestaurants } from "./services/dining.service.js";
import { getHotels } from "./services/hotel.service.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// Stream itinerary generation
app.post("/api/plan-trip", async (req, res) => {
  const { destination, budget, people, days } = req.body;

  if (!destination || !budget || !people || !days) {
    return res.status(400).json({ message: "All fields are required" });
  }

  // Calculate Budget Tier based on Total Budget
  const totalBudget = parseInt(budget);
  let budgetTier = "Medium"; // Default

  if (totalBudget < 20000) {
    budgetTier = "Low";
  } else if (totalBudget >= 20000 && totalBudget <= 30000) {
    budgetTier = "Medium";
  } else if (totalBudget > 30000) {
    budgetTier = "High";
  }

  // Set headers for streaming
  res.setHeader('Content-Type', 'text/plain; charset=utf-8');
  res.setHeader('Transfer-Encoding', 'chunked');

  // Stream function (simulating typing effect, but faster)
  const stream = async (text) => {
    // Send larger chunks for better performance
    const chunkSize = 5;
    for (let i = 0; i < text.length; i += chunkSize) {
      await new Promise(resolve => {
        res.write(text.slice(i, i + chunkSize));
        setTimeout(resolve, 5); // Faster typing speed
      });
    }
  };

  try {
    // 1. Get Context (Real places, Dining, Hotels)
    console.log(`Fetching context for ${destination}...`);

    // Fetch coordinates first for specific searches
    const coords = await getCoordinates(destination);

    let placesPromise = getPlacesByName(destination);
    let diningPromise = Promise.resolve([]);
    let hotelsPromise = Promise.resolve([]);

    if (coords) {
      // If we have coords, we can fetch dining and hotels nearby
      diningPromise = getRestaurants(coords.lat, coords.lon);
      hotelsPromise = getHotels(coords.lat, coords.lon);
    }

    const [places, dining, hotels] = await Promise.all([placesPromise, diningPromise, hotelsPromise]);

    // 2. Build Prompt
    console.log("Building prompt...");
    const prompt = buildPrompt({ destination, budget: totalBudget, budgetTier, people, days }, { places, dining, hotels });

    // 3. Call LLM
    console.log("Calling LLM...");
    const itinerary = await callLLM(prompt);

    // 4. Stream response
    await stream(itinerary);
    res.end();
  } catch (error) {
    console.error("Error in plan-trip:", error);
    // If headers aren't sent yet
    if (!res.headersSent) {
      res.status(500).json({ message: "Error generating itinerary" });
    } else {
      res.write("\n\nError: Failed to complete itinerary generation.");
      res.end();
    }
  }
});

app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});