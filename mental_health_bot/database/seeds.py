from app import app
from database.db import db, Resource

def seed_resources():
    with app.app_context():
        # Check if resources exist to avoid duplicates
        if Resource.query.first():
            print("Resources already seeded.")
            return

        resources = [
            Resource(
                title="Understanding Anxiety",
                url="https://www.nimh.nih.gov/health/topics/anxiety-disorders",
                category="anxiety",
                sentiment_tag="negative"
            ),
            Resource(
                title="Coping with Depression",
                url="https://www.helpguide.org/articles/depression/coping-with-depression.htm",
                category="depression",
                sentiment_tag="negative"
            ),
            Resource(
                title="Guided Meditation for Stress",
                url="https://www.youtube.com/watch?v=ssss7V1_eyA",
                category="stress",
                sentiment_tag="negative"
            ),
            Resource(
                title="Suicide Prevention",
                url="https://988lifeline.org/",
                category="crisis",
                sentiment_tag="negative"
            ),
            Resource(
                title="7 Ways to Boost Self-Esteem",
                url="https://www.psychologytoday.com/us/blog/nurturing-self-compassion/201703/8-steps-improving-your-self-esteem",
                category="motivation",
                sentiment_tag="positive"
            )
        ]
        
        db.session.bulk_save_objects(resources)
        db.session.commit()
        print("Database seeded with Augmented Data resources.")

if __name__ == "__main__":
    seed_resources()
