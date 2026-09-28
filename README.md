# PocketSmart AI - Your Smart Budget & Recommendation Assistant

## Overview
PocketSmart AI is a GenAI-powered, cross-platform recommendation system that delivers personalized, budget-based suggestions for products and services. Built with **FastAPI** and **Google Gemini 1.5 Flash Pro**, it helps users plan home interiors, parties, and jewelry shopping—all within their defined budgets.

## Features
- **🏠 Home Interior Planner**: Get furniture and decor recommendations based on room type, budget, and quantities
- **🎉 Party Budget Planner**: Plan events with catering, decoration, and entertainment suggestions
- **💎 Jewelry Recommendations**: Get style-matched jewelry suggestions for any occasion
- **🔐 User Authentication**: Register, login, and manage personalized recommendations
- **📜 History**: View past recommendation queries and results

## Quick Start

### Prerequisites
- Python 3.12+
- Google Gemini API Key (from [console.cloud.google.com](https://console.cloud.google.com))

### Installation
```bash
pip install -r requirements.txt
```

### Setup
1. Get your Gemini API Key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Edit `.env` file and replace `YOUR_GEMINI_API_KEY_HERE` with your actual key
3. Run the server:
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Access the App
- **Home**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Home Planner**: http://localhost:8000/home-planner
- **Party Planner**: http://localhost:8000/party-planner
- **Jewelry Planner**: http://localhost:8000/jewelry-planner

## Architecture
- **Backend**: FastAPI with modular routers (auth, home, party, jewelry, recommendations)
- **AI Engine**: Gemini 1.5 Flash Pro for multimodal recommendations
- **Database**: SQLite with SQLAlchemy (users, sessions, recommendation history)
- **Frontend**: HTML/CSS/JS with Jinja2 templates

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/register | Create new account |
| POST | /auth/login | Login and get token |
| POST | /home/generate-home | Get home recommendations |
| POST | /party/generate-party | Get party recommendations |
| POST | /jewelry/generate-jewelry | Get jewelry recommendations |
| GET | /recommendations/history | View recommendation history |
| GET | / | Home page |
| GET | /dashboard | User dashboard |

## Project Structure
```
PocketSmartAI/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Application configuration
│   ├── database.py          # Database setup
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication utilities
│   ├── gemini_utils.py      # Gemini AI integration
│   ├── routers/             # API routers
│   │   ├── auth.py
│   │   ├── home.py
│   │   ├── party.py
│   │   ├── jewelry.py
│   │   └── recommendations.py
│   ├── services/
│   │   └── recommendation_service.py
│   └── templates/           # HTML templates
├── static/
│   ├── css/style.css        # Stylesheet
│   └── js/main.js           # Frontend JavaScript
├── .env                     # Environment variables
└── requirements.txt         # Python dependencies
```

## Technologies Used
- **FastAPI** - Modern Python web framework
- **Gemini 1.5 Flash Pro** - Google's multimodal AI model
- **SQLAlchemy** - Database ORM
- **Jinja2** - Template engine
- **python-jose** - JWT authentication
- **passlib** - Password hashing
- **HTML/CSS/JavaScript** - Frontend

## License
MIT License
