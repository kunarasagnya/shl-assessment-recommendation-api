from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):

    import json

    conversation_text = " ".join(
        [message.content.lower() for message in request.messages]
    )

    with open("data/catalog.json", "r") as file:
        catalog = json.load(file)

    vague_words = [
        "assessment",
        "test",
        "need assessment",
        "need test"
    ]

    if conversation_text in vague_words:

        return {
            "reply": "What role are you hiring for?",
            "recommendations": [],
            "end_of_conversation": False
        }

    matched_assessments = []

    for assessment in catalog:

        description = assessment["description"].lower()
        name = assessment["name"].lower()

        if "java" in conversation_text:
            if "java" in description:
                matched_assessments.append(assessment)

        if "python" in conversation_text:
            if "python" in description:
                matched_assessments.append(assessment)

        if "personality" in conversation_text:
            if "personality" in description or "opq" in name:
                matched_assessments.append(assessment)

    return {
        "reply": f"Here are suitable assessments for: {conversation_text}",
        "recommendations": matched_assessments,
        "end_of_conversation": False
    }