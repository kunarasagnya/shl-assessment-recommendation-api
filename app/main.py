from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from pathlib import Path
import json

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

    conversation_text = " ".join(
        [m.content.lower() for m in request.messages]
    )

    latest_message = request.messages[-1].content.lower()

    # catalog path
    catalog_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "catalog.json"
    )

    with open(catalog_path, "r", encoding="utf-8") as file:
        catalog = json.load(file)

    # vague queries
    vague_queries = [
        "assessment",
        "test",
        "need assessment",
        "need test"
    ]

    if latest_message.strip() in vague_queries:

        return {
            "reply": "What role are you hiring for?",
            "recommendations": [],
            "end_of_conversation": False
        }

    # OPQ vs GSA
    if (
        "difference" in conversation_text
        and "opq" in conversation_text
        and "gsa" in conversation_text
    ):

        return {
            "reply": (
                "OPQ focuses on personality and workplace behavior, "
                "while GSA focuses on skills and development areas."
            ),
            "recommendations": [],
            "end_of_conversation": True
        }

    matched_assessments = []
    seen_links = set()

    personality_required = (
        "personality" in conversation_text
        or "behavior" in conversation_text
    )

    # role keywords
    role_map = {
        "python": [
            "python",
            "django",
            "flask",
            "fastapi"
        ],

        "java": [
            "java",
            "spring",
            "hibernate"
        ],

        "data_science": [
            "data science",
            "data scientist",
            "machine learning",
            "ml",
            "ai",
            "analytics"
        ],

        "sql": [
            "sql",
            "database"
        ],

        "cloud": [
            "aws",
            "docker",
            "kubernetes",
            "cloud"
        ],

        "frontend": [
            "angular",
            "react",
            "frontend",
            "javascript"
        ],

        "finance": [
            "finance",
            "financial",
            "accounting"
        ],

        "excel_word": [
            "excel",
            "word",
            "admin assistant"
        ],

        "sales": [
            "sales",
            "sales manager"
        ],

        "leadership": [
            "leadership",
            "director",
            "executive",
            "cxo"
        ]
    }

    detected_roles = []

    for role, keywords in role_map.items():

        if any(
            keyword in conversation_text
            for keyword in keywords
        ):
            detected_roles.append(role)

    # if no known role found
    if len(detected_roles) == 0:

        return {
            "reply": (
                "I could not find a matching assessment "
                "category for this role in the SHL catalog."
            ),
            "recommendations": [],
            "end_of_conversation": True
        }

    # irrelevant assessments
    irrelevant_keywords = [
        "photoshop",
        "retail",
        "call center",
        "contact center",
        "customer service",
        "aerospace",
        "safety",
        "industrial"
    ]

    scored_results = []

    for assessment in catalog:

        name = assessment.get("name", "").lower()

        description = assessment.get(
            "description",
            ""
        ).lower()

        keys = " ".join(
            assessment.get("keys", [])
        ).lower()

        link = assessment.get(
            "link",
            assessment.get("url", "")
        )

        combined = f"{name} {description} {keys}"

        # remove irrelevant matches
        if any(
            bad in combined
            for bad in irrelevant_keywords
        ):
            continue

        score = 0

        # Python roles
        if "python" in detected_roles:

        # exact python assessment
            if "python" in name:
                score += 10

            python_keywords = [
                "python",
                "programming",
                "coding",
                "software",
                "developer",
                "automata",
                "backend"
            ]

            keyword_matches = 0

            for word in python_keywords:

                if word in combined:
                    keyword_matches += 1
                    

            score += keyword_matches * 2
        # Java roles
        if "java" in detected_roles:

            java_keywords = [
                "java",
                "spring",
                "rest",
                "backend",
                "sql"
            ]

            if any(
                word in combined
                for word in java_keywords
            ):
                score += 6

        # Data science
        if "data_science" in detected_roles:

            ds_keywords = [
                "data science",
                "statistics",
                "analytics",
                "machine learning",
                "ai",
                "sql",
                "python"
            ]

            if any(
                word in combined
                for word in ds_keywords
            ):
                score += 6

        # SQL
        if "sql" in detected_roles:

            if "sql" in combined:
                score += 5

        # Cloud
        if "cloud" in detected_roles:

            cloud_keywords = [
                "aws",
                "docker",
                "cloud",
                "kubernetes"
            ]

            if any(
                word in combined
                for word in cloud_keywords
            ):
                score += 5

        # Frontend
        if "frontend" in detected_roles:

            frontend_keywords = [
                "angular",
                "react",
                "javascript"
            ]

            if any(
                word in combined
                for word in frontend_keywords
            ):
                score += 5

        # Finance
        if "finance" in detected_roles:

            finance_keywords = [
                "finance",
                "financial",
                "accounting",
                "statistics"
            ]

            if any(
                word in combined
                for word in finance_keywords
            ):
                score += 5

        # Excel / Word
        if "excel_word" in detected_roles:

            office_keywords = [
                "excel",
                "word",
                "microsoft"
            ]

            if any(
                word in combined
                for word in office_keywords
            ):
                score += 5

        # Sales
        if "sales" in detected_roles:

            sales_keywords = [
                "sales",
                "customer",
                "transformation"
            ]

            if any(
                word in combined
                for word in sales_keywords
            ):
                score += 5

        # Leadership
        if "leadership" in detected_roles:

            leadership_keywords = [
                "leadership",
                "opq",
                "executive",
                "manager"
            ]

            if any(
                word in combined
                for word in leadership_keywords
            ):
                score += 6

        # prioritize technical assessments
        if (
            "knowledge & skills" in keys
            or "simulations" in keys
        ):
            score += 3

        # personality requested
        if personality_required:

            if "personality & behavior" in keys:
                score += 4

        else:

            # reduce personality-only priority
            if (
                "personality & behavior" in keys
                and "knowledge & skills" not in keys
                and "simulations" not in keys
            ):
                score -= 3

        if score > 0:

            scored_results.append(
                (score, assessment)
            )

    # sort by best score
    scored_results.sort(
        key=lambda x: x[0],
        reverse=True
    )

    # top recommendations
    for score, assessment in scored_results:

        link = assessment.get(
            "link",
            assessment.get("url", "")
        )

        if link not in seen_links:

            matched_assessments.append(
                assessment
            )

            seen_links.add(link)

        if len(matched_assessments) >= 10:
            break

    # no relevant assessments
    if not matched_assessments:

        return {
            "reply": (
                "No relevant assessments were found "
                "for this role in the SHL catalog."
            ),
            "recommendations": [],
            "end_of_conversation": True
        }

    return {
        "reply": (
            f"Here are suitable assessments for: "
            f"{request.messages[-1].content}"
        ),
        "recommendations": matched_assessments,
        "end_of_conversation": True
    }