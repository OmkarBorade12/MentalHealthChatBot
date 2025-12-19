from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
import os
import json
from database.models import db, User, JournalEntry, ChatHistory, MoodEntry, Resource
from chatbot.engine import ChatbotEngine, chatbot
from chatbot.sentiment import analyze_sentiment
from datetime import date, datetime

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))

@app.route('/')
@login_required
def index():
    # Check if daily check-in is needed
    show_checkin = False
    if current_user.last_checkin_date != date.today():
        show_checkin = True
    return render_template('index.html', show_checkin=show_checkin)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        # Update Preferences
        if 'theme' in request.form:
            prefs = current_user.get_preferences()
            prefs['theme'] = request.form.get('theme')
            prefs['notifications'] = 'notifications' in request.form
            current_user.set_preferences(prefs)
            db.session.commit()
            flash('Preferences updated')
            
        # Change Password
        if 'new_password' in request.form and request.form['new_password']:
            current_user.set_password(request.form['new_password'])
            db.session.commit()
            flash('Password changed successfully')
            
    return render_template('settings.html', preferences=current_user.get_preferences())

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/api/chat', methods=['POST'])
@login_required
def chat():
    data = request.json
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    # 1. Analyze Sentiment
    sentiment = analyze_sentiment(user_message)
    
    # 2. Get Intent & Response
    # Inject context: recent mood
    user_context_id = str(current_user.id)
    
    # Simple context injection via prompt enrichment could be done here if engine supported it
    # For now, we rely on standard engine
    
    intent = chatbot.predict_intent(user_message, user_id=user_context_id)
    bot_response = chatbot.get_response(intent, user_input=user_message, user_id=user_context_id)
    
    # 3. Check for Resources
    resources = []
    
    # We want resources if:
    # 1. Sentiment is negative
    # 2. Intent matches a specific category (e.g. anxiety, ptsd_info)
    # 3. Intent implies need for help (stress, crisis)
    
    query_filters = []
    
    if sentiment == 'negative':
        query_filters.append(Resource.sentiment_tag == 'negative')
        
    # Always check if the current intent matches a resource category
    # This covers things like 'ptsd_info', 'anxiety', 'social_anxiety' etc.
    query_filters.append(Resource.category == intent)
    
    if query_filters:
        # Use 'OR' logic: show if matches intent OR matches negative sentiment
        from sqlalchemy import or_
        relevant_resources = Resource.query.filter(
            or_(*query_filters)
        ).limit(3).all()
        
        for res in relevant_resources:
            resources.append({'title': res.title, 'url': res.url})
            
    # 3. Save to Database (Architecture Requirement)
    try:
        # Save User Message
        user_msg = ChatHistory(user_id=current_user.id, role='user', content=user_message)
        db.session.add(user_msg)
        
        # Save Bot Message
        bot_msg = ChatHistory(user_id=current_user.id, role='bot', content=bot_response)
        db.session.add(bot_msg)
        
        db.session.commit()
    except Exception as e:
        print(f"Error saving chat history: {e}")
    
    return jsonify({
        'response': bot_response,
        'sentiment': sentiment,
        'resources': resources
    })

@app.route('/api/checkin', methods=['POST'])
@login_required
def checkin():
    data = request.json
    score = data.get('score')
    tag = data.get('tag')
    note = data.get('note', '')
    
    if score is None:
        return jsonify({'error': 'Score required'}), 400
        
    entry = MoodEntry(
        user=current_user,
        score=int(score),
        emotion_tag=tag,
        note=note
    )
    
    # Update Streak
    if current_user.last_checkin_date != date.today():
        # logic: if yesterday was checkin, inc streak, else reset 1
        # simpler: just inc for now to encourage usage
        current_user.streak_count += 1
        current_user.last_checkin_date = date.today()
        
    db.session.add(entry)
    db.session.commit()
    
    return jsonify({'success': True, 'streak': current_user.streak_count})

@app.route('/dashboard')
@login_required
def dashboard():
    # Chat History
    history = ChatHistory.query.filter_by(author=current_user).order_by(ChatHistory.timestamp.asc()).all()
    
    # Mood History
    moods = MoodEntry.query.filter_by(user=current_user).order_by(MoodEntry.timestamp.asc()).all()
    
    # Prepare Chat Data
    chat_dates = [c.timestamp.isoformat() + 'Z' for c in history]
    # chat_sentiments removed as model does not have this field
    
    # Prepare Mood Data
    mood_dates = [m.timestamp.isoformat() + 'Z' for m in moods]
    mood_scores = [m.score for m in moods]
    mood_tags = [m.emotion_tag for m in moods]
    
    return render_template('dashboard.html', 
                           chat_dates=chat_dates,
                           mood_dates=mood_dates, mood_scores=mood_scores, mood_tags=mood_tags,
                           streak=current_user.streak_count)

@app.route('/journal')
@login_required
def journal():
    entries = JournalEntry.query.filter_by(author=current_user).order_by(JournalEntry.timestamp.desc()).all()
    return render_template('journal.html', entries=entries)

@app.route('/journal/new', methods=['GET', 'POST'])
@login_required
def new_journal():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        entry = JournalEntry(author=current_user, title=title, content=content)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('journal'))
    return render_template('journal_edit.html', entry=None)

@app.route('/journal/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def view_journal(entry_id):
    entry = db.session.get(JournalEntry, entry_id)
    if not entry or entry.author != current_user:
        return redirect(url_for('journal'))
    
    if request.method == 'POST':
        entry.title = request.form.get('title')
        entry.content = request.form.get('content')
        db.session.commit()
        return redirect(url_for('journal'))
        
    return render_template('journal_edit.html', entry=entry)

@app.route('/journal/<int:entry_id>/delete', methods=['POST'])
@login_required
def delete_journal(entry_id):
    entry = db.session.get(JournalEntry, entry_id)
    if not entry or entry.author != current_user:
        return redirect(url_for('journal'))
    
    db.session.delete(entry)
    db.session.commit()
    flash('Journal entry deleted.')
    return redirect(url_for('journal'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        from database.db import seed_resources
        seed_resources()
    app.run(debug=True, host='0.0.0.0')
