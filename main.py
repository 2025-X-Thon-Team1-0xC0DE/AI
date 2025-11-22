import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="gAIde Model Server")


# 문서 카테고리 정의 (오타 방지용 Enum)
class DocumentCategory(str, Enum):
    RESUME = "resume"  # 자기소개서
    REPORT = "report"  # 보고서/기획서
    ESSAY = "essay"  # 논문/에세이
    EMAIL = "email"  # 비즈니스 메일


# 요청 데이터 모델 (Spring Boot에서 받을 데이터)
class FeedbackRequest(BaseModel):
    category: DocumentCategory
    user_text: str
    # 필요하다면 이전 대화 내역(history) 필드 추가 가능


# System Prompt
# 핵심: 카테고리별로 AI의 '검토 기준'과 '성격'을 다르게 설정
PROMPT_TEMPLATES = {
    DocumentCategory.RESUME: """
    당신은 15년 차 베테랑 인사 담당자입니다.
    사용자의 '자기소개서'를 검토하고 피드백을 주어야 합니다.
    
    [원칙]
    1. 절대로 문장을 대신 다시 쓰거나 생성하지 마십시오.
    2. 오직 '질문'과 '지적'만 하십시오.
    3. 구체적인 경험이나 수치적 성과가 부족하면 날카롭게 지적하십시오.
    4. 어투는 정중하지만 냉철하게 유지하십시오.
    """,
    DocumentCategory.REPORT: """
    당신은 논리적이고 깐깐한 전략 기획 팀장입니다.
    사용자의 '비즈니스 보고서'를 검토합니다.
    
    [원칙]
    1. 문장을 직접 수정해 주지 마십시오. 논리의 비약만 지적하십시오.
    2. '근거 데이터'가 부족하거나, 결론이 모호한 부분을 찾아서 역질문하십시오.
    3. 두괄식 구성이 아니면 지적하십시오.
    """,
    DocumentCategory.ESSAY: """
    당신은 대학원 지도 교수입니다.
    사용자의 '논문' 또는 '에세이'를 지도합니다.
    
    [원칙]
    1. 글을 고쳐주지 말고, 더 깊이 사고하도록 유도하십시오.
    2. 주장의 독창성과 인과관계를 중점적으로 확인하십시오.
    3. 표현이 너무 구어체이거나 비학문적인 단어가 쓰였는지 체크하십시오.
    """,
}

# 기본 공통 규칙
COMMON_RULE = "\n\n중요: 사용자의 글을 절대 직접 수정하지 마세요. 대신 '이 부분은 ~한 이유로 어색함', '~에 대한 검증이 부족함' 등의 형식으로 가이드만 제시하세요."


# API 엔드포인트
@app.post("/api/feedback")
async def generate_feedback(request: FeedbackRequest):
    try:
        # 카테고리에 맞는 시스템 프롬프트 로드
        system_instruction = PROMPT_TEMPLATES.get(
            request.category,
            PROMPT_TEMPLATES[DocumentCategory.RESUME], # 기본값 처리
        )
        full_system_prompt = system_instruction + COMMON_RULE

        # OpenAI API 호출
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": full_system_prompt},
                {"role": "user", "content": request.user_text},
            ],
            temperature=0.7,
            max_tokens=500,  # 답변 길이 제한
        )

        feedback_content = list(response.choices[0].message.content.split("\n\n"))

        return {
            "category": request.category,
            "status": "success",
            "feedback": feedback_content,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
