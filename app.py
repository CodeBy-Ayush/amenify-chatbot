from flask import Flask, request, jsonify, render_template, session
import re

app = Flask(__name__)
app.secret_key = "amenify_super_secret_key" 

def load_knowledge_base():
    try:
        with open("data.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return ["Amenify provides services for apartment residents."]

KNOWLEDGE_BASE = load_knowledge_base()

STOPWORDS = {"is", "am", "are", "a", "an", "the", "in", "on", "at", "to", "for", "of", "and", "or", "what", "how", "does", "do", "tell", "me", "about"}
MANDATORY_KEYWORDS = {"amenify", "service", "services", "cleaning", "booking", "pricing", "platform", "app", "chores", "technology"}

def process_text(text):
    words = re.findall(r'\b\w+\b', text.lower())
    # Remove stopwords
    return set([w for w in words if w not in STOPWORDS])

def get_answer(user_query):
    query_tokens = process_text(user_query)
    
    if not query_tokens:
        return "Please ask a question."

    if not query_tokens.intersection(MANDATORY_KEYWORDS):
        return "I don't know."

    best_match = "I don't know."
    highest_score = 0.0

    for chunk in KNOWLEDGE_BASE:
        chunk_tokens = process_text(chunk)
        
        intersection = query_tokens.intersection(chunk_tokens)
        
        score = len(intersection) / len(query_tokens)

        if score > highest_score:
            highest_score = score
            best_match = chunk

    if highest_score >= 0.40:
        return best_match
    else:
        return "I don't know."

@app.route("/")
def home():
    session['history'] = []
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if 'history' not in session:
        session['history'] = []

    bot_reply = get_answer(user_message)

    session['history'].append({"user": user_message, "bot": bot_reply})
    session.modified = True

    return jsonify({
        "reply": bot_reply,
        "history": session['history']
    })

if __name__ == "__main__":
    app.run(debug=True)