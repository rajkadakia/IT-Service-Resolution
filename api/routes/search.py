from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Literal

from backend.scripts.retriever import retrieve_context
from backend.scripts.llmgroq import generate_answer
from backend.scripts.clarifier import generate_clarifying_question

MAX_CLARIFICATION_TURNS = 2

router = APIRouter()



class SearchRequest(BaseModel):
    query: str


class ClarificationRequest(BaseModel):
    previous_query: str
    clarification_answer: str
    turn: int




class IncidentMatch(BaseModel):
    incident_id: str
    text: str


class AnswerResponse(BaseModel):
    type: Literal["answer"]
    answer: str
    context: List[IncidentMatch]


class ClarificationResponse(BaseModel):
    type: Literal["clarification"]
    question: str
    turn: int


SearchResponse = AnswerResponse | ClarificationResponse




def run_category_search(query: str, category: str):
    data = retrieve_context(query=query, category=category)

    confidence = data["confidence"]
    categories = data["categories"]
    results = data["results"]

    
    if confidence < 0.55 or len(categories) > 1:
        question = generate_clarifying_question(
            query=query,
            categories=categories
        )
        return {
            "type": "clarification",
            "question": question,
            "turn": 0
        }

    
    answer = generate_answer(query, results)

    return {
        "type": "answer",
        "answer": answer,
        "context": results
    }




def run_followup_search(
    previous_query: str,
    clarification_answer: str,
    turn: int,
    category: str
):
    combined_query = f"{previous_query}. {clarification_answer}"

    data = retrieve_context(query=combined_query, category=category)

    confidence = data["confidence"]
    categories = data["categories"]
    results = data["results"]

    
    if turn >= MAX_CLARIFICATION_TURNS:
        answer = generate_answer(
            query=combined_query,
            context=results,
            force=True
        )
        return {
            "type": "answer",
            "answer": answer,
            "context": results
        }

    
    if confidence < 0.55 or len(categories) > 1:
        question = generate_clarifying_question(
            query=combined_query,
            categories=categories
        )
        return {
            "type": "clarification",
            "question": question,
            "turn": turn + 1
        }

    
    answer = generate_answer(combined_query, results)
    return {
        "type": "answer",
        "answer": answer,
        "context": results
    }




@router.post("/dns", response_model=SearchResponse, operation_id="search_dns")
def search_dns(req: SearchRequest):
    return run_category_search(req.query, "dns")


@router.post("/dns/followup", response_model=SearchResponse, operation_id="search_dns_followup")
def search_dns_followup(req: ClarificationRequest):
    return run_followup_search(
        req.previous_query,
        req.clarification_answer,
        req.turn,
        "dns"
    )


@router.post("/vpn", response_model=SearchResponse, operation_id="search_vpn")
def search_vpn(req: SearchRequest):
    return run_category_search(req.query, "vpn")


@router.post("/vpn/followup", response_model=SearchResponse, operation_id="search_vpn_followup")
def search_vpn_followup(req: ClarificationRequest):
    return run_followup_search(
        req.previous_query,
        req.clarification_answer,
        req.turn,
        "vpn"
    )


@router.post("/firewall", response_model=SearchResponse, operation_id="search_firewall")
def search_firewall(req: SearchRequest):
    return run_category_search(req.query, "firewall")


@router.post("/firewall/followup", response_model=SearchResponse, operation_id="search_firewall_followup")
def search_firewall_followup(req: ClarificationRequest):
    return run_followup_search(
        req.previous_query,
        req.clarification_answer,
        req.turn,
        "firewall"
    )


@router.post("/proxy", response_model=SearchResponse, operation_id="search_proxy")
def search_proxy(req: SearchRequest):
    return run_category_search(req.query, "proxy")


@router.post("/proxy/followup", response_model=SearchResponse, operation_id="search_proxy_followup")
def search_proxy_followup(req: ClarificationRequest):
    return run_followup_search(
        req.previous_query,
        req.clarification_answer,
        req.turn,
        "proxy"
    )
