from app import app
from database.db import db, Resource

def seed_resources():
    with app.app_context():
        # Force fresh start
        db.drop_all()
        db.create_all()
        
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
            ),
            Resource(
                title="NAMI: PTSD Info",
                url="https://www.nami.org/About-Mental-Illness/Mental-Health-Conditions/Posttraumatic-Stress-Disorder",
                category="ptsd",
                sentiment_tag="negative"
            ),
            Resource(
                title="IOCDF: What is OCD?",
                url="https://iocdf.org/about-ocd/",
                category="ocd",
                sentiment_tag="negative"
            ),
            Resource(
                title="CHADD: ADHD Support",
                url="https://chadd.org/",
                category="adhd",
                sentiment_tag="negative"
            ),
            Resource(
                title="NEDA: Eating Disorder Help",
                url="https://www.nationaleatingdisorders.org/",
                category="eating_disorder",
                sentiment_tag="negative"
            ),
            Resource(
                title="AA: Alcoholics Anonymous",
                url="https://www.aa.org/",
                category="addiction",
                sentiment_tag="negative"
            ),
            Resource(
                title="Mindfulness Exercises",
                url="https://www.mindful.org/mindfulness-exercises-for-beginners/",
                category="mindfulness",
                sentiment_tag="positive"
            )
        ]
        
        db.session.bulk_save_objects(resources)
        db.session.commit()
        print("Database seeded with Augmented Data resources.")

if __name__ == "__main__":
    seed_resources()
