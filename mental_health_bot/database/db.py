from .models import db, Resource

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        # Seed initial resources if empty
        if not Resource.query.first():
            seed_resources()

def seed_resources():
    resources = [
        # Crisis & Hotlines
        Resource(title="International Suicide Hotlines", url="https://www.suicidestop.com/call_a_hotline.html", category="suicide", sentiment_tag="negative"),
        Resource(title="Crisis Text Line (Text HOME to 741741)", url="https://www.crisistextline.org/", category="suicide", sentiment_tag="negative"),
        
        # General Mental Health
        Resource(title="NIMH - Mental Health Information", url="https://www.nimh.nih.gov/health/topics", category="general", sentiment_tag="neutral"),
        Resource(title="MentalHealth.gov", url="https://www.mentalhealth.gov/", category="general", sentiment_tag="neutral"),
        
        # Anxiety & Stress
        Resource(title="ADAA - Anxiety and Depression Association", url="https://adaa.org/", category="anxiety", sentiment_tag="negative"),
        Resource(title="Box Breathing Technique (Video)", url="https://www.youtube.com/watch?v=tEmt1Znux58", category="anxiety", sentiment_tag="neutral"),
        Resource(title="Tips for Managing Stress", url="https://www.webmd.com/balance/stress-management/stress-management", category="stress", sentiment_tag="negative"),

        # Depression
        Resource(title="Depression Support - 7 Cups", url="https://www.7cups.com/", category="depression", sentiment_tag="negative"),
        Resource(title="Understanding Depression", url="https://www.mayoclinic.org/diseases-conditions/depression/symptoms-causes/syc-20356007", category="depression", sentiment_tag="negative"),

        # Relaxation & Sleep
        Resource(title="Guided Sleep Meditation", url="https://www.youtube.com/watch?v=aEqlQvczMJQ", category="insomnia", sentiment_tag="neutral"),
        Resource(title="Calming Nature Sounds", url="https://www.youtube.com/watch?v=eKFTSSKCzWA", category="relaxation", sentiment_tag="positive"),
        
        # Motivation
        Resource(title="TED Talk: The Power of Vulnerability", url="https://www.ted.com/talks/brene_brown_the_power_of_vulnerability", category="motivation", sentiment_tag="positive"),
        Resource(title="How to Build Self-Esteem", url="https://www.mind.org.uk/information-support/types-of-mental-health-problems/self-esteem/about-self-esteem/", category="self_esteem", sentiment_tag="neutral"),
    ]
    db.session.bulk_save_objects(resources)
    db.session.commit()
