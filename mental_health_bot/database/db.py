from .models import db, Resource

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        # Seed initial resources if empty
        # Seed/Update initial resources
        seed_resources()

def seed_resources():
    # Define resources to seed
    resources_data = [
        # Crisis & Hotlines
        {"title": "International Suicide Hotlines", "url": "https://www.suicidestop.com/call_a_hotline.html", "category": "suicide", "sentiment_tag": "negative"},
        {"title": "Crisis Text Line (Text HOME to 741741)", "url": "https://www.crisistextline.org/", "category": "suicide", "sentiment_tag": "negative"},
        {"title": "Panic Attack SOS: Follow Along", "url": "https://www.youtube.com/watch?v=9swp6n-K0_s", "category": "panic_attack", "sentiment_tag": "negative"},

        # General Mental Health
        {"title": "NIMH - Mental Health Information", "url": "https://www.nimh.nih.gov/health/topics", "category": "general", "sentiment_tag": "neutral"},
        {"title": "MentalHealth.gov", "url": "https://www.mentalhealth.gov/", "category": "general", "sentiment_tag": "neutral"},
        
        # Anxiety & Stress
        {"title": "ADAA - Anxiety and Depression Association", "url": "https://adaa.org/", "category": "anxiety", "sentiment_tag": "negative"},
        {"title": "10-Minute Meditation for Anxiety", "url": "https://www.youtube.com/watch?v=O-6f5wQXSu8", "category": "anxiety", "sentiment_tag": "neutral"},
        {"title": "Stress Relief Breathing", "url": "https://www.youtube.com/watch?v=hnpQrMqDoqE", "category": "stress", "sentiment_tag": "negative"},
        {"title": "Overcoming Social Anxiety", "url": "https://www.youtube.com/watch?v=S6k6SOtpgqk", "category": "social_anxiety", "sentiment_tag": "negative"},

        # Depression & Sadness
        {"title": "Depression Support - 7 Cups", "url": "https://www.7cups.com/", "category": "depression", "sentiment_tag": "negative"},
        {"title": "Understanding Depression & Healing", "url": "https://www.youtube.com/watch?v=8Su5VtKeXU8", "category": "depression", "sentiment_tag": "negative"},
        {"title": "Coping with Sadness (Therapist's Tips)", "url": "https://www.youtube.com/watch?v=-e_3Cg9GZFU", "category": "sad", "sentiment_tag": "negative"},
        {"title": "Coping with Seasonal Depression", "url": "https://www.youtube.com/watch?v=Xqp_a1fR-L0", "category": "seasonal_depression", "sentiment_tag": "negative"},

        # Relaxation & Sleep
        {"title": "Deep Sleep Music", "url": "https://www.youtube.com/watch?v=aEqlQvczMJQ", "category": "insomnia", "sentiment_tag": "neutral"},
        {"title": "Calming Nature Sounds", "url": "https://www.youtube.com/watch?v=eKFTSSKCzWA", "category": "relaxation", "sentiment_tag": "positive"},
        
        # Specific Conditions
        {"title": "Grounding Techniques for PTSD", "url": "https://www.youtube.com/watch?v=b2Hdyiy5Zyg", "category": "ptsd_info", "sentiment_tag": "neutral"},
        {"title": "Detaching from Intrusive Thoughts (OCD)", "url": "https://www.youtube.com/watch?v=ua9o-d7t5FU", "category": "ocd_info", "sentiment_tag": "neutral"},
        {"title": "Understanding Bipolar Disorder", "url": "https://www.youtube.com/watch?v=f5YhFD7qCjQ", "category": "bipolar_info", "sentiment_tag": "neutral"},
        {"title": "Eating Disorder Recovery Advice", "url": "https://www.youtube.com/watch?v=1zeAd95g5a0", "category": "eating_disorder_info", "sentiment_tag": "neutral"},
        {"title": "How to Focus with ADHD", "url": "https://www.youtube.com/watch?v=JiwZQNYlGQI", "category": "adhd_info", "sentiment_tag": "neutral"},
        
        # Emotional Management
        {"title": "Anger Management Techniques", "url": "https://www.youtube.com/watch?v=BsVq5R_F6RA", "category": "anger", "sentiment_tag": "negative"},
        {"title": "Dealing with Grief & Loss", "url": "https://www.youtube.com/watch?v=gsYL4Pdn1VM", "category": "grief", "sentiment_tag": "negative"},
        {"title": "Building Self Esteem", "url": "https://www.youtube.com/watch?v=l_NYrWqUR40", "category": "self_esteem", "sentiment_tag": "neutral"},
        {"title": "Recovering from Burnout", "url": "https://www.youtube.com/watch?v=wzJ0PeEChFM", "category": "work_stress_burnout", "sentiment_tag": "negative"},
        {"title": "Overcoming Imposter Syndrome", "url": "https://www.youtube.com/watch?v=ZQUxL4Jm1Lo", "category": "imposter_syndrome", "sentiment_tag": "negative"},

        # Motivation & Support
        {"title": "TED Talk: The Power of Vulnerability", "url": "https://www.ted.com/talks/brene_brown_the_power_of_vulnerability", "category": "motivation", "sentiment_tag": "positive"},
        {"title": "It Gets Better: Support (LGBTQ)", "url": "https://www.youtube.com/watch?v=d_2e7mYgJ_s", "category": "lgbtq_support", "sentiment_tag": "neutral"},
    ]

    for r_data in resources_data:
        existing = Resource.query.filter_by(url=r_data['url']).first()
        if not existing:
            new_res = Resource(
                title=r_data['title'],
                url=r_data['url'],
                category=r_data['category'],
                sentiment_tag=r_data['sentiment_tag']
            )
            db.session.add(new_res)
    
    db.session.commit()
    print("Database resources updated.")
