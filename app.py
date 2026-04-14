from flask import Flask, request, jsonify, render_template, session
import re

app = Flask(__name__)
app.secret_key = "amenify_super_secret_key" # Required for session history

# 1. Load Data
def load_knowledge_base():
    try:
        with open("data.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return ["Amenify provides services for apartment residents."]

KNOWLEDGE_BASE = load_knowledge_base()

# Hardcoded stopwords to avoid NLTK dependency issues in deployment
STOPWORDS = {"is", "am", "are", "a", "an", "the", "in", "on", "at", "to", "for", "of", "and", "or", "what", "how", "does", "do", "tell", "me", "about"}
MANDATORY_KEYWORDS = {"amenify", "service", "services", "cleaning", "booking", "pricing", "platform", "app", "chores", "technology"}

def process_text(text):
    # Lowercase and extract words
    words = re.findall(r'\b\w+\b', text.lower())
    # Remove stopwords
    return set([w for w in words if w not in STOPWORDS])

def get_answer(user_query):
    query_tokens = process_text(user_query)
    
    # EDGE CASE: Empty input
    if not query_tokens:
        return "Please ask a question."

    # KEYWORD FILTER (IPL Problem Fix)
    if not query_tokens.intersection(MANDATORY_KEYWORDS):
        return "I don't know."

    best_match = "I don't know."
    highest_score = 0.0

    # MATCHING LOGIC
    for chunk in KNOWLEDGE_BASE:
        chunk_tokens = process_text(chunk)
        
        # Count matching words
        intersection = query_tokens.intersection(chunk_tokens)
        
        # Calculate Score based on query length
        score = len(intersection) / len(query_tokens)

        if score > highest_score:
            highest_score = score
            best_match = chunk

    # THRESHOLD CHECK (40% match required)
    if highest_score >= 0.40:
        return best_match
    else:
        return "I don't know."

@app.route("/")
def home():
    # Clear history on page reload for fresh start
    session['history'] = []
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    # Initialize history if not exists
    if 'history' not in session:
        session['history'] = []

    # Get bot reply
    bot_reply = get_answer(user_message)

    # Update history
    session['history'].append({"user": user_message, "bot": bot_reply})
    session.modified = True

    return jsonify({
        "reply": bot_reply,
        "history": session['history']
    })

if __name__ == "__main__":
    app.run(debug=True)