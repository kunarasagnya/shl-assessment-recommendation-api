# SHL Assessment Recommendation API

A FastAPI-based recommendation system that suggests relevant SHL assessments based on user queries such as job roles, skills, personality traits, and hiring requirements.

This project was developed as part of the SHL AI Research Intern assignment.

---

# Features

- Recommends relevant SHL assessments from the provided catalog
- Supports role-based queries
- Supports skill-based queries
- Supports personality and behavioral assessment queries
- Handles unknown or unsupported roles gracefully
- Returns clean JSON responses
- FastAPI Swagger documentation included
- Deployable on Render

---

# Tech Stack

- Python 3
- FastAPI
- Uvicorn
- JSON-based catalog retrieval
- Rule-based semantic matching

---

# Project Structure

```text
shl-project/
│
├── app/
│   ├── main.py
│   └── main_backup.py
│
├── data/
│   └── catalog.json
│
├── requirements.txt
├── README.md
└── venv/
```

---

# API Endpoints

## Health Check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

---

## Chat Recommendation Endpoint

```http
POST /chat
```

Request Format:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Need Python developer assessment"
    }
  ]
}
```

---

# Example Queries

## Python Developer

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Need Python developer assessment"
    }
  ]
}
```

---

## Data Scientist

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Looking for Data Scientist assessment"
    }
  ]
}
```

---

## Java Backend Developer

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Need Java backend developer test"
    }
  ]
}
```

---

## Personality Assessment

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Need leadership personality assessment"
    }
  ]
}
```

---

## Unknown Role

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Need astronaut assessment"
    }
  ]
}
```

---

# Response Format

```json
{
  "reply": "Here are suitable assessments for your query",
  "recommendations": [
    {
      "name": "Assessment Name",
      "url": "Assessment URL",
      "test_type": "Knowledge & Skills",
      "description": "Assessment description"
    }
  ],
  "end_of_conversation": true
}
```

---

# How Recommendation Logic Works

The recommendation system uses:

- Role keyword detection
- Skill keyword matching
- Personality keyword detection
- Scoring-based filtering
- Relevance ranking

The system avoids returning irrelevant assessments by:
- Matching role-specific keywords
- Prioritizing domain relevance
- Filtering unrelated personality-only assessments
- Handling unsupported roles separately

---

# Local Setup Instructions

## 1. Clone Repository

```bash
git clone https://github.com/kunarasagnya/shl-assessment-recommendation-api.git
```

---

## 2. Navigate to Project Folder

```bash
cd shl-assessment-recommendation-api
```

---

## 3. Create Virtual Environment

```bash
python -m venv venv
```

---

## 4. Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

## 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 6. Run Application

```bash
uvicorn app.main:app --reload
```

---

# Swagger Documentation

After running locally:

```text
http://127.0.0.1:8000/docs
```

---

# Live Deployment

## Render Deployment URL

```text
https://shl-assessment-recommendation-api.onrender.com
```

---

## Live Swagger Docs

```text
https://shl-assessment-recommendation-api.onrender.com/docs
```

---

# Deployment Details

The project is deployed using Render.

## Build Command

```bash
pip install -r requirements.txt
```

## Start Command

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

# Assumptions

- Recommendations are generated only from the provided SHL catalog
- Unknown or unsupported roles return a graceful fallback response
- Matching is based on semantic keyword scoring
- The system prioritizes relevance over quantity

---

# Future Improvements

- Add embedding-based semantic search
- Integrate vector databases
- Add LLM-based query understanding
- Add fuzzy matching
- Improve ranking using NLP similarity

---

# Author

Kuna Rasagnya

Developed for SHL AI Research Intern Assignment.