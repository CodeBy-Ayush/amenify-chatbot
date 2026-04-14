# Amenify Customer Support Bot

## 🚀 Overview

This project is a **Strict Retrieval-Based Customer Support Chatbot** built for Amenify.

Unlike generative AI models, this chatbot **does not generate answers**. Instead, it retrieves responses strictly from a predefined knowledge base (`data.txt`).

If a query is unrelated or no relevant match is found, the bot safely responds with:

> **"I don't know"**

This ensures **high accuracy and zero hallucination**.

---

## 🎯 Key Features

* ✅ Retrieval-based architecture (no hallucination)
* ✅ Keyword-based matching with scoring
* ✅ Threshold filtering (40% match required)
* ✅ Strict domain control (Amenify-related queries only)
* ✅ Session-based chat history
* ✅ Clean and modern UI (sky-blue theme)
* ✅ Typing indicator for better UX
* ✅ Sidebar chat history panel

---

## 🏗️ Project Structure

```
amenify-chatbot/
│
├── app.py              # Flask backend (core logic)
├── data.txt            # Knowledge base (structured chunks)
├── requirements.txt    # Dependencies
│
├── templates/
│   └── index.html      # UI layout
│
├── static/
│   ├── style.css       # Styling
│   └── script.js       # Frontend logic
│
└── README.md           # Documentation
```

---

## 🧠 How It Works (Core Logic)

### 1. Data Loading

* Reads `data.txt`
* Each line = one meaningful knowledge chunk

---

### 2. Query Processing

* Converts input to lowercase
* Removes stopwords (e.g., "what", "is", "the")

Example:

```
"What services does Amenify provide?"
→ ["services", "amenify", "provide"]
```

---

### 3. Keyword Filtering

* Ensures query contains relevant keywords like:

  * amenify
  * service
  * booking
  * platform

If not → returns:

```
"I don't know"
```

---

### 4. Matching Logic

* Compares query tokens with each chunk
* Calculates score:

```
score = matched_words / total_query_words
```

---

### 5. Threshold Decision

* If score ≥ 0.40 → return best match
* Else → return:

```
"I don't know"
```

---

## 🧪 Example Queries

| Query                      | Output         |
| -------------------------- | -------------- |
| What is Amenify?           | Correct answer |
| Who is CEO of Amenify?     | Everett Lynn   |
| What services are offered? | Correct answer |
| IPL match today?           | I don't know   |

---

## ⚠️ Hallucination Control

This system avoids hallucination by:

* ❌ Not generating answers
* ✅ Only retrieving from `data.txt`
* ✅ Using strict threshold filtering
* ✅ Returning "I don't know" for unknown queries

---

## ⚠️ Limitations

* Keyword-based matching (no deep semantic understanding)
* Limited to predefined knowledge base
* Cannot handle highly paraphrased or complex queries

---

## 🚀 Future Improvements

* Use embeddings / vector search (FAISS)
* Add fuzzy matching (Levenshtein distance)
* Expand knowledge base dynamically
* Improve UI with real-time updates

---

## 🛠️ Setup Instructions (Local)

### 1. Clone Repository

```
git clone <your-repo-link>
cd amenify-chatbot
```

---

### 2. Create Virtual Environment

```
python -m venv venv
```

---

### 3. Activate Environment

* Windows:

```
venv\Scripts\activate
```

* Mac/Linux:

```
source venv/bin/activate
```

---

### 4. Install Dependencies

```
pip install -r requirements.txt
```

---

### 5. Run Application

```
python app.py
```

---

### 6. Open in Browser

```
http://127.0.0.1:5000
```

---

## 🌐 Deployment (Render)

1. Push code to GitHub
2. Go to Render → New Web Service
3. Connect repo
4. Set:

Build Command:

```
pip install -r requirements.txt
```

Start Command:

```
gunicorn app:app
```

5. Deploy 🚀

---

## 📌 Design Decision

This chatbot is intentionally designed to:

* prioritize **accuracy over completeness**
* avoid **hallucinated responses**
* maintain a **controlled knowledge scope**

---

## 👨‍💻 Author

**Ayush Kumar**

* LinkedIn: https://www.linkedin.com/in/ayush111
* GitHub: https://github.com/CodeBy-Ayush

---

## 📌 Submission Notes

* The chatbot strictly answers from the Amenify knowledge base.
* Unrelated queries are handled safely with "I don't know".
* The system demonstrates strong control over hallucination and response accuracy.
