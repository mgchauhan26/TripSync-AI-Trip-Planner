export function buildPrompt(user, context = {}) {
  const { destination, budget, budgetTier, people, days } = user;
  const places = context.places ? context.places.map(p => p.name).join(", ") : "Main attractions";
  const dining = context.dining ? context.dining.map(d => `${d.name} (${d.cuisine || 'Local'} - ${d.address || d.city || 'Nearby'})`).join(", ") : "Local food spots";
  const hotels = context.hotels ? context.hotels.map(h => `${h.name} (${h.type} - ${h.city || 'Nearby'})`).join(", ") : "Standard hotels";

  return `
SYSTEM:
You are a professional travel planner.
Create a detailed, day-by-day itinerary for a trip to ${destination}.
You must account for a TOTAL budget of ₹${budget} (${budgetTier} Budget) for ${people} people.
The itinerary should be practical, listing specific places to visit, estimated costs, and timing.
IMPORTANT: All costs must be in Indian Rupees (₹). Do not use USD ($).

USER:
Destination: ${destination}
Duration: ${days} days
Travelers: ${people} person(s)
Budget Limit: ₹${budget} (${budgetTier})
Top Places to Include (if fitting): ${places}
Popular Dining Spots (if fitting): ${dining}
Suggested Accommodation (if fitting): ${hotels}

OUTPUT FORMAT:
Provide a structured response:
1. Trip Overview (Total estimated cost, vibe)
2. Day-by-Day Itinerary (Morning, Afternoon, Evening for each day)
3. Budget Breakdown
4. Travel Tips

Do not use markdown formatting like bolding (**) or headers (##) excessively as this is a plain text stream, but you can use simple formatting like:
DAY 1: [Title]
- Morning: ...
`;
}