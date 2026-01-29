# ✈️ TripSync - AI-Powered Trip Planner

<p align="center">
  <img src="static/images/logo.png" alt="TripSync Logo" width="120">
</p>

An intelligent trip planning application that combines **Large Language Models (LLM)**, **Machine Learning (ML)**, and **Retrieval-Augmented Generation (RAG)** to create personalized travel itineraries.

## 🚀 Quick Start

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env  # Add your API keys

# Run the application
python app.py
```

**Access:** http://localhost:5000

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **LLM Itinerary Generation** | Groq API with llama-3.3-70b-versatile |
| 🔍 **RAG Pipeline** | Context-aware responses with vector similarity search |
| 📊 **ML Recommendations** | TF-IDF content filtering + KMeans clustering |
| 🗺️ **Interactive Maps** | Mappls SDK with route visualization |
| 📍 **Places API** | Real-time attractions via Geoapify |
| 💰 **Budget Planning** | Smart budget distribution across categories |
| 🍽️ **Dining Suggestions** | Restaurant recommendations via Overpass API |

## 🧠 AI/ML Technologies

### 1. Large Language Model (LLM)
- **Provider:** Groq API
- **Model:** `llama-3.3-70b-versatile`
- **Purpose:** Generate detailed day-by-day itineraries

### 2. Retrieval-Augmented Generation (RAG)
- **Embeddings:** OpenRouter API (`text-embedding-3-small`)
- **Vector Store:** Custom implementation with cosine similarity
- **Knowledge Base:** Travel safety, seasons, temple rules

### 3. Machine Learning
- **TF-IDF Vectorizer:** Content-based place recommendations
- **KMeans Clustering:** Geographical grouping for day allocation
- **Haversine Distance:** Proximity-based scoring

## 📋 Configuration

Create a `.env` file with your API keys:

```env
# Required
GROQ_API_KEY=your_groq_key
GEOAPIFY_API_KEY=your_geoapify_key

# Optional - Enhanced Features
OPENAI_API_KEY=your_openrouter_key        # For RAG embeddings
MAPPLS_CLIENT_ID=your_mappls_id           # For maps
MAPPLS_CLIENT_SECRET=your_mappls_secret
GOOGLE_PLACES_API_KEY=your_google_key     # For place images
```

## 📂 Project Structure

```
TripSync/
├── app.py                      # Flask application
├── requirements.txt            # Python dependencies
│
├── services/                   # Backend services
│   ├── llm_service.py          # Groq LLM integration
│   ├── prompt_builder.py       # Prompt construction
│   ├── places_service.py       # Places API
│   ├── mappls_service.py       # Maps & routing
│   ├── image_service.py        # Place images
│   ├── local_db_service.py     # Local caching
│   │
│   └── rag/                    # RAG pipeline
│       ├── loader.py           # Document loading
│       ├── vector_store.py     # Embeddings & search
│       └── query_rag.py        # Query interface
│
├── ml_engine/                  # ML components
│   ├── recommender.py          # TF-IDF recommender
│   └── clustering.py           # KMeans clustering
│
├── templates/                  # Jinja2 templates
│   ├── index.html              # Main page
│   └── itinerary-display.html  # Results view
│
├── static/                     # Static assets
│   ├── css/styles.css
│   └── js/app.js
│
└── data/                       # Datasets
    ├── raw/                    # Source data
    └── processed/              # Cached database
```

## 🛠️ Technology Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.x, Flask |
| **LLM** | Groq API (llama-3.3-70b) |
| **ML** | scikit-learn (TF-IDF, KMeans) |
| **RAG** | Custom vector store + OpenRouter embeddings |
| **Maps** | Mappls SDK |
| **Geocoding** | Geoapify, Nominatim |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Templates** | Jinja2 |

## 🧪 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main trip planning form |
| `/api/plan-trip` | POST | Generate itinerary |
| `/api/map-data` | POST | Get route & places |
| `/api/place-images` | POST | Fetch place images |

### Example Request

```bash
curl -X POST http://localhost:5000/api/plan-trip \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Goa",
    "source": "Mumbai",
    "budget": "25000",
    "people": 2,
    "days": 3,
    "transport": "car",
    "preferences": ["beach", "adventure"]
  }'
```

## 📊 System Architecture

```
User Input → Flask API → Context Gathering → RAG Query
                              ↓
                    ML Recommendations (TF-IDF)
                              ↓
                    Prompt Builder + Context
                              ↓
                    Groq LLM (llama-3.3-70b)
                              ↓
                    JSON Itinerary Response
                              ↓
                    KMeans Day Allocation
                              ↓
                    Frontend Display + Map
```

## 🔐 API Rate Limits

| API | Free Tier |
|-----|-----------|
| Groq | 30 req/min |
| Geoapify | 250k/month |
| Mappls | 1M/month |
| OpenRouter | Pay-per-use |

## 📝 License

MIT License

## 👨‍💻 Author

**TripSync AI Development Team**

---

<p align="center">
  Built with ❤️ using Python, Flask, and AI
</p>
