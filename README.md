# 🔥 HabitForge

Un'app per il tracking delle abitudini con analisi automatica del linguaggio naturale.

## 🚀 Quick Start

```bash
# Avvia l'intera applicazione (database + backend + pgAdmin)
docker-compose up --build

# Accedi all'API documentation
http://localhost:8000/docs

# Accedi al database via pgAdmin (interfaccia web)
http://localhost:5050

# Testa l'endpoint
curl -X POST "http://localhost:8000/habits/analyze" \
     -H "Content-Type: application/json" \
     -d '{"text": "Voglio correre 5km tutti i giorni"}'
```

## 📊 Database Access

Il progetto include **pgAdmin** per gestire visivamente il database PostgreSQL:

- **URL**: http://localhost:5050
- **Login**: admin@habitforge.com
- **Password**: admin123

### Connessione al database in pgAdmin:
1. Vai su http://localhost:5050
2. Effettua il login con le credenziali sopra
3. Clicca su "Add New Server"
4. **Name**: HabitForge DB
5. **Host**: db
6. **Port**: 5432
7. **Database**: habitforge_db
8. **Username**: postgres
9. **Password**: postgres

## 🏗️ Architettura

```
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI endpoints
│   │   │   ├── models/   # Pydantic data models
│   │   │   └── server.py # Main FastAPI application
│   │   ├── db/           # Database access layer
│   │   └── NLM/          # Natural Language Processing
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env             # Configurazione database e pgAdmin
│   └── tests/           # Test suite
├── docker-compose.yml   # Orchestrazione completa (db + backend + pgAdmin)
└── README.md
```

## 🎯 Funzionalità

- **NLP Analysis**: Estrazione automatica di azione, quantità e frequenza da testo naturale
- **Database**: PostgreSQL con schema completo per abitudini e utenti
- **API**: FastAPI con documentazione automatica
- **Admin Interface**: pgAdmin per gestione database
- **Docker**: Setup completo con un solo comando

## 🧪 Esempio di Utilizzo

```json
POST /habits/analyze
{
  "text": "Bere 2 litri di acqua al giorno",
  "user_id": "user123"
}

Response:
{
  "status": "success",
  "analysis": {
    "action": "bere",
    "quantity": "2 litri",
    "frequency_count": 7,
    "frequency_period": 7,
    "language": "it"
  }
}
```

## 🛠️ Sviluppo

```bash
# Solo backend per sviluppo
cd backend
pip install -r requirements.txt
uvicorn app.api.server:app --reload

# Solo database + pgAdmin
docker-compose up db pgadmin

# Ricostruisci solo il backend
docker-compose up --build backend
```

## 📊 Database Schema

Il database include:
- **users**: Gestione utenti
- **habits**: Abitudini con analisi NLP
- **habit_entries**: Tracking giornaliero
- **social_groups**: Gruppi sociali
- **group_members**: Membri dei gruppi 🔥

### A smart, social habit tracker that leverages friendly competition to turn your goals into achievements.

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com) <!-- Placeholder -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Note:** This project is currently under active development.

---

## 🎯 The Vision

Standard habit trackers often fail because they are a solitary journey. It's easy to lose motivation when you're the only one holding yourself accountable.

**HabitForge** is built on a simple but powerful premise: **motivation is amplified by community.** It's a smart habit tracker designed to help you and your friends build routines and stick to them through healthy, friendly competition.

It's more than just a checklist; it's an intelligent coach that understands your goals and a social platform that makes self-improvement a shared, engaging, and rewarding experience.

<!-- Add a screenshot or GIF of the app in action here later -->
<!-- ![App Screenshot](link_to_your_screenshot.png) -->

## ✨ Key Features

*   **💬 Natural Language Habit Creation:** Just type your goal like you would say it (e.g., "Read 10 pages of a book every day"). Our NLP backend understands and sets it up for you.
*   **🏆 Real-Time Competitive Leaderboards:** Challenge your friends and see who is the most consistent. Leaderboards are updated in real-time using WebSockets, so you see every success as it happens.
*   **🤖 AI-Powered Consistency Coach:** Our smart agent learns your patterns and predicts when you're likely to miss a habit, sending you a timely, personalized motivational nudge.
*   **📊 Insightful Progress Visualization:** Track your journey with beautiful and intuitive visualizations, including consistency heatmaps and progress charts.
*   **🤝 Social Groups & Challenges:** Create private groups for specific goals (like a "Morning Run Club" or "Book Club") and launch time-boxed challenges to keep everyone engaged.
*   **🚀 Asynchronous Notification System:** A robust, non-blocking notification system ensures you and your friends get all important updates without slowing down the app.

## 🛠️ Tech Stack

The project uses a modern, scalable tech stack, perfect for a real-world application.

*   **Backend:**
    *   **Framework:** **FastAPI** (Python 3.11+)
    *   **Real-time Communication:** **WebSockets**
    *   **Asynchronous Tasks:** **Celery** & **Redis**
    *   **AI / NLP:** **spaCy** for Natural Language Processing, **Scikit-learn** for predictive modeling.
*   **Frontend:**
    *   **Framework:** **React** (with Vite)
    *   **State Management:** Redux Toolkit / Zustand (TBD)
    *   **Data Visualization:** **Recharts**
*   **Database:**
    *   **Primary:** **PostgreSQL**
*   **DevOps:**
    *   **Containerization:** **Docker** & **Docker Compose**

## 🚀 Getting Started

Instructions on how to set up and run the project locally.

### Prerequisites

*   Git
*   Python 3.11+
*   Node.js 18+ and npm/yarn
*   Docker and Docker Compose

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/habitforge.git
    cd habitforge
    ```

2.  **Setup the Backend:**
    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```
    *You will also need to create a `.env` file for your environment variables (database URL, API keys, etc.).*

3.  **Setup the Frontend:**
    ```bash
    cd ../frontend
    npm install
    ```

4.  **Run the application (with Docker):**
    The easiest way to get all services (backend, frontend, database, Redis) running is with Docker Compose.
    ```bash
    # From the root project directory
    docker-compose up --build
    ```
    The application will be available at `http://localhost:3000`.

## 🗺️ Project Roadmap

This is a living project. Future plans include:

*   [ ] More advanced AI-driven suggestions for new habits.
*   [ ] Integration with third-party apps (Google Calendar, Strava, etc.).
*   [ ] A fully-featured native mobile app (React Native or Flutter).
*   [ ] Gamification elements like badges and achievement streaks.

## 🤝 Contributing

Contributions are welcome! If you have suggestions or want to fix a bug, please open an issue to discuss it first.

## 📄 License

This project is licensed under the **MIT License**. See the `LICENSE` file for more details.
