Mental Health Chatbot & Companion
A comprehensive mental health support application featuring an AI-powered sentiment analysis chatbot, mood tracking, journaling, and resource recommendation system.

🌟 Features
AI Chatbot Companion: Interact with an intelligent bot that understands various mental health contexts (Anxiety, Depression, PTSD, OCD, etc.) using natural language understanding.
Sentiment Analysis: The bot analyzes your emotional state in real-time to provide empathetic responses.
Smart Resource Recommendations: automatically suggests relevant articles, helplines, and videos based on the conversation's context and detected sentiment.
Mood Journal & Dashboard: Track your daily mood scores, view trends over time, and maintain a personal journal.
Secure & Private: User authentication ensures your data and journal entries remain private.
🛠️ Tech Stack
Backend: Flask (Python)
Database: SQLAlchemy (SQLite for development / MySQL compatible)
AI/ML: Scikit-Learn, NLTK, TextBlob
Frontend: HTML5, CSS3, JavaScript (Bootstrap 5)
🚀 Installation
Clone the repository

git clone <repository-url>
cd mental_health_bot
Install Dependencies It is recommended to use a virtual environment.

pip install -r requirements.txt
Initialize Database Run the seed script to create the database tables and populate them with initial resources.

Warning: This will drop existing tables and data to ensure a fresh setup.

python seed_data.py
Run the Application

python app.py
Access the App Open your browser and navigate to: http://localhost:5000

📂 Project Structure
app.py: Main application entry point and route definitions.
chatbot/: Contains the NLU engine (engine.py), sentiment analysis (sentiment.py), and training data (psych_data.json).
database/: Database models and connection logic.
templates/: HTML templates for the user interface.
seed_data.py: Script to initialize the database with helper resources.
🤝 Usage
Register/Login: Create a new account to start tracking your journey.
Daily Check-in: Log your mood on the home page.
Chat: Use the chat interface to talk about your feelings or ask for advice.
Dashboard: Visit the dashboard to see your mood history and chat logs.
Journal: Write private entries to reflect on your day.
