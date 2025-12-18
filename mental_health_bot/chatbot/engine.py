import json
import random
import pickle
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity

class ChatbotEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.X_train = None 
        self.y_train = []
        self.intents = []
        self.context = {} # Store context per user: {'user_id': {'history': [], 'entities': {}}}
        self.load_data()
        self.train()

    def load_data(self):
        file_path = os.path.join(os.path.dirname(__file__), 'intents.json')
        with open(file_path, 'r') as f:
            data = json.load(f)
        self.intents = data['intents']
        
        psych_path = os.path.join(os.path.dirname(__file__), 'psych_data.json')
        if os.path.exists(psych_path):
            with open(psych_path, 'r') as f:
                self.psych_data = json.load(f)
        else:
            self.psych_data = {}

    def train(self):
        corpus = []
        self.y_train = []
        for intent in self.intents:
            for pattern in intent['patterns']:
                corpus.append(pattern)
                self.y_train.append(intent['tag'])
        self.X_train = self.vectorizer.fit_transform(corpus)
        print("Bot trained successfully.")

    def extract_entities(self, text):
        entities = {}
        # Simple Regex for attributes
        import re
        name_match = re.search(r"\b(name is|call me|I am) (\w+)", text, re.IGNORECASE)
        if name_match:
            entities['name'] = name_match.group(2)
            
        age_match = re.search(r"\b(I am|turn) (\d+) (years old|years)", text, re.IGNORECASE)
        if age_match:
            entities['age'] = age_match.group(2)
            
        return entities

    def predict_intent(self, text, user_id='default'):
        # 0. Safety Override
        crisis_keywords = ["suicide", "kill myself", "want to die", "end it all", "hurt myself", "cutting", "overdose"]
        for keyword in crisis_keywords:
            if keyword in text.lower():
                return "suicide"

        # 1. Entity Extraction
        new_entities = self.extract_entities(text)
        if user_id not in self.context:
            self.context[user_id] = {'entities': {}, 'history': []}
        self.context[user_id]['entities'].update(new_entities)

        # 2. Transform & Similarity
        X_test = self.vectorizer.transform([text])
        similarities = cosine_similarity(X_test, self.X_train)
        best_match_index = np.argmax(similarities)
        best_score = similarities[0][best_match_index]
        print(f"Input: '{text}', Score: {best_score}")

        # 3. Contextual Adjustment
        # If user says "yes" or "no", check last intent
        if best_score < 0.5 and len(text.split()) < 3:
            last_intent = self.context[user_id].get('last_intent')
            if last_intent == 'sad' and text.lower() in ['yes', 'yeah']:
                 return 'depression_info' # Example flow

        if best_score > 0.35: 
             return self.y_train[best_match_index]
        
        # 4. Fallback Keyword Match
        text_lower = text.lower()
        for intent in self.intents:
            for pattern in intent['patterns']:
                 if pattern.lower() in text_lower:
                     return intent['tag']
        
        return "unknown"

    def get_response(self, intent_tag, user_input=None, user_id='default'):
        self.context[user_id]['last_intent'] = intent_tag
        
        # Personalization
        name = self.context[user_id]['entities'].get('name')
        
        # Check Psychological Data (same logic as before, preserved)
        if user_input and self.psych_data:
             lower_input = user_input.lower()
             if "grounding" in lower_input or "calm down" in lower_input:
                 tech = random.choice(self.psych_data.get('grounding_techniques', []))
                 steps = "\n".join(tech['steps'])
                 return f"Let's try the {tech['name']}:\n{steps}"

        # Get Response from Intents
        for intent in self.intents:
            if intent['tag'] == intent_tag:
                response = random.choice(intent['responses'])
                # Personalize response
                if "{name}" in response:
                    name = self.context.get(user_id, {}).get('entities', {}).get('name', '')
                    if name:
                        response = response.replace("{name}", name)
                    else:
                        response = response.replace("{name}", "friend")
                        
                # Architecture Requirement: Emotion-based Video Recommendations
                video_recommendations = {
                    'anxious': " <br><br>📺 <b>Recommended:</b> <a href='https://www.youtube.com/watch?v=O-6f5wQXSu8' target='_blank'>10-Minute Meditation for Anxiety</a>",
                    'sad': " <br><br>📺 <b>Recommended:</b> <a href='https://www.youtube.com/watch?v=-e_3Cg9GZFU' target='_blank'>Coping with Sadness (Therapist's Tips)</a>",
                    'stressed': " <br><br>📺 <b>Recommended:</b> <a href='https://www.youtube.com/watch?v=hnpQrMqDoqE' target='_blank'>Stress Relief Breathing</a>",
                    'depressed': " <br><br>📺 <b>Recommended:</b> <a href='https://www.youtube.com/watch?v=8Su5VtKeXU8' target='_blank'>Understanding Depression & Healing</a>",
                    'insomnia': " <br><br>📺 <b>Recommended:</b> <a href='https://www.youtube.com/watch?v=aEqlQvczMJQ' target='_blank'>Deep Sleep Music</a>",
                    # Expanded Conditions
                    'panic_attack': " <br><br>🆘 <b>Immediate Help:</b> <a href='https://www.youtube.com/watch?v=9swp6n-K0_s' target='_blank'>Panic Attack SOS: Follow Along</a>",
                    'ptsd_info': " <br><br>📺 <b>Recommended:</b> <a href='https://www.youtube.com/watch?v=b2Hdyiy5Zyg' target='_blank'>Grounding Techniques for PTSD</a>",
                    'ocd_info': " <br><br>📺 <b>Recommended:</b> <a href='https://www.youtube.com/watch?v=ua9o-d7t5FU' target='_blank'>Detaching from Intrusive Thoughts</a>",
                    'bipolar_info': " <br><br>📺 <b>Recommended:</b> <a href='https://www.youtube.com/watch?v=f5YhFD7qCjQ' target='_blank'>Understanding Bipolar Disorder</a>",
                    'eating_disorder_info': " <br><br>📺 <b>Recommended:</b> <a href='https://www.youtube.com/watch?v=1zeAd95g5a0' target='_blank'>Eating Disorder Recovery Advice</a>",
                    'social_anxiety': " <br><br>📺 <b>Recommended:</b> <a href='https://www.youtube.com/watch?v=S6k6SOtpgqk' target='_blank'>Overcoming Social Anxiety</a>",
                    'adhd_info': " <br><br>📺 <b>Recommended:</b> <a href='https://www.youtube.com/watch?v=JiwZQNYlGQI' target='_blank'>How to Focus with ADHD</a>",
                    # Further Expansion
                    'anger': " <br><br>📺 <b>Recommended:</b> <a href='https://www.youtube.com/watch?v=BsVq5R_F6RA' target='_blank'>Anger Management Techniques</a>",
                    'grief': " <br><br>📺 <b>Recommended:</b> <a href='https://www.youtube.com/watch?v=gsYL4Pdn1VM' target='_blank'>Dealing with Grief & Loss</a>",
                    'self_esteem': " <br><br>📺 <b>Recommended:</b> <a href='https://www.youtube.com/watch?v=l_NYrWqUR40' target='_blank'>Building Self Esteem</a>",
                    'work_stress_burnout': " <br><br>📺 <b>Recommended:</b> <a href='https://www.youtube.com/watch?v=wzJ0PeEChFM' target='_blank'>Recovering from Burnout</a>",
                    'lgbtq_support': " <br><br>📺 <b>Recommended:</b> <a href='https://www.youtube.com/watch?v=d_2e7mYgJ_s' target='_blank'>It Gets Better: Support</a>",
                    'imposter_syndrome': " <br><br>📺 <b>Recommended:</b> <a href='https://www.youtube.com/watch?v=ZQUxL4Jm1Lo' target='_blank'>Overcoming Imposter Syndrome</a>",
                    'seasonal_depression': " <br><br>📺 <b>Recommended:</b> <a href='https://www.youtube.com/watch?v=Xqp_a1fR-L0' target='_blank'>Coping with Seasonal Depression</a>"
                }
                
                if intent_tag in video_recommendations:
                    response += video_recommendations[intent_tag]

                return response
            
        return "I'm still learning. Can you tell me more?"

chatbot = ChatbotEngine()
