export function buildPrompt(user, context = {}) {
  const { destination, source, budget, budgetTier, people, days, transportMode, preferences } = user;
  const places = context.places ? context.places.map(p => p.name).join(", ") : "Main attractions";
  const dining = context.dining ? context.dining.map(d => `${d.name} (${d.cuisine || 'Local'} - ${d.address || d.city || 'Nearby'})`).join(", ") : "Local food spots";
  const hotels = context.hotels ? context.hotels.map(h => `${h.name} (${h.type} - ${h.city || 'Nearby'})`).join(", ") : "Standard hotels";

  return `
SYSTEM:
You are a professional travel planner.
Create a detailed, day-by-day itinerary for a trip from ${source} to ${destination}.
You must account for a TOTAL budget of ₹${budget} (${budgetTier} Budget) for ${people} people.
The itinerary should be practical, listing specific places to visit, estimated costs, and timing.
IMPORTANT: All costs must be in Indian Rupees (₹). Do not use USD ($).
IMPORTANT: Include transportation details from ${source} to ${destination} using ${transportMode}.
IMPORTANT: Focus on activities and places that match these preferences: ${preferences}.

USER:
Source: ${source}
Destination: ${destination}
Duration: ${days} days
Travelers: ${people} person(s)
Budget Limit: ₹${budget} (${budgetTier})
Transportation: ${transportMode}
Preferences: ${preferences}
Top Places to Include (if fitting): ${places}
Popular Dining Spots (if fitting): ${dining}
Suggested Accommodation (if fitting): ${hotels}

OUTPUT FORMAT:
Provide a structured response:
1. Trip Overview (Total estimated cost, vibe, travel style based on preferences)
2. Transportation (How to reach ${destination} from ${source} via ${transportMode}, with estimated costs and duration)
3. Day-by-Day Itinerary (Morning, Afternoon, Evening for each day, focusing on ${preferences} activities)
4. Budget Breakdown (Transportation, Accommodation, Food, Activities, Miscellaneous)
5. Travel Tips (specific to ${transportMode} travel and ${preferences} experiences)

Do not use markdown formatting like bolding (**) or headers (##) excessively as this is a plain text stream, but you can use simple formatting like:
DAY 1: [Title]
- Morning: ...
`;
}