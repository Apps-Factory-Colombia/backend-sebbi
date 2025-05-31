from abc import ABC, abstractmethod
from typing import Protocol
from app.services.gemini_service import GeminiService

class AIServiceProtocol(Protocol):
    async def generate_response(self, text: str) -> str: ...
    async def generate_response_with_context(self, text: str, pdf_urls: list[str]) -> str: ...
    async def autocomplete_text(self, text_input: str) -> str: ...

class AIServiceFactory(ABC):
    @abstractmethod
    def create_service(self) -> AIServiceProtocol:
        pass

class GeminiServiceFactory(AIServiceFactory):
    def create_service(self) -> AIServiceProtocol:
        return GeminiService()

class AIServiceFactoryRegistry:
    _factories = {
        "gemini": GeminiServiceFactory,
        "default": GeminiServiceFactory
    }
    
    @classmethod
    def get_factory(cls, service_type: str = "default") -> AIServiceFactory:
        factory_class = cls._factories.get(service_type, cls._factories["default"])
        return factory_class()
    
    @classmethod
    def register_factory(cls, service_type: str, factory_class: type[AIServiceFactory]):
        cls._factories[service_type] = factory_class

def create_ai_service(service_type: str = "default") -> AIServiceProtocol:
    factory = AIServiceFactoryRegistry.get_factory(service_type)
    return factory.create_service() 