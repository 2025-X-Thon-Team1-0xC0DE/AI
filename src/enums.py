from enum import Enum

# 문서 카테고리 정의 (오타 방지용 Enum)
class DocumentCategory(str, Enum):
    RESUME = "resume"  # 자기소개서
    REPORT = "report"  # 보고서/기획서
    ESSAY = "essay"  # 논문/에세이
    EMAIL = "email"  # 비즈니스 메일