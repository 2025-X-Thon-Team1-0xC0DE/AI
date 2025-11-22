from fastapi import APIRouter, HTTPException
from openai import AsyncOpenAI

from settings import OPENAI_API_KEY
from src.prompters import FeedbackPrompter
from src.schemas import FeedbackRequest, FeedbackResponse

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

router = APIRouter(prefix="/api", tags=["gaide-api"])
@router.post("/feedback")
async def generate_feedback(request: FeedbackRequest):
    try:
        prompter = FeedbackPrompter(category=request.category)
        full_system_prompt = prompter.get_prompt()

        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": full_system_prompt},
                {"role": "user", "content": request.user_text},
            ],
            temperature=0.7,
            max_tokens=500,
        )

        feedback_content = list(response.choices[0].message.content.split("\n\n")) \
            if response.choices[0].message.content else []
        
        return FeedbackResponse(
            category=request.category,
            status="success",
            feedback=feedback_content,
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))