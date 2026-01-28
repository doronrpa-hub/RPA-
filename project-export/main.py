"""
RPA-PORT Israeli Customs AI
Website: https://www.rpa-port.com
Contact: devrpa@rpa-port.co.il

AI-powered Israeli Customs Classification System using Anthropic Claude
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import anthropic
import os

# Create FastAPI application
app = FastAPI(
    title="RPA-PORT Customs AI",
    description="AI-powered Israeli Customs Classification System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.rpa-port.com", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# System prompt for Claude
SYSTEM_PROMPT = """אתה מומחה בכיר למכס ישראלי של חברת RPA-PORT LTD.

📚 מקורות ידע:
- פקודת המכס (נוסח חדש)
- נוהל תש"ר 2024 (תהליך השחרור)
- צו תעריף המכס והפטורים ומס קנייה
- הסכמי סחר בינלאומיים (ארה"ב, האיחוד האירופי, EFTA, ועוד)
- דרישות משרדי ממשלה (בריאות, חקלאות, מכון התקנים)

🎯 יכולות:
- סיווג טובין לפי HS Code (10 ספרות)
- ניתוח הצהרות יבוא ויצוא
- חישוב מיסים (מכס, מע"מ, מס קנייה)
- זיהוי הטבות מהסכמי סחר
- בדיקת דרישות רישוי ותקינה

🗣️ שפה:
- מדבר עברית מקצועית
- יכול לענות גם באנגלית

📋 כללים:
1. תמיד לציין מקור המידע
2. להזהיר כשיש אי-ודאות
3. להפנות לייעוץ מקצועי בנושאים מורכבים

אתר: www.rpa-port.com
מייל: devrpa@rpa-port.co.il"""


# Request/Response Models
class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = None
    tenant_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    tenant_id: Optional[str] = None

class ClassifyRequest(BaseModel):
    description: str
    additional_info: Optional[Dict[str, Any]] = None


# Helper function
def get_anthropic_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500, 
            detail="ANTHROPIC_API_KEY environment variable not configured"
        )
    return anthropic.Anthropic(api_key=api_key)


# Routes
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "RPA-PORT Customs AI",
        "version": "1.0.0",
        "website": "https://www.rpa-port.com",
        "contact": "devrpa@rpa-port.co.il",
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "chat": "POST /api/chat",
            "classify": "POST /api/classify",
            "agreements": "GET /api/agreements"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint for load balancers"""
    return {
        "status": "healthy",
        "service": "rpa-port-customs-ai",
        "version": "1.0.0"
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with the Customs AI
    
    Supports Hebrew and English
    """
    try:
        client = get_anthropic_client()
        
        # Build messages
        messages = []
        if request.history:
            messages.extend(request.history)
        messages.append({"role": "user", "content": request.message})
        
        # Call Claude
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=messages,
        )
        
        return ChatResponse(
            response=response.content[0].text,
            tenant_id=request.tenant_id
        )
        
    except anthropic.APIError as e:
        raise HTTPException(status_code=500, detail=f"Claude API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/classify")
async def classify(request: ClassifyRequest):
    """
    Classify a product and get HS code
    
    Returns classification with HS code, duty rates, and requirements
    """
    prompt = f"""סווג את המוצר הבא לפי תעריף המכס הישראלי:

**תיאור המוצר:** {request.description}

{f"**מידע נוסף:** {request.additional_info}" if request.additional_info else ""}

אנא החזר:
1. קוד HS מלא (10 ספרות)
2. תיאור בעברית ובאנגלית
3. שיעור מכס
4. מס קנייה (אם יש)
5. דרישות מיוחדות (רישיונות, תקנים)
6. הסכמי סחר רלוונטיים
7. רמת ודאות בסיווג (0-100%)"""
    
    try:
        client = get_anthropic_client()
        
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        
        return {"classification": response.content[0].text}
        
    except anthropic.APIError as e:
        raise HTTPException(status_code=500, detail=f"Claude API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/agreements")
async def list_agreements():
    """List all trade agreements Israel has"""
    return {
        "agreements": [
            {"code": "2", "name": "Israel-USA FTA", "name_he": "הסכם ישראל-ארה\"ב", "year": 1985},
            {"code": "92", "name": "Israel-EU Association", "name_he": "הסכם ישראל-אירופה", "year": 1995},
            {"code": "EFTA", "name": "Israel-EFTA", "name_he": "הסכם ישראל-EFTA", "year": 1992},
            {"code": "CA", "name": "Israel-Canada FTA", "name_he": "הסכם ישראל-קנדה", "year": 1997},
            {"code": "MX", "name": "Israel-Mexico FTA", "name_he": "הסכם ישראל-מקסיקו", "year": 2000},
            {"code": "TR", "name": "Israel-Turkey FTA", "name_he": "הסכם ישראל-טורקיה", "year": 1997},
            {"code": "KR", "name": "Israel-South Korea FTA", "name_he": "הסכם ישראל-קוריאה", "year": 2021},
            {"code": "AE", "name": "Israel-UAE FTA", "name_he": "הסכם ישראל-איחוד האמירויות", "year": 2022},
            {"code": "UA", "name": "Israel-Ukraine FTA", "name_he": "הסכם ישראל-אוקראינה", "year": 2021},
            {"code": "VN", "name": "Israel-Vietnam FTA", "name_he": "הסכם ישראל-וייטנאם", "year": 2024},
            {"code": "JO", "name": "Israel-Jordan FTA", "name_he": "הסכם ישראל-ירדן", "year": 1995},
            {"code": "EG", "name": "Israel-Egypt QIZ", "name_he": "אזורי QIZ ישראל-מצרים", "year": 2005},
            {"code": "CO", "name": "Israel-Colombia FTA", "name_he": "הסכם ישראל-קולומביה", "year": 2020},
            {"code": "PA", "name": "Israel-Panama FTA", "name_he": "הסכם ישראל-פנמה", "year": 2020},
            {"code": "MERCOSUR", "name": "Israel-Mercosur", "name_he": "הסכם ישראל-מרקוסור", "year": 2007},
        ]
    }


# Run with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
