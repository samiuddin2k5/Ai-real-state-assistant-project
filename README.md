# AI Real Estate Assistant - Full Stack RAG Project

An intelligent real estate platform powered by AI and RAG (Retrieval-Augmented Generation) technology. This platform enables users to search properties, chat with AI assistants, get investment recommendations, and receive personalized insights.

## 🚀 Features

### 1. **AI Property Recommendation**
- Natural language property search
- Smart filtering based on user preferences
- Personalized recommendations based on budget and requirements

### 2. **RAG Property Chatbot**
- Intelligent answers about property details
- Investment advice and analysis
- Information about nearby facilities
- Legal guidance and area comparisons

### 3. **Smart Property Search**
- NLP-powered query understanding
- Advanced filtering by location, price, amenities
- Real-time property recommendations

### 4. **Investment Analysis AI**
- ROI calculations
- Rental income projections
- Risk assessment

### 5. **WhatsApp Integration**
- Property alerts via WhatsApp
- Lead notifications
- Direct agent communication

## 💻 Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | React + Vite + Tailwind |
| Backend | FastAPI |
| Database | PostgreSQL |
| AI/LLM | OpenAI API |
| RAG | LangChain + ChromaDB |
| Maps | Google Maps API |
| Auth | JWT |
| Deployment | Vercel + Render |

## 📁 Project Structure

```
Ai-real-state-assistant-project/
├── frontend/
├── backend/
├── database/
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## 🔧 Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📚 API Endpoints

- `GET /api/properties` - Get all properties
- `POST /api/chat` - Chat with AI
- `POST /api/search/smart` - AI-powered search
- `POST /api/investment/roi` - Calculate ROI
- `POST /api/auth/register` - Register user

---

**Building with ❤️ using AI**
