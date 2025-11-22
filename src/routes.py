# 요청을 받는 핵심적인 파일

from fastapi import APIRouter, HTTPException
from openai import AsyncOpenAI

from settings import OPENAI_API_KEY
from src.prompters import FeedbackPrompter
from src.schemas import FeedbackRequest, FeedbackResponse

client = AsyncOpenAI(api_key=OPENAI_API_KEY)
router = APIRouter(prefix="/api", tags=["gaide-api"])


# 피드백 생성 엔드포인트
@router.post("/feedback")
async def generate_feedback(request: FeedbackRequest):
    try:
        # 프롬프터 생성
        prompter = FeedbackPrompter(category=request.category, keyword=request.keyword)
        full_system_prompt = prompter.get_prompt()

        # OpenAI API 호출
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": full_system_prompt},
                {"role": "user", "content": request.user_text},
            ],
            temperature=0.7,
            max_tokens=500,
        )

        # 응답 파싱
        feedback_content = (
            list(response.choices[0].message.content.split("\n\n"))
            if response.choices[0].message.content
            else []
        )

        # 응답 반환
        return FeedbackResponse(
            category=request.category,
            status="success",
            feedback=feedback_content,
        )

    # 예외 처리
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
