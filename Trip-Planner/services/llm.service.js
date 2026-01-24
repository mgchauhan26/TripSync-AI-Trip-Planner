import axios from "axios";

export async function callLLM(prompt) {
  const response = await axios.post(
    "https://openrouter.ai/api/v1/chat/completions",
    {
      model: "gpt-4o-mini", // OpenRouter supports this model mapping usually, or we can use openai/gpt-4o-mini
      messages: [
        { role: "user", content: prompt }
      ],
      temperature: 0.7
    },
    {
      headers: {
        "Authorization": `Bearer ${process.env.OPENAI_API_KEY}`,
        "HTTP-Referer": "http://localhost:3000", // Required by OpenRouter
        "X-Title": "Trip Planner" // Optional
      }
    }
  );

  return response.data.choices[0].message.content;
}