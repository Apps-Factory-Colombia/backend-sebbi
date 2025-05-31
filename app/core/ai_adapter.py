from abc import ABC, abstractmethod
from typing import List
from app.services.gemini_service import GeminiService

class AIAdapter(ABC):
    @abstractmethod
    async def process_text(self, text: str) -> str:
        pass
    
    @abstractmethod
    async def process_with_documents(self, text: str, documents: List[str]) -> str:
        pass
    
    @abstractmethod
    async def complete_text(self, text: str) -> str:
        pass

class GeminiAdapter(AIAdapter):
    def __init__(self):
        self._gemini_service = GeminiService()
    
    async def process_text(self, text: str) -> str:
        return await self._gemini_service.generate_response(text)
    
    async def process_with_documents(self, text: str, documents: List[str]) -> str:
        return await self._gemini_service.generate_response_with_context(text, documents)
    
    async def complete_text(self, text: str) -> str:
        return await self._gemini_service.autocomplete_text(text)

class MockAIAdapter(AIAdapter):
    async def process_text(self, text: str) -> str:
        return f"Respuesta simulada para: {text}"
    
    async def process_with_documents(self, text: str, documents: List[str]) -> str:
        return f"Respuesta con {len(documents)} documentos para: {text}"
    
    async def complete_text(self, text: str) -> str:
        return f"{text} [continuación simulada]"

class AIAdapterFactory:
    _adapters = {
        "gemini": GeminiAdapter,
        "mock": MockAIAdapter,
        "default": GeminiAdapter
    }
    
    @classmethod
    def create_adapter(cls, adapter_type: str = "default") -> AIAdapter:
        adapter_class = cls._adapters.get(adapter_type, cls._adapters["default"])
        return adapter_class()
    
    @classmethod
    def register_adapter(cls, adapter_type: str, adapter_class: type[AIAdapter]):
        cls._adapters[adapter_type] = adapter_class

def get_ai_adapter(adapter_type: str = "default") -> AIAdapter:
    return AIAdapterFactory.create_adapter(adapter_type) 