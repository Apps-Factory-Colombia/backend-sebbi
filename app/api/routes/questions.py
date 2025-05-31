from fastapi import APIRouter, HTTPException
from app.models.question import Question, QuestionResponse
from app.core.service_facade import app_facade

router = APIRouter(prefix="/questions", tags=["questions"])

@router.post("/ask", response_model=QuestionResponse)
async def ask_question(question: Question):
    try:
        result = await app_facade.process_question_with_documents(
            question=question.text,
            document_urls=question.context if question.context else None
        )
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["response"])
            
        return QuestionResponse(response=result["response"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 