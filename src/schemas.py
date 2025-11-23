from pydantic import BaseModel

from src.enums import DocumentCategory


# 요청 데이터 모델 (Spring Boot에서 받을 데이터)
class FeedbackRequest(BaseModel):
    category: DocumentCategory
    keywords: list
    request_type: int
    description: str
    user_text: str
    # 필요하다면 이전 대화 내역(history) 필드 추가 가능


# 응답 데이터 모델 (Spring Boot로 보낼 데이터)
class FeedbackResponse(BaseModel):
    feedback: list[str]  # 피드백


class EvaluationRequest(BaseModel):
    category: DocumentCategory
    keywords: list[str]
    description: str
    user_text: str


class EvaluationResponse(BaseModel):
    eval: str
