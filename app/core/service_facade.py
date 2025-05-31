from typing import Dict, List, Optional
from app.core.ai_factory import create_ai_service
from app.core.ai_adapter import get_ai_adapter
from app.services.supabase_service import supabase_service
from app.services.pdf_service import pdf_service
from app.services.document_service import document_service

class ApplicationFacade:
    def __init__(self):
        self._ai_service = create_ai_service()
        self._ai_adapter = get_ai_adapter()
        self._db_service = supabase_service
        self._pdf_service = pdf_service
        self._document_service = document_service
    
    async def process_question_with_documents(self, 
                                            question: str, 
                                            user_id: Optional[str] = None,
                                            document_urls: Optional[List[str]] = None) -> Dict:
        try:
            if document_urls:
                response = await self._ai_adapter.process_with_documents(question, document_urls)
            else:
                response = await self._ai_adapter.process_text(question)
            
            result = {
                "question": question,
                "response": response,
                "status": "success"
            }
            
            return result
        except Exception as e:
            return {
                "question": question,
                "response": f"Error procesando la pregunta: {str(e)}",
                "status": "error"
            }
    
    async def complete_user_workflow(self, text_input: str) -> Dict:
        try:
            completion = await self._ai_adapter.complete_text(text_input)
            
            return {
                "original_text": text_input,
                "completion": completion,
                "status": "success"
            }
        except Exception as e:
            return {
                "original_text": text_input,
                "completion": f"Error en autocompletado: {str(e)}",
                "status": "error"
            }
    
    async def authenticate_and_get_profile(self, email: str, password: str) -> Dict:
        try:
            auth_result = self._db_service.login_user(email, password)
            return {
                "authenticated": True,
                "user_data": auth_result,
                "status": "success"
            }
        except Exception as e:
            return {
                "authenticated": False,
                "error": str(e),
                "status": "error"
            }
    
    async def register_new_user(self, name: str, email: str, password: str) -> Dict:
        try:
            user_result = self._db_service.register_user(name, email, password)
            return {
                "registered": True,
                "user_data": user_result,
                "status": "success"
            }
        except Exception as e:
            return {
                "registered": False,
                "error": str(e),
                "status": "error"
            }

app_facade = ApplicationFacade() 