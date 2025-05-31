from fastapi import APIRouter, HTTPException, Path, Query
from typing import List, Optional
from app.models.document import DocumentCreate, DocumentUpdate, DocumentResponse, DocumentDelete, AutocompleteRequest, AutocompleteResponse
from app.services.document_service import document_service
from app.core.service_facade import app_facade

router = APIRouter(prefix="/documents", tags=["documents"])

@router.get("/test")
async def test_documents_endpoint():
    return {"status": "documents router test OK", "method": "GET"}

@router.get("/simple")
async def simple_endpoint():
    return {"message": "endpoint simple sin query params"}

@router.get("/with-param")
async def with_param_endpoint(email: Optional[str] = Query(None)):
    return {"message": f"endpoint con param email: {email}"}

@router.post("/create", response_model=DocumentResponse)
async def create_document(document_data: DocumentCreate):
    """
    Crea un nuevo documento
    """
    try:
        document = document_service.create_document(
            content=document_data.content,
            email=document_data.email
        )
        return document
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/list")
async def get_documents_list(email: Optional[str] = Query(None, description="Email del usuario")):
    """
    Obtiene todos los documentos de un usuario
    """
    try:
        if not email:
            raise HTTPException(status_code=400, detail="El parámetro email es requerido")
        
        documents = document_service.get_documents_by_email(email)
        return {"documents": documents, "count": len(documents)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/all")
async def get_all_documents(email: Optional[str] = Query(None, description="Email del usuario")):
    """
    Endpoint alternativo para obtener todos los documentos
    """
    try:
        if not email:
            raise HTTPException(status_code=400, detail="El parámetro email es requerido")
        
        documents = document_service.get_documents_by_email(email)
        return {"documents": documents, "count": len(documents)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int = Path(..., description="ID del documento"), 
    email: str = Query(..., description="Email del usuario")
):
    """
    Obtiene un documento por su ID
    """
    try:
        document = document_service.get_document_by_id(document_id, email)
        return document
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_data: DocumentUpdate,
    document_id: int = Path(..., description="ID del documento"),
    email: str = Query(..., description="Email del usuario")
):
    """
    Actualiza un documento
    """
    try:
        document = document_service.update_document(
            document_id=document_id,
            content=document_data.content,
            email=email
        )
        return document
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{document_id}", response_model=DocumentResponse)
async def delete_document(
    document_id: int = Path(..., description="ID del documento"),
    email: str = Query(..., description="Email del usuario")
):
    """
    Elimina un documento
    """
    try:
        document = document_service.delete_document(document_id, email)
        return document
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/autocomplete", response_model=AutocompleteResponse)
async def autocomplete_text_document(request_data: AutocompleteRequest):
    """
    Autocompleta un texto utilizando Gemini.
    El texto puede ser un título o un párrafo.
    """
    try:
        result = await app_facade.complete_user_workflow(request_data.text_input)
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["completion"])
            
        return AutocompleteResponse(autocompleted_text=result["completion"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al autocompletar el texto: {str(e)}") 